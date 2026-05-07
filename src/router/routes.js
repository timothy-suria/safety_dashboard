import { createRouter, createWebHistory } from "vue-router";
import Login from "../login/Login.vue";
import Register from "../login/Register.vue";
import Dashboard from "../dashboard/Dashboard.vue";
import SafetyModules from "../dashboard/views/SafetyModules.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", name: "Login", component: Login },
  { path: "/register", name: "Register", component: Register },
  {
    path: "/dashboard",
    component: Dashboard,
    children: [
      { path: "", redirect: "/dashboard/modules" },
      { path: "modules", name: "SafetyModules", component: SafetyModules },
      { path: "reports", name: "Reports", component: { template: "<div style='padding:32px'><h2>Reports coming soon</h2></div>" } },
      { path: "settings", name: "Settings", component: { template: "<div style='padding:32px'><h2>Settings coming soon</h2></div>" } },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
