<template>
  <div class="settings-page">
    <div class="page-header">
      <div>
        <h2>Pengaturan</h2>
        <p>Kelola preferensi akun Anda.</p>
      </div>
    </div>

    <div class="settings-card">
      <div class="card-section-title">Keamanan Akun</div>
      <p class="card-section-sub">Perbarui password Anda secara berkala untuk menjaga keamanan akun.</p>

      <div class="form-group">
        <label class="form-label">Password Saat Ini</label>
        <input
          type="password"
          v-model="currentPassword"
          placeholder="Masukkan password saat ini"
          class="form-input"
        />
        <small v-if="wrongPwd" class="form-error">{{ wrongPwd }}</small>
      </div>

      <div class="form-group">
        <label class="form-label">Password Baru</label>
        <input
          type="password"
          v-model="newPassword"
          placeholder="Minimal 6 karakter"
          class="form-input"
        />
        <small v-if="success" class="form-success">{{ success }}</small>
      </div>

      <div class="button-row">
        <button @click="changePassword" class="btn-primary">Ubah Password</button>
        <button @click="cancel" class="btn-secondary">Batal</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { authService } from "@/services/authService";

const currentPassword = ref("");
const newPassword = ref("");
const wrongPwd = ref("");
const success = ref("");

async function changePassword() {
  wrongPwd.value = "";
  success.value = "";

  if (!currentPassword.value || !newPassword.value) {
    wrongPwd.value = "Silakan masukkan password saat ini dan password baru.";
    return;
  }

  if (newPassword.value.length < 6) {
    wrongPwd.value = "Password baru harus terdiri dari minimal 6 karakter.";
    return;
  }

  try {
    await authService.changePassword(currentPassword.value, newPassword.value);
    success.value = "Password berhasil diubah!";
    currentPassword.value = "";
    newPassword.value = "";
  } catch (error) {
    wrongPwd.value = error.message || "Gagal mengubah password.";
  }
}

function cancel() {
  currentPassword.value = "";
  newPassword.value = "";
  wrongPwd.value = "";
  success.value = "";
}
</script>

<style scoped>
.settings-page {
  padding: 28px 32px;
}

@media (max-width: 1024px) { .settings-page { padding: 20px 20px; } }
@media (max-width: 640px)  { .settings-page { padding: 16px 14px; } }

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 4px;
}

.page-header p {
  font-size: 13px;
  color: #64748b;
  margin: 0;
}

.settings-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 28px 28px 24px;
  max-width: 480px;
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 640px) {
  .settings-card {
    padding: 20px 16px 18px;
    max-width: 100%;
  }
}

.card-section-title {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.card-section-sub {
  font-size: 13px;
  color: #64748b;
  margin: 0 0 20px;
  line-height: 1.5;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.form-input {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #1e293b;
  background-color: #fff;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.15s, box-shadow 0.15s;
  font-family: inherit;
}

.form-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12);
}

.form-error {
  color: #dc2626;
  font-size: 12px;
}

.form-success {
  color: #16a34a;
  font-size: 12px;
}

.button-row {
  display: flex;
  gap: 10px;
  margin-top: 8px;
  flex-wrap: wrap;
}

@media (max-width: 400px) {
  .button-row { flex-direction: column; }
  .button-row button { width: 100%; }
}

.btn-primary {
  padding: 9px 20px;
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-primary:hover { background: #2563eb; }

.btn-secondary {
  padding: 9px 18px;
  background: #f1f5f9;
  color: #374151;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-secondary:hover { background: #e2e8f0; }
</style>
