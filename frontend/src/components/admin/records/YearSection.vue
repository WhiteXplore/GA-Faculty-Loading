<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">
        Class & Assigned Courses Overview
      </h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableYearSection />
    </div>
  </div>
</template>

<script>
import tableYearSection from "./tables/table-year-section.vue";
export default {
  name: "ClassesPage",
  components: {
    tableYearSection,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
