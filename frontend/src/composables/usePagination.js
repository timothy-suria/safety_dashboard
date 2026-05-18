import { ref, computed, watch } from "vue";

export function usePagination(source, defaultPerPage = 10) {
  const currentPage = ref(1);
  const perPage = ref(defaultPerPage);

  const totalItems = computed(() => source.value.length);
  const totalPages = computed(() =>
    Math.max(1, Math.ceil(totalItems.value / perPage.value)),
  );

  const paginatedItems = computed(() => {
    const start = (currentPage.value - 1) * perPage.value;
    return source.value.slice(start, start + perPage.value);
  });

  function goToPage(page) {
    if (page >= 1 && page <= totalPages.value) currentPage.value = page;
  }

  function setPerPage(n) {
    perPage.value = n;
    currentPage.value = 1;
  }

  // Reset to page 1 when source (filtered list) changes
  watch(source, () => {
    currentPage.value = 1;
  });

  return { currentPage, perPage, totalItems, totalPages, paginatedItems, goToPage, setPerPage };
}
