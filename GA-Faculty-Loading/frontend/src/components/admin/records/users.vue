<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">User Accounts</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableUsers />
    </div>
  </div>
</template>

<script>
import tableUsers from "./tables/table-users.vue";
export default {
  name: "TimePage",
  components: {
    tableUsers,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
