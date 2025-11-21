<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-md">Rooms Availability</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableRooms />
    </div>
  </div>
</template>

<script>
import tableRooms from "./tables/table-rooms.vue";
export default {
  name: "SchoolYearPage",
  components: {
    tableRooms,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
