<template>
  <div v-if="visible" class="camera-modal-overlay" @click.self="close">
    <div class="camera-modal">
      <div class="camera-modal-header">
        <h3>Ambil Foto</h3>
        <button type="button" class="camera-close" @click="close">&times;</button>
      </div>
      <div class="camera-modal-body">
        <video v-show="!capturedUrl" ref="videoEl" autoplay playsinline muted></video>
        <img v-if="capturedUrl" :src="capturedUrl" alt="preview" class="camera-preview-img" />
        <canvas ref="canvasEl" style="display: none"></canvas>
        <p v-if="error" class="camera-error">{{ error }}</p>
      </div>
      <div class="camera-modal-actions">
        <template v-if="!capturedUrl">
          <button
            type="button"
            class="btn btn-primary"
            :disabled="!streamReady"
            @click="takePhoto"
          >
            Ambil Foto
          </button>
        </template>
        <template v-else>
          <button type="button" class="btn btn-secondary" @click="retake">Ulangi</button>
          <button type="button" class="btn btn-primary" @click="usePhoto">Gunakan Foto</button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";

const emit = defineEmits(["capture"]);

const visible = ref(false);
const videoEl = ref(null);
const canvasEl = ref(null);
const streamReady = ref(false);
const capturedUrl = ref("");
const error = ref("");
let stream = null;
let capturedBlob = null;

async function open() {
  visible.value = true;
  capturedUrl.value = "";
  capturedBlob = null;
  error.value = "";
  streamReady.value = false;

  if (!navigator.mediaDevices?.getUserMedia) {
    error.value = "Browser tidak mendukung akses kamera.";
    return;
  }

  await nextTick();
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
      audio: false,
    });
    if (videoEl.value) {
      videoEl.value.srcObject = stream;
      streamReady.value = true;
    }
  } catch (e) {
    error.value = "Tidak dapat mengakses kamera. Periksa izin kamera pada browser.";
  }
}

function stopStream() {
  if (stream) {
    stream.getTracks().forEach((t) => t.stop());
    stream = null;
  }
}

function close() {
  stopStream();
  visible.value = false;
  capturedUrl.value = "";
  capturedBlob = null;
}

function takePhoto() {
  const video = videoEl.value;
  const canvas = canvasEl.value;
  if (!video || !canvas) return;
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(
    (blob) => {
      capturedBlob = blob;
      capturedUrl.value = URL.createObjectURL(blob);
    },
    "image/jpeg",
    0.92,
  );
}

function retake() {
  capturedUrl.value = "";
  capturedBlob = null;
}

function usePhoto() {
  if (!capturedBlob) return;
  const file = new File([capturedBlob], `kamera-${Date.now()}.jpg`, {
    type: "image/jpeg",
  });
  emit("capture", file);
  close();
}

defineExpose({ open, close });
</script>

<style scoped>
.camera-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.camera-modal {
  background: #fff;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 480px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.camera-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.camera-modal-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.camera-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  color: #6b7280;
}

.camera-modal-body {
  background: #111827;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 240px;
}

.camera-modal-body video,
.camera-preview-img {
  width: 100%;
  max-height: 60vh;
  object-fit: contain;
  display: block;
}

.camera-error {
  color: #fca5a5;
  padding: 1.5rem;
  text-align: center;
  margin: 0;
}

.camera-modal-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  padding: 0.75rem 1rem;
  border-top: 1px solid #e5e7eb;
}
</style>
