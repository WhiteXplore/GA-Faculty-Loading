<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">
        Faculty Expertise Overview
      </h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableFacultyExpertise />
    </div>
  </div>
</template>

<script>
import tableFacultyExpertise from "./tables/table-faculty-expertise.vue";
export default {
  name: "FacultyLoadingPage",
  components: {
    tableFacultyExpertise,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
