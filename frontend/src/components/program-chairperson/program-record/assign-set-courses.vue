<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-md">Assign Courses</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableAssignSetCourses />
    </div>
  </div>
</template>

<script>
import tableAssignSetCourses from "./tables/table-assign-set-courses.vue";
export default {
  name: "AssignSetCoursesPage",
  components: {
    tableAssignSetCourses,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
