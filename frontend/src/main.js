import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router/routes";

const app = createApp(App);
app.use(router);
app.mount("#app");

if ("serviceWorker" in navigator && import.meta.env.PROD) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  });
}
