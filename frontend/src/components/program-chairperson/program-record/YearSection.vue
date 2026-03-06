<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Year & Section</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <TableYearSection />
    </div>
  </div>
</template>

<script>
import TableYearSection from "../../program-chairperson/program-record/tables/table-year-section.vue";
export default {
  name: "RoomsPage",
  components: {
    TableYearSection,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
