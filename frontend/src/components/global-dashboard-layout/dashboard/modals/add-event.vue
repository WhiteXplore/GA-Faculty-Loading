<template>
  <div
    class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50"
  >
    <div class="bg-white w-full max-w-xl rounded-xl shadow-2xl p-6 space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <h2 class="text-lg font-semibold text-gray-800">Add Event</h2>
        <button
          @click="$emit('cancel')"
          class="text-gray-400 hover:text-gray-600 transition"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Title Input -->
      <input
        v-model="newEventTitle"
        type="text"
        placeholder="Add title"
        class="w-full text-xl font-semibold bg-transparent border-b border-gray-300 focus:border-blue-600 focus:outline-none px-1 py-2 text-gray-800 placeholder-gray-400"
      />

      <!-- Date & Time Grid -->
      <div class="grid grid-cols-2 gap-6">
        <!-- Start -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-500">Start</label>
          <input
            type="date"
            v-model="startDate"
            class="w-full bg-white border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
          <input
            type="time"
            v-model="timeStart"
            :disabled="isAllDay"
            class="w-full bg-white border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
        </div>

        <!-- End -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-500">End</label>
          <input
            type="date"
            v-model="endDate"
            class="w-full bg-white border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
          <input
            type="time"
            v-model="timeEnd"
            :disabled="isAllDay"
            class="w-full bg-white border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
        </div>
      </div>

      <!-- All Day Checkbox -->
      <div class="flex items-center gap-2">
        <input
          type="checkbox"
          id="allDay"
          v-model="isAllDay"
          class="h-4 w-4 text-blue-600"
        />
        <label for="allDay" class="text-sm text-gray-700">All day</label>
      </div>
      <!-- Institute & Program Selection -->
      <div class="grid grid-cols-2 gap-6">
        <!-- Institute -->
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1"
            >Institute</label
          >
          <select
            v-model="selectedInstituteId"
            @change="filterPrograms"
            class="w-full bg-white border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
          >
            <option value="" disabled>Select Institute</option>
            <option
              v-for="inst in dataStore.institutes"
              :key="inst.institute_id"
              :value="inst.institute_id"
            >
              {{ inst.institute_name }}
            </option>
          </select>
        </div>

        <!-- Program -->
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1"
            >Program</label
          >
          <select
            v-model="selectedProgramId"
            :disabled="!filteredPrograms.length"
            class="w-full bg-white border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
          >
            <option value="" disabled>Select Program</option>
            <option
              v-for="prog in filteredPrograms"
              :key="prog.program_id"
              :value="prog.program_id"
            >
              {{ prog.program_name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-end gap-3 pt-4">
        <button
          @click="$emit('cancel')"
          class="text-sm text-gray-600 hover:text-black px-4 py-2 rounded-md transition"
        >
          Cancel
        </button>
        <button
          @click="submitEvent"
          class="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-md transition"
        >
          Save
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import dayjs from "dayjs";
import { useFetchDataStore } from "../../../../store/fetch-data-store.js";
import { onMounted } from "vue";

export default {
  name: "AddEventModal",
  props: {
    selectedDate: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      newEventTitle: "",
      startDate: "",
      endDate: "",
      timeStart: "09:30",
      timeEnd: "10:30",
      isAllDay: false,
      selectedInstituteId: "",
      selectedProgramId: "",
      filteredPrograms: [],
    };
  },
  setup() {
    const dataStore = useFetchDataStore();
    onMounted(() => {
      dataStore.fetchInstitutes();
      dataStore.fetchPrograms();
    });
    return { dataStore };
  },
  mounted() {
    const dateStr = this.selectedDate.format("YYYY-MM-DD");
    this.startDate = dateStr;
    this.endDate = dateStr;
  },
  methods: {
    filterPrograms() {
      const id = this.selectedInstituteId;
      this.filteredPrograms = this.dataStore.programs.filter(
        (p) => p.institute_id === parseInt(id)
      );
      this.selectedProgramId = "";
    },
    submitEvent() {
      if (!this.newEventTitle.trim()) {
        alert("Please enter an event title.");
        return;
      }

      if (dayjs(this.endDate).isBefore(this.startDate)) {
        alert("End date cannot be before start date.");
        return;
      }

      if (!this.selectedInstituteId || !this.selectedProgramId) {
        alert("Please select both institute and program.");
        return;
      }

      this.$emit("add", {
        title: this.newEventTitle,
        startDate: this.startDate,
        endDate: this.endDate,
        timeStart: this.isAllDay ? null : this.timeStart,
        timeEnd: this.isAllDay ? null : this.timeEnd,
        isAllDay: this.isAllDay,
        program_id: this.selectedProgramId, // ✅ match backend
      });

      // Reset form
      const dateStr = this.selectedDate.format("YYYY-MM-DD");
      this.newEventTitle = "";
      this.startDate = dateStr;
      this.endDate = dateStr;
      this.timeStart = "09:30";
      this.timeEnd = "10:30";
      this.isAllDay = false;
      this.selectedInstituteId = "";
      this.selectedProgramId = "";
      this.filteredPrograms = [];
    },
  },
};
</script>
