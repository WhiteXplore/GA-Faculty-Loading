<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">
        Curriculum Offers
      </h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableCurriculum />
    </div>
  </div>
</template>

<script>
import tableCurriculum from "./tables/table-curriculum.vue";
export default {
  name: "CurriculumPage",
  components: {
    tableCurriculum,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
