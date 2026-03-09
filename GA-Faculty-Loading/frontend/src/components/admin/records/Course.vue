<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Courses</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableCourses />
    </div>
  </div>
</template>

<script>
import tableCourses from "./tables/table-courses.vue";
export default {
  name: "CoursesPage",
  components: {
    tableCourses,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
