<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-md">Exam Schules</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <TableExamSchedules />
    </div>
  </div>
</template>

<script>
import TableExamSchedules from "./tables/table-exam-schedules.vue";
export default {
  name: "ExamSchedulesPage",
  components: {
    TableExamSchedules,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
