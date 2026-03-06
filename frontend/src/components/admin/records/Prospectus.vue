<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Prospectus</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableCurriculumOffers />
    </div>
  </div>
</template>

<script>
import tableCurriculumOffers from "./tables/table-prospectus.vue";
export default {
  name: "CurriculumOffersPage",
  components: {
    tableCurriculumOffers,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
