<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">School Years</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableSchoolYear />
    </div>
  </div>
</template>

<script>
import tableSchoolYear from "./tables/table-school-year.vue";
export default {
  name: "SchoolYearPage",
  components: {
    tableSchoolYear,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
