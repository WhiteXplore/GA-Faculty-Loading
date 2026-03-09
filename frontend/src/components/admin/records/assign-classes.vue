<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-md">Assign Classes</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableAssignClasses />
    </div>
  </div>
</template>

<script>
import tableAssignClasses from "./tables/table-assign-classes.vue";
export default {
  name: "AssignClassesPage",
  components: {
    tableAssignClasses,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
