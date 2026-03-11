<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Assigned Course</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <TableAssignedCourse />
    </div>
  </div>
</template>

<script>
import TableAssignedCourse from "../../program-chairperson/program-record/tables/table-assigned-course.vue";
export default {
  name: "RoomsPage",
  components: {
    TableAssignedCourse,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
