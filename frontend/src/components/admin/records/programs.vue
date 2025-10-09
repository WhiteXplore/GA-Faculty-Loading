<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-md">Programs</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tablePrograms />
    </div>
  </div>
</template>

<script>
import tablePrograms from "./tables/table-programs.vue";
export default {
  name: "ProgramsPage",
  components: {
    tablePrograms,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>

