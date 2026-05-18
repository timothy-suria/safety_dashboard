<script setup>
const props = defineProps({
  currentPage: { type: Number, required: true },
  totalPages:  { type: Number, required: true },
  totalItems:  { type: Number, required: true },
  perPage:     { type: Number, required: true },
});

const emit = defineEmits(["page", "per-page"]);

function pages() {
  const p = props.totalPages;
  const c = props.currentPage;
  if (p <= 7) return Array.from({ length: p }, (_, i) => i + 1);
  const result = [];
  if (c <= 4) {
    result.push(1, 2, 3, 4, 5, "…", p);
  } else if (c >= p - 3) {
    result.push(1, "…", p - 4, p - 3, p - 2, p - 1, p);
  } else {
    result.push(1, "…", c - 1, c, c + 1, "…", p);
  }
  return result;
}

const start = () => (props.currentPage - 1) * props.perPage + 1;
const end   = () => Math.min(props.currentPage * props.perPage, props.totalItems);
</script>

<template>
  <div class="pagination-bar" v-if="totalItems > 0">
    <span class="pg-info">
      {{ start() }}–{{ end() }} dari {{ totalItems }} data
    </span>

    <div class="pg-controls">
      <button class="pg-btn" :disabled="currentPage === 1" @click="emit('page', currentPage - 1)">‹</button>

      <template v-for="p in pages()" :key="p">
        <span v-if="p === '…'" class="pg-ellipsis">…</span>
        <button
          v-else
          class="pg-btn"
          :class="{ active: p === currentPage }"
          @click="emit('page', p)"
        >{{ p }}</button>
      </template>

      <button class="pg-btn" :disabled="currentPage === totalPages" @click="emit('page', currentPage + 1)">›</button>
    </div>

    <select class="pg-size" :value="perPage" @change="emit('per-page', +$event.target.value)">
      <option value="10">10 / hal</option>
      <option value="25">25 / hal</option>
      <option value="50">50 / hal</option>
      <option value="100">100 / hal</option>
    </select>
  </div>
</template>

<style scoped>
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid #e5e7eb;
  font-size: 13px;
  color: #64748b;
}

.pg-info {
  white-space: nowrap;
}

.pg-controls {
  display: flex;
  align-items: center;
  gap: 3px;
}

.pg-btn {
  min-width: 32px;
  height: 32px;
  padding: 0 6px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: #fff;
  color: #374151;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pg-btn:hover:not(:disabled):not(.active) {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.pg-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #fff;
  font-weight: 600;
}

.pg-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pg-ellipsis {
  min-width: 28px;
  text-align: center;
  color: #94a3b8;
  font-size: 14px;
}

.pg-size {
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 13px;
  color: #374151;
  background: #fff;
  cursor: pointer;
  outline: none;
}

.pg-size:focus {
  border-color: #3b82f6;
}
</style>
