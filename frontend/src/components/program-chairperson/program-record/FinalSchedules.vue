<template>
  <div class="px-4 mt-4">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="font-semibold tracking-wide text-sm px-1">
        Generated Schedules
      </h1>
    </div>

    <!-- Tabs -->
    <div class="mt-2 justify-between flex items-center">
      <div class="flex gap-1">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="activeTab = tab.value"
          :class="[
            'px-4 py-2 rounded-t-lg font-normal text-sm',
            activeTab === tab.value
              ? ' bg-defaultGreen text-white border border-gray-300 border-b-white shadow-sm'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
          ]"
        >
          {{ tab.label }}
        </button>
      </div>
      <div class="text-[13px] text-gray-700 px-6 flex justify-end">
        Pages / Generated Schedules
        <span class="text-gray-400 mx-1">/</span>
        <span class="font-semibold text-defaultGreen">{{ activeTab }}</span>
      </div>
    </div>

    <!-- Content Card -->
    <div class="bg-white border border-gray-300 border-t-0 shadow-sm mt-2">
      <tableFinalGenerated v-if="activeTab === 'Scheduled'" />
      <tableUnscheduledMeetings v-if="activeTab === 'Unscheduled'" />
    </div>
  </div>
</template>

<script>
import tableFinalGenerated from "./tables/table-final-generated.vue";
import tableUnscheduledMeetings from "./tables/table-unscheduled-meetings.vue";

export default {
  name: "FacultyLoadingPage",
  components: {
    tableFinalGenerated,
    tableUnscheduledMeetings,
  },
  data() {
    return {
      activeTab: "Scheduled",
      tabs: [
        { label: "Scheduled", value: "Scheduled" },
        { label: "Unscheduled", value: "Unscheduled" },
      ],
    };
  },
};
</script>

<style scoped>
/* Clean professional style */
</style>
