<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { authService } from "./services/authService.js";

const router = useRouter();
const showExpiredPopup = ref(false);
const showWarningPopup = ref(false);
const minutesLeft = ref(5);

const WARN_BEFORE_MS = 5 * 60 * 1000; // warn 5 minutes before expiry

let checkInterval = null;

// ── Screen-capture deterrents ──────────────────────────────────────
// NOTE: A browser cannot truly block screenshots/recording. These are
// deterrents: they disable copy/right-click/printing and warn on the
// PrintScreen key (best-effort clipboard wipe). They do not stop OS
// capture tools or a phone camera.
const showCaptureWarning = ref(false);
let captureWarningTimer = null;

// Allow normal copy/selection inside editable fields so forms stay usable.
function isEditable(el) {
  if (!el) return false;
  const tag = el.tagName;
  return tag === "INPUT" || tag === "TEXTAREA" || el.isContentEditable;
}

function flashCaptureWarning() {
  showCaptureWarning.value = true;
  clearTimeout(captureWarningTimer);
  captureWarningTimer = setTimeout(() => {
    showCaptureWarning.value = false;
  }, 2500);
}

function blockContextMenu(e) {
  e.preventDefault();
}

function blockCopyCut(e) {
  if (isEditable(e.target)) return; // keep form fields functional
  e.preventDefault();
  if (e.clipboardData) e.clipboardData.setData("text/plain", "");
}

function onKeyDown(e) {
  // Ctrl/Cmd+P (print), Ctrl/Cmd+S (save page) → block + warn
  const k = e.key?.toLowerCase();
  if ((e.ctrlKey || e.metaKey) && (k === "p" || k === "s")) {
    e.preventDefault();
    flashCaptureWarning();
  }
}

async function onKeyUp(e) {
  // PrintScreen fires on keyup in most browsers; wipe the clipboard image
  // (best-effort — requires focus + permission) and warn the user.
  if (e.key === "PrintScreen") {
    try {
      await navigator.clipboard.writeText(" ");
    } catch (_) {
      /* clipboard not writable — ignore */
    }
    flashCaptureWarning();
  }
}

function onBeforePrint() {
  flashCaptureWarning();
}

function handleLogout() {
  showExpiredPopup.value = false;
  showWarningPopup.value = false;
  authService.logout();
  router.push({ name: "Login" });
}

function dismissWarning() {
  showWarningPopup.value = false;
}

function checkSession() {
  const token = localStorage.getItem("token");
  if (!token) return;

  const expiry = authService.getTokenExpiry();
  if (!expiry) return;

  const now = Date.now();
  const remaining = expiry - now;

  if (remaining <= 0) {
    showWarningPopup.value = false;
    showExpiredPopup.value = true;
    clearInterval(checkInterval);
  } else if (remaining <= WARN_BEFORE_MS) {
    minutesLeft.value = Math.ceil(remaining / 60000);
    showWarningPopup.value = true;
  }
}

onMounted(() => {
  checkInterval = setInterval(checkSession, 30 * 1000); // check every 30s
  checkSession();

  // Screen-capture deterrents
  document.body.classList.add("no-select");
  document.addEventListener("contextmenu", blockContextMenu);
  document.addEventListener("copy", blockCopyCut);
  document.addEventListener("cut", blockCopyCut);
  document.addEventListener("dragstart", blockContextMenu);
  document.addEventListener("keydown", onKeyDown);
  document.addEventListener("keyup", onKeyUp);
  window.addEventListener("beforeprint", onBeforePrint);

  // warm up Vercel serverless backend on app load (fire-and-forget)
  fetch(`${import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'}/graphql`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: '{ __typename }' }),
  }).catch(() => {});
});

onUnmounted(() => {
  clearInterval(checkInterval);

  clearTimeout(captureWarningTimer);
  document.body.classList.remove("no-select");
  document.removeEventListener("contextmenu", blockContextMenu);
  document.removeEventListener("copy", blockCopyCut);
  document.removeEventListener("cut", blockCopyCut);
  document.removeEventListener("dragstart", blockContextMenu);
  document.removeEventListener("keydown", onKeyDown);
  document.removeEventListener("keyup", onKeyUp);
  window.removeEventListener("beforeprint", onBeforePrint);
});
</script>

<template>
  <router-view />

  <!-- Session expired popup -->
  <div v-if="showExpiredPopup" class="session-overlay">
    <div class="session-modal">
      <div class="session-icon">⏰</div>
      <h2 class="session-title">Sesi Telah Berakhir</h2>
      <p class="session-desc">
        Sesi login Anda telah habis. Silakan login kembali untuk melanjutkan.
      </p>
      <button class="session-btn" @click="handleLogout">Login Kembali</button>
    </div>
  </div>

  <!-- Screen-capture deterrent warning -->
  <div v-if="showCaptureWarning" class="capture-warning">
    <span class="capture-warning-icon">🚫</span>
    <span>Tangkapan layar &amp; pencetakan dibatasi pada aplikasi ini.</span>
  </div>

  <!-- Session expiring soon warning -->
  <div v-if="showWarningPopup && !showExpiredPopup" class="session-warning">
    <div class="session-warning-content">
      <span class="session-warning-icon">⚠️</span>
      <span class="session-warning-text">
        Sesi Anda akan berakhir dalam
        <strong>{{ minutesLeft }} menit</strong>
      </span>
      <button class="session-warning-dismiss" @click="dismissWarning">✕</button>
    </div>
  </div>
</template>

<style scoped>
.session-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(2px);
}

.session-modal {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px 36px;
  max-width: 380px;
  width: 90%;
  text-align: center;
  box-shadow: var(--shadow);
}

.session-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.session-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-h);
  margin: 0 0 12px;
}

.session-desc {
  color: var(--text);
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 24px;
}

.session-btn {
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 28px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.session-btn:hover {
  opacity: 0.85;
}

/* Warning toast */
.session-warning {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9998;
  animation: slide-in 0.3s ease;
}

.session-warning-content {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fff8e1;
  border: 1px solid #f59e0b;
  border-radius: 10px;
  padding: 12px 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  font-size: 14px;
  color: #92400e;
}

.session-warning-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.session-warning-text strong {
  font-weight: 700;
}

.session-warning-dismiss {
  background: none;
  border: none;
  cursor: pointer;
  color: #92400e;
  font-size: 14px;
  padding: 0 2px;
  margin-left: 4px;
  opacity: 0.7;
  flex-shrink: 0;
}

.session-warning-dismiss:hover {
  opacity: 1;
}

@keyframes slide-in {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Screen-capture deterrent warning banner */
.capture-warning {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10000;
  display: flex;
  align-items: center;
  gap: 10px;
  background: #1e293b;
  color: #fff;
  border-radius: 10px;
  padding: 12px 20px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.3);
  animation: slide-in 0.25s ease;
}

.capture-warning-icon {
  font-size: 18px;
}
</style>

<!-- Global (non-scoped): selection + print rules must reach <body> -->
<style>
/* Disable text selection app-wide, but keep editable fields usable */
body.no-select,
body.no-select * {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
body.no-select input,
body.no-select textarea,
body.no-select [contenteditable="true"] {
  -webkit-user-select: text;
  -moz-user-select: text;
  -ms-user-select: text;
  user-select: text;
}

/* Block printing: replace page content with a notice when printed */
@media print {
  body * {
    visibility: hidden !important;
  }
  body::before {
    content: "Pencetakan dinonaktifkan untuk alasan keamanan.";
    visibility: visible;
    position: fixed;
    top: 40%;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 18px;
    font-family: sans-serif;
    color: #000;
  }
}
</style>
