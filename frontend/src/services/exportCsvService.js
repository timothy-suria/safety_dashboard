import ExcelJS from 'exceljs';

/**
 * Export data to XLSX using ExcelJS (full style support).
 *
 * columns: Array of { label, key?, transform?, image?, formula? }
 *   - key: direct property lookup
 *   - transform: custom fn, takes priority over key
 *   - image: if true, value is a URL — image is fetched and embedded at original ratio
 *   - formula: if true, value starting with "=" is written as an Excel formula
 *
 * rows: Array of plain objects
 */

async function fetchImageBuffer(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) return null;
    return await res.arrayBuffer();
  } catch {
    return null;
  }
}

function getImageExtension(url) {
  const match = url.match(/\.(png|gif|webp|jpe?g)(\?|$)/i);
  if (!match) return 'jpeg';
  const ext = match[1].toLowerCase();
  return ext === 'jpg' ? 'jpeg' : ext;
}

function getImageNaturalSize(buffer) {
  return new Promise((resolve) => {
    const blob = new Blob([buffer]);
    const blobUrl = URL.createObjectURL(blob);
    const img = new Image();
    img.onload = () => {
      resolve({ width: img.naturalWidth, height: img.naturalHeight });
      URL.revokeObjectURL(blobUrl);
    };
    img.onerror = () => {
      resolve({ width: 150, height: 100 });
      URL.revokeObjectURL(blobUrl);
    };
    img.src = blobUrl;
  });
}

// Scale dimensions to fit within maxW x maxH, preserving aspect ratio.
// Defaults match the column width (100/7 char ≈ 100px) and row height (75pt × 96/72 ≈ 100px).
function scaleToFit(w, h, maxW = 95, maxH = 95) {
  if (!w || !h) return { width: maxW, height: maxH };
  const scale = Math.min(maxW / w, maxH / h, 1); // never upscale
  return { width: Math.round(w * scale), height: Math.round(h * scale) };
}

export async function exportToCsv(filename, columns, rows) {
  const wb = new ExcelJS.Workbook();
  const ws = wb.addWorksheet('Data');

  const centerAlign = { horizontal: 'center', vertical: 'middle', wrapText: true };

  // Column widths: A = 40px, rest = 100px (ExcelJS uses "character units" ~= px/7)
  ws.columns = columns.map((col, i) => ({
    header: col.label,
    key: String(i),
    width: i === 0 ? 40 / 7 : 100 / 7,
  }));

  // Style header row
  const headerRow = ws.getRow(1);
  headerRow.eachCell((cell) => {
    cell.alignment = centerAlign;
    cell.font = { bold: true };
  });

  // Track image placements: { url, rowIndex (0-based ws), colIndex (0-based ws) }
  const imagePlacements = [];

  // Add data rows
  rows.forEach((row, rowIdx) => {
    const rowValues = columns.map((col, colIdx) => {
      const val = col.transform ? col.transform(row) : row[col.key];
      if (col.image && val) {
        // Schedule image embedding — leave cell empty for now
        imagePlacements.push({ url: String(val), rowIndex: rowIdx + 1, colIndex: colIdx });
        return '';
      }
      if (col.formula && val != null && String(val).startsWith('=')) {
        return { formula: String(val).slice(1) };
      }
      return val == null ? '' : String(val);
    });

    const exRow = ws.addRow(rowValues);
    exRow.height = 75; // ~100px (ExcelJS height is in points: 100px * 72/96 ≈ 75pt)
    exRow.eachCell({ includeEmpty: true }, (cell) => {
      cell.alignment = centerAlign;
    });
  });

  // Fetch and embed images at their natural aspect ratio
  for (const { url, rowIndex, colIndex } of imagePlacements) {
    const buffer = await fetchImageBuffer(url);
    if (!buffer) continue;
    const ext = getImageExtension(url);
    const { width: natW, height: natH } = await getImageNaturalSize(buffer);
    const { width, height } = scaleToFit(natW, natH);
    const imageId = wb.addImage({ buffer, extension: ext });
    // Using tl + ext (not br) so image keeps its ratio and is freely resizable
    ws.addImage(imageId, {
      tl: { col: colIndex, row: rowIndex },
      ext: { width, height },
      editAs: 'oneCell',
    });
  }

  // Download
  const buffer = await wb.xlsx.writeBuffer();
  const blob = new Blob([buffer], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename.replace(/\.(csv|xlsx)$/i, '') + '.xlsx';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
