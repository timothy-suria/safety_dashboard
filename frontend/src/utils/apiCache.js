const TTL_MS = 5 * 60 * 1000; // 5 minutes

export function makeCache() {
  const store = new Map();
  return {
    get(key) {
      const e = store.get(key);
      if (!e) return null;
      if (Date.now() - e.at > TTL_MS) { store.delete(key); return null; }
      return e.data;
    },
    set(key, data) {
      store.set(key, { data, at: Date.now() });
    },
    del(key) {
      if (key !== undefined) store.delete(key);
      else store.clear();
    },
  };
}
