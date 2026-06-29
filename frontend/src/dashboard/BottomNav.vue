<template>
  <!-- Mobile-only bottom navigation. Hidden on >=768px via CSS. -->
  <nav class="bottom-nav">
    <!-- Dashboard: direct link -->
    <router-link
      to="/dashboard"
      class="bn-item"
      exact-active-class="active"
      @click="closeSheet"
    >
      <svg class="bn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="3" width="7" height="7" rx="1" />
        <rect x="14" y="3" width="7" height="7" rx="1" />
        <rect x="3" y="14" width="7" height="7" rx="1" />
        <rect x="14" y="14" width="7" height="7" rx="1" />
      </svg>
      <span>Dashboard</span>
    </router-link>

    <!-- Modul HSE: opens sheet -->
    <button
      class="bn-item"
      :class="{ active: isHseActive }"
      @click="toggleSheet('modul')"
    >
      <svg class="bn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="9" y1="13" x2="15" y2="13" />
        <line x1="9" y1="17" x2="15" y2="17" />
        <line x1="9" y1="9" x2="11" y2="9" />
      </svg>
      <span>Modul</span>
    </button>

    <!-- Laporan: opens sheet -->
    <button
      class="bn-item"
      :class="{ active: isReportsActive }"
      @click="toggleSheet('laporan')"
    >
      <svg class="bn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
      </svg>
      <span>Laporan</span>
    </button>

    <!-- Chat: direct link -->
    <router-link
      to="/dashboard/chat"
      class="bn-item"
      active-class="active"
      @click="closeSheet"
    >
      <svg class="bn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
      </svg>
      <span>Chat</span>
    </router-link>

    <!-- More: opens sheet -->
    <button
      class="bn-item"
      :class="{ active: isMoreActive }"
      @click="toggleSheet('more')"
    >
      <svg class="bn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="5" cy="12" r="1.5" />
        <circle cx="12" cy="12" r="1.5" />
        <circle cx="19" cy="12" r="1.5" />
      </svg>
      <span>Lainnya</span>
    </button>
  </nav>

  <!-- Bottom sheet + backdrop -->
  <Teleport to="body">
    <transition name="sheet-backdrop">
      <div v-if="activeSheet" class="sheet-backdrop" @click="closeSheet" />
    </transition>
    <transition name="sheet">
      <div v-if="activeSheet" class="sheet" role="dialog">
        <div class="sheet-handle" />

        <!-- Modul HSE -->
        <template v-if="activeSheet === 'modul'">
          <div class="sheet-title">Modul HSE</div>
          <router-link
            v-for="link in modulLinks"
            :key="link.to"
            :to="link.to"
            class="sheet-item"
            active-class="active"
            @click="closeSheet"
          >
            {{ link.label }}
          </router-link>
        </template>

        <!-- Laporan -->
        <template v-else-if="activeSheet === 'laporan'">
          <div class="sheet-title">Laporan</div>
          <router-link
            v-for="link in reportLinks"
            :key="link.to"
            :to="link.to"
            class="sheet-item"
            active-class="active"
            @click="closeSheet"
          >
            {{ link.label }}
          </router-link>
        </template>

        <!-- More -->
        <template v-else-if="activeSheet === 'more'">
          <div class="sheet-user">
            <div class="sheet-avatar">{{ initials }}</div>
            <div class="sheet-user-details">
              <span class="sheet-user-name">{{ displayName }}</span>
              <span class="sheet-user-meta"
                >{{ user?.role || '-'
                }}{{ user?.businessUnit ? ' · ' + user.businessUnit : '' }}</span
              >
            </div>
          </div>

          <router-link
            v-if="canAccessMasterData"
            to="/dashboard/master-data"
            class="sheet-item"
            active-class="active"
            @click="closeSheet"
          >
            <svg class="sheet-item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <ellipse cx="12" cy="5" rx="9" ry="3" />
              <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
              <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
            </svg>
            Master Data
          </router-link>

          <router-link
            to="/dashboard/settings"
            class="sheet-item"
            active-class="active"
            @click="closeSheet"
          >
            <svg class="sheet-item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
            </svg>
            Pengaturan
          </router-link>

          <button class="sheet-item sheet-logout" @click="handleLogout">
            <svg class="sheet-item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            Keluar
          </button>
        </template>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { authService } from '@/services/authService';
import { disablePush } from '@/services/pushService.js';

const route = useRoute();
const router = useRouter();

// null | 'modul' | 'laporan' | 'more'
const activeSheet = ref(null);

function toggleSheet(name) {
  activeSheet.value = activeSheet.value === name ? null : name;
}
function closeSheet() {
  activeSheet.value = null;
}

// Close the sheet whenever the route changes (covers back-button navigation).
watch(() => route.path, closeSheet);

const modulLinks = [
  { to: '/dashboard/modules/sop', label: 'Standard of Procedure (SoP)' },
  { to: '/dashboard/modules/wi', label: 'Working Instruction (WI)' },
  { to: '/dashboard/modules/form', label: 'Form' },
  { to: '/dashboard/modules/edukasi', label: 'Safety Sharing (Edukasi)' },
];

const reportLinks = [
  { to: '/dashboard/reports/inspection-k3l', label: 'Inspeksi K3L' },
  { to: '/dashboard/reports/hse-daily', label: 'Permit Kerja HSE' },
  { to: '/dashboard/reports/case-incident', label: 'Insiden & Kecelakaan Kerja' },
];

const isHseActive = computed(() => route.path.startsWith('/dashboard/modules'));
const isReportsActive = computed(() => route.path.startsWith('/dashboard/reports'));
const isMoreActive = computed(
  () =>
    route.path.startsWith('/dashboard/master-data') ||
    route.path.startsWith('/dashboard/settings'),
);

const user = authService.getCurrentUser();
const canAccessMasterData = authService.canAccessMasterData();
const displayName = computed(
  () => user?.fullName || user?.username || user?.email || '',
);
const initials = computed(() => {
  const name = user?.fullName || user?.username || user?.email || 'U';
  return name
    .split(' ')
    .slice(0, 2)
    .map((w) => w[0].toUpperCase())
    .join('');
});

async function handleLogout() {
  closeSheet();
  await disablePush();
  authService.logout();
  router.push('/login');
}
</script>

<style scoped>
.bottom-nav {
  display: none;
}

/* Mobile only */
@media (max-width: 767px) {
  .bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 150;
    display: flex;
    align-items: stretch;
    background: #1e2a3a;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    /* Respect iOS home-indicator safe area */
    padding-bottom: env(safe-area-inset-bottom, 0px);
  }
}

.bn-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  padding: 8px 2px;
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  font-size: 10px;
  font-weight: 500;
  text-decoration: none;
  font-family: inherit;
  transition: color 0.15s;
}

.bn-item.active {
  color: #60a5fa;
}

.bn-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

/* Backdrop */
.sheet-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  z-index: 200;
}

/* Bottom sheet */
.sheet {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 201;
  background: #1e2a3a;
  border-radius: 16px 16px 0 0;
  padding: 8px 16px calc(16px + env(safe-area-inset-bottom, 0px));
  display: flex;
  flex-direction: column;
  gap: 2px;
  max-height: 70vh;
  overflow-y: auto;
}

.sheet-handle {
  width: 40px;
  height: 4px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.2);
  margin: 4px auto 12px;
  flex-shrink: 0;
}

.sheet-title {
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  padding: 4px 12px 8px;
  letter-spacing: 0.3px;
}

.sheet-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 12px;
  border-radius: 8px;
  color: #cbd5e1;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
  text-align: left;
  width: 100%;
  transition: background 0.15s, color 0.15s;
}

.sheet-item:active {
  background: rgba(255, 255, 255, 0.07);
}

.sheet-item.active {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.sheet-item-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.sheet-logout {
  color: #f87171;
  margin-top: 4px;
}

/* User block in the More sheet */
.sheet-user {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 12px 14px;
  margin-bottom: 6px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.sheet-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #3b82f6;
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.sheet-user-details {
  display: flex;
  flex-direction: column;
  line-height: 1.3;
  min-width: 0;
}

.sheet-user-name {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sheet-user-meta {
  font-size: 12px;
  color: #64748b;
  text-transform: capitalize;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Transitions */
.sheet-enter-active,
.sheet-leave-active {
  transition: transform 0.25s ease;
}
.sheet-enter-from,
.sheet-leave-to {
  transform: translateY(100%);
}

.sheet-backdrop-enter-active,
.sheet-backdrop-leave-active {
  transition: opacity 0.25s ease;
}
.sheet-backdrop-enter-from,
.sheet-backdrop-leave-to {
  opacity: 0;
}
</style>
