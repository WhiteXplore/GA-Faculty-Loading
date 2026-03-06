<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Faculty List</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <TableFacultySchedule />
    </div>
  </div>
</template>

<script>
import TableFacultySchedule from "./tables/table-faculty.vue";
export default {
  name: "FacultyuSchedulePage",
  components: {
    TableFacultySchedule,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
