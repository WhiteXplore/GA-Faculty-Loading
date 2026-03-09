<template>
  <div class="px-2 mt-2">
    <!-- Header -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Room Utilities</h1>
    </div>

    <!-- Main Layout -->
    <div class="mt-3 flex">
      <!-- LEFT SIDE (Tabs List) -->
      <div class="w-60 bg-white border-r pr-1">
        <ul class="space-y-1">
          <li @click="activeTab = 'room'" :class="tabClass('room')">Room</li>
          <li @click="activeTab = 'building'" :class="tabClass('building')">
            Building
          </li>
          <li @click="activeTab = 'setup'" :class="tabClass('setup')">
            Setup Time
          </li>
          <li @click="activeTab = 'branch'" :class="tabClass('branch')">
            College Branch
          </li>
        </ul>
      </div>

      <!-- RIGHT SIDE (Table Content) -->
      <div class="flex-1 bg-white pl-2">
        <tableRooms v-if="activeTab === 'room'" />
        <tableBuildings v-if="activeTab === 'building'" />
        <tableCollegeBranch v-if="activeTab === 'branch'" />
        <tableBuildingAreas v-if="activeTab === 'setup'" />
      </div>
    </div>
  </div>
</template>

<script>
import tableRooms from "./tables/table-rooms.vue";
import tableBuildings from "./tables/table-building.vue";
import tableCollegeBranch from "./tables/table-college_branch.vue";
import tableBuildingAreas from "./tables/table-building-areas.vue";

export default {
  name: "UtilitiesPage",

  components: {
    tableRooms,
    tableBuildings,
    tableCollegeBranch,
    tableBuildingAreas,
  },

  data() {
    return {
      activeTab: "room",
    };
  },

  methods: {
    tabClass(tab) {
      return [
        "cursor-pointer px-3 py-2 rounded-md text-sm transition",
        this.activeTab === tab
          ? "bg-defaultGreen text-white"
          : "hover:bg-gray-100 text-gray-700",
      ];
    },
  },
};
</script>

<style scoped></style>
