<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Institutes</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <TableInstitutes />
    </div>
  </div>
</template>

<script>
import TableInstitutes from "./tables/table-institutes.vue";
export default {
  name: "FacultyuSchedulePage",
  components: {
    TableInstitutes,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
