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

export const masterDataService = {
  // ── Business Unit ─────────────────────────────────────────────────────

  async listBusinessUnits() {
    const data = await gql(`
      query {
        businessUnits {
          id name code description isActive createdAt
        }
      }
    `);
    return data.businessUnits;
  },

  async createBusinessUnit(input) {
    const data = await gql(
      `mutation CreateBU($name: String!, $code: String!, $description: String, $isActive: Boolean) {
        createBusinessUnit(name: $name, code: $code, description: $description, isActive: $isActive) {
          success message
          businessUnit { id name code description isActive createdAt }
        }
      }`,
      input,
    );
    const r = data.createBusinessUnit;
    if (!r.success) throw new Error(r.message);
    return r;
  },

  async updateBusinessUnit(id, input) {
    const data = await gql(
      `mutation UpdateBU($id: Int!, $name: String, $code: String, $description: String, $isActive: Boolean) {
        updateBusinessUnit(id: $id, name: $name, code: $code, description: $description, isActive: $isActive) {
          success message
          businessUnit { id name code description isActive createdAt }
        }
      }`,
      { id, ...input },
    );
    const r = data.updateBusinessUnit;
    if (!r.success) throw new Error(r.message);
    return r;
  },

  async deleteBusinessUnit(id) {
    const data = await gql(
      `mutation DeleteBU($id: Int!) {
        deleteBusinessUnit(id: $id) { success message }
      }`,
      { id },
    );
    const r = data.deleteBusinessUnit;
    if (!r.success) throw new Error(r.message);
    return r;
  },

  // ── Plant ─────────────────────────────────────────────────────────────

  async listPlants(businessUnitId = null) {
    const data = await gql(
      `query Plants($businessUnitId: Int) {
        plants(businessUnitId: $businessUnitId) {
          id name code businessUnitId location isActive createdAt
        }
      }`,
      { businessUnitId },
    );
    return data.plants;
  },

  async createPlant(input) {
    const data = await gql(
      `mutation CreatePlant($name: String!, $code: String!, $businessUnitId: Int!, $location: String, $isActive: Boolean) {
        createPlant(name: $name, code: $code, businessUnitId: $businessUnitId, location: $location, isActive: $isActive) {
          success message
          plant { id name code businessUnitId location isActive createdAt }
        }
      }`,
      input,
    );
    const r = data.createPlant;
    if (!r.success) throw new Error(r.message);
    return r;
  },

  async updatePlant(id, input) {
    const data = await gql(
      `mutation UpdatePlant($id: Int!, $name: String, $code: String, $businessUnitId: Int, $location: String, $isActive: Boolean) {
        updatePlant(id: $id, name: $name, code: $code, businessUnitId: $businessUnitId, location: $location, isActive: $isActive) {
          success message
          plant { id name code businessUnitId location isActive createdAt }
        }
      }`,
      { id, ...input },
    );
    const r = data.updatePlant;
    if (!r.success) throw new Error(r.message);
    return r;
  },

  async deletePlant(id) {
    const data = await gql(
      `mutation DeletePlant($id: Int!) {
        deletePlant(id: $id) { success message }
      }`,
      { id },
    );
    const r = data.deletePlant;
    if (!r.success) throw new Error(r.message);
    return r;
  },
};
