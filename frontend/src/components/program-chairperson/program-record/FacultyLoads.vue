<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Faculty Loads</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableFacultyLoading />
    </div>
  </div>
</template>

<script>
import tableFacultyLoading from "./tables/table-faculty-loading.vue";
export default {
  name: "FacultyLoadingPage",
  components: {
    tableFacultyLoading,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
