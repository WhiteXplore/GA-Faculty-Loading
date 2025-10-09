<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-md">Specializations</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableSpecializations />
    </div>
  </div>
</template>

<script>
import tableSpecializations from "./tables/table-specializations.vue";
export default {
  name: "SpecializationsPage",
  components: {
    tableSpecializations,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>

