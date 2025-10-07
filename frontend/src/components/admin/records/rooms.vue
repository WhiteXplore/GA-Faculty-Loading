<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-md">Rooms Availability</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <TableRooms />
    </div>
  </div>
</template>

<script>
import TableRooms from "./tables/table-rooms.vue";
export default {
  name: "RoomsPage",
  components: {
    TableRooms,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
