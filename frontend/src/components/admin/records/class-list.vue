<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-md">Classes</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableClassList />
    </div>
  </div>
</template>

<script>
import tableClassList from "./tables/table-class-list.vue";
export default {
  name: "RoomsPage",
  components: {
    tableClassList,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
