<template>
  <div class="pwd-container">
    <p>Ganti password:</p>
    <input
      type="password"
      v-model="currentPassword"
      placeholder="Password saat ini"
      class="form-input"
    />
    <small v-if="wrongPwd" class="form-error">{{ wrongPwd }}</small>

    <input
      type="password"
      v-model="newPassword"
      placeholder="Password baru"
      class="form-input"
    />
    <small v-if="success" class="form-success">{{ success }}</small>

    <div class="button-row">
      <button @click="changePassword" class="btn btn-primary">
        Ubah Password
      </button>
      <button @click="cancel" class="btn btn-secondary">Batal</button>
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
.pwd-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-left: 27px;
  max-width: 420px;
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
  margin-top: -8px;
}

.form-success {
  color: #16a34a;
  font-size: 12px;
  margin-top: -8px;
}

.button-row {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
</style>
