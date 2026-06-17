const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const GRAPHQL_URL = `${API_BASE}/graphql`;

async function gql(query, variables = {}) {
  const token = localStorage.getItem("token");
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(GRAPHQL_URL, {
    method: "POST",
    headers,
    body: JSON.stringify({ query, variables }),
  });

  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  const { data, errors } = await res.json();
  if (errors?.length) throw new Error(errors[0].message);
  return data;
}

export const authService = {
  async register(email, password) {
    const data = await gql(
      `mutation Register($email: String!, $password: String!) {
        register(email: $email, password: $password) {
          success message token
          user { id email fullName username role roleId roleLevel businessUnit plant businessUnitId plantId departmentId department }
        }
      }`,
      { email, password },
    );
    const result = data.register;
    if (!result.success) throw new Error(result.message);
    localStorage.setItem("token", result.token);
    localStorage.setItem("user", JSON.stringify(result.user));
    return result;
  },

  async login(identifier, password) {
    const data = await gql(
      `mutation Login($identifier: String!, $password: String!) {
        login(identifier: $identifier, password: $password) {
          success message token
          user { id email fullName username role roleId roleLevel businessUnit plant businessUnitId plantId departmentId department }
        }
      }`,
      { identifier, password },
    );
    const result = data.login;
    if (!result.success) throw new Error(result.message);
    localStorage.setItem("token", result.token);
    localStorage.setItem("user", JSON.stringify(result.user));
    return result;
  },

  getCurrentUser() {
    const raw = localStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  },

  getRoleLevel() {
    const user = this.getCurrentUser();
    return user?.roleLevel ?? 999;
  },

  isAdmin() {
    return this.getRoleLevel() === 0;
  },

  canAccessMasterData() {
    return this.getRoleLevel() <= 3;
  },

  logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  },

  getTokenExpiry() {
    const token = localStorage.getItem("token");
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      return payload.exp ? payload.exp * 1000 : null;
    } catch {
      return null;
    }
  },

  isTokenExpired() {
    const expiry = this.getTokenExpiry();
    if (!expiry) return true;
    return Date.now() >= expiry;
  },

  async changePassword(currentPassword, newPassword) {
    const data = await gql(
      `mutation ChangePassword($currentPassword: String!, $newPassword: String!) {
      changePassword(currentPassword: $currentPassword, newPassword: $newPassword) {
        success
        message
      }
    }`,
      { currentPassword, newPassword },
    );

    const result = data.changePassword;
    if (!result.success) throw new Error(result.message);
    return result;
  },
};
