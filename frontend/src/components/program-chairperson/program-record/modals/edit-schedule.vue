<template>
  <div
    v-if="show"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 z-50"
  >
    <div
      class="bg-white rounded-xl p-1.5 w-[80vw] relative max-h-[90vh] overflow-y-auto"
    >
      <div
        class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-lg flex justify-between items-center border-b shadow"
      >
        <div class="flex gap-1 items-center">
          <icon :name="'add-students'" />
          <h1 class="font-bold tracking-wide text-lg">Edit Schedule</h1>
        </div>
        <icon
          :name="'circle-close3'"
          @click="$emit('close')"
          class="cursor-pointer"
        />
      </div>
      <div class="grid grid-cols-2 gap-2 mt-2">
        <!-- ========================== -->
        <!-- EDITABLE TABLE -->
        <!-- ========================== -->
        <div
          class="mb-6 overflow-auto max-h-full rounded-lg border border-gray-200"
        >
          <table class="min-w-full divide-y divide-gray-200 text-sm">
            <thead class="bg-gray-100 text-gray-800">
              <tr>
                <th class="px-4 py-3 text-left font-semibold border">
                  Instructor
                </th>
                <th class="px-4 py-3 text-left font-semibold border">Room</th>
                <th class="px-4 py-3 text-left font-semibold border">Day</th>
                <th class="px-4 py-3 text-left font-semibold border">
                  Start Hour
                </th>
                <th class="px-4 py-3 text-left font-semibold border">
                  Duration
                </th>
              </tr>
            </thead>
            <tbody class="bg-white">
              <tr
                v-for="record in localData"
                :key="record.id"
                class="hover:bg-gray-50 transition-colors duration-200"
              >
                <td class="px-2 py-2 border">
                  <input
                    v-model="record.faculty_name"
                    class="w-full px-3 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-1 focus:ring-indigo-400 focus:border-indigo-400"
                  />
                </td>
                <td class="px-2 py-2 border">
                  <div class="flex flex-col space-y-2 w-full relative">
                    <input
                      v-model="record.searchRoomQuery"
                      type="text"
                      placeholder="Select room..."
                      class="px-3 py-2 border w-full border-gray-600 rounded-md text-md text-gray-800"
                      @focus="record.showRoomDropdown = true"
                      @input="record.room_id = null"
                    />

                    <div
                      v-if="
                        record.showRoomDropdown && filteredRooms(record).length
                      "
                      class="absolute top-[60px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
                      @mouseleave="record.showRoomDropdown = false"
                    >
                      <div
                        v-for="room in filteredRooms(record)"
                        :key="room.room_id"
                        class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                        @mousedown="selectRoom(record, room)"
                      >
                        {{ room.room_name }}
                      </div>
                    </div>
                  </div>
                </td>

                <td class="px-2 py-2 border">
                  <input
                    v-model="record.day"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-400 focus:border-indigo-400"
                  />
                </td>
                <td class="px-2 py-2 border">
                  <input
                    v-model.number="record.start_hour"
                    type="number"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-400 focus:border-indigo-400"
                  />
                </td>
                <td class="px-2 py-2 border">
                  <input
                    v-model.number="record.duration"
                    type="number"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-400 focus:border-indigo-400"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- ========================== -->
        <!-- DETAILED DRAG & DROP CALENDAR -->
        <!-- ========================== -->
        <div
          v-for="(records, instructor) in groupedSchedule"
          :key="instructor"
          class="bg-white flex flex-col mb-4"
        >
          <div
            class="flex items-center bg-gray-100 text-gray-800 border px-4 py-3 font-semibold text-sm rounded-t-lg"
          >
            <span>{{ instructor }}</span>
          </div>
          <div class="overflow-x-auto overflow-y-auto flex-1">
            <table class="w-full text-left border-collapse text-[11px]">
              <thead class="sticky top-0 bg-gray-100 z-10">
                <tr class="text-gray-700">
                  <th class="px-4 py-2 border border-gray-200 w-24 text-center">
                    Time
                  </th>
                  <th
                    v-for="day in days"
                    :key="day"
                    class="px-4 py-2 border border-gray-200 text-center w-28"
                  >
                    {{ day }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="slot in timeSlots"
                  :key="slot.start + slot.end"
                  class="odd:bg-white even:bg-gray-50"
                >
                  <!-- Time column -->
                  <td
                    class="px-4 py-4 border border-gray-200 font-medium text-center whitespace-nowrap"
                  >
                    {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                  </td>

                  <!-- Days columns -->
                  <td
                    v-for="day in days"
                    :key="day"
                    class="relative border border-gray-200 text-left align-top h-[40px] p-0 transition-all"
                    @dragover.prevent
                    @drop="onDrop($event, instructor, day, slot.start)"
                  >
                    <!-- Current instructor's blocks -->
                    <template
                      v-for="item in getScheduleForCell(slot, day, instructor)"
                      :key="item.id"
                    >
                      <div
                        v-if="isStartingSlot(item, slot)"
                        draggable="true"
                        @dragstart="onDragStart($event, item)"
                        :class="[
                          'absolute inset-x-1 border rounded-lg text-[11px] text-gray-800 shadow-sm overflow-hidden transition-all duration-200 whitespace-nowrap',
                          getTypeColor(item.type),
                          hasRoomConflict(item)
                            ? 'bg-red-300 border-red-500 text-red-900'
                            : '',
                        ]"
                        :style="{
                          top: getBlockTop(item, slot.start) + 'px',
                          height: getBlockHeight(item) + 'px',
                          width: 'calc(100% - 0.5rem)',
                          cursor: 'pointer',
                          zIndex: 10,
                        }"
                        :title="getConflictTooltip(item)"
                      >
                        <div class="p-2 leading-snug truncate">
                          <p class="font-semibold truncate">
                            {{ item.course_code }}
                          </p>
                          <p class="text-gray-600 truncate">
                            {{ item.room_name }}
                          </p>
                          <p class="text-gray-600 truncate">
                            {{ item.class_id }}
                          </p>
                          <button
                            v-if="hasRoomConflict(item)"
                            @click.stop="openConflictModal(item)"
                            class="mt-2 w-full text-center px-2 py-1 text-[10px] rounded bg-red-100 text-red-600 hover:bg-red-200 transition"
                          >
                            ⚠ View Conflict
                          </button>
                        </div>
                      </div>
                    </template>

                    <!-- Overlay other instructors' conflicting blocks -->
                    <template
                      v-for="conflict in getConflictsInCell(
                        slot,
                        day,
                        instructor
                      )"
                      :key="conflict.id + '-conflict'"
                    >
                      <div
                        class="absolute inset-x-1 border rounded-lg text-[11px] bg-red-200 border-red-500 text-red-900 shadow-sm p-1 whitespace-nowrap"
                        :style="{
                          top: getBlockTop(conflict, slot.start) + 'px',
                          height: getBlockHeight(conflict) + 'px',
                          width: 'calc(100% - 0.5rem)',
                          zIndex: 5,
                        }"
                        :title="`Conflict with: ${conflict.faculty_name} (${conflict.course_code})`"
                      >
                        <p class="truncate font-semibold">
                          {{ conflict.course_code }}
                        </p>
                        <p class="truncate">{{ conflict.faculty_name }}</p>
                        <p class="truncate">{{ conflict.room_name }}</p>
                      </div>
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ACTION BUTTONS -->
      <div class="flex justify-end gap-2 mt-4 px-2 py-1">
        <button
          @click="$emit('close')"
          class="px-3 py-1 rounded border hover:bg-gray-100"
          :disabled="saving"
        >
          Cancel
        </button>
        <button
          @click="saveEdit"
          class="px-3 py-1 rounded bg-blue-500 text-white hover:bg-blue-600"
          :disabled="saving || !isValid"
        >
          {{ saving ? "Saving..." : "Save" }}
        </button>
      </div>
    </div>
    <!-- CONFLICT MODAL -->
    <!-- MODERN CONFLICT MODAL -->
    <div
      v-if="conflictModalVisible"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50"
    >
      <div
        class="bg-white rounded-xl shadow-lg w-full max-w-lg relative max-h-[80vh] overflow-y-auto p-6"
      >
        <!-- Header -->
        <div class="flex justify-between items-center border-b pb-3 mb-4">
          <div class="flex gap-1">
            <icon
              name="exclamation-circle"
              class="text-red-900 w-7 p-1 rounded-full bg-red-200"
            />
            <h3 class="text-lg font-semibold text-gray-800">
              Schedule Conflicts
            </h3>
          </div>

          <button
            @click="closeConflictModal"
            class="text-gray-400 hover:text-gray-600 transition"
          >
            ✕
          </button>
        </div>

        <!-- Conflicts List -->
        <div class="space-y-3">
          <div
            v-for="conflict in conflictRecords"
            :key="conflict.id"
            class="bg-red-50 p-3 rounded-md shadow-sm"
          >
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Faculty:</span>
              {{ conflict.faculty_name }}
            </p>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Course:</span>
              {{ conflict.course_code }}
            </p>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Room:</span> {{ conflict.room_name }}
            </p>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Day:</span> {{ conflict.day }}
            </p>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Time:</span>
              {{ conflict.time_slot }}
            </p>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex justify-end mt-5">
          <button
            @click="closeConflictModal"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";
import icon from "@/assets/icon.vue";
export default {
  components: { icon },
  props: {
    show: Boolean,
    instructorData: { type: Array, default: () => [] },
  },
  data() {
    return {
      localData: [],
      saving: false,
      days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      timeSlots: Array.from({ length: 12 }, (_, i) => ({
        start: i + 8,
        end: i + 9,
      })),
      draggedRecord: null,
      hourHeight: 50,
      fullSchedules: [],
      conflictModalVisible: false,
      conflictRecords: [],
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rooms"]),

    groupedSchedule() {
      const groups = {};
      this.localData.forEach((rec) => {
        if (!groups[rec.faculty_name]) groups[rec.faculty_name] = [];
        groups[rec.faculty_name].push(rec);
      });
      return groups;
    },
    isValid() {
      return this.localData.every(
        (r) =>
          r.faculty_name &&
          r.day &&
          r.start_hour != null &&
          r.duration != null &&
          !this.hasRoomConflict(r)
      );
    },
  },
  watch: {
    instructorData: {
      immediate: true,
      handler(newVal) {
        this.localData = (Array.isArray(newVal) ? [...newVal] : []).map(
          (rec) => ({
            ...rec,
            searchRoomQuery: rec.room_name || "",
            showRoomDropdown: false,
          })
        );
      },
    },
  },
  methods: {
    ...mapActions(useFetchDataStore, ["fetchRooms"]),
    // Filter function
    filteredRooms(record) {
      if (!record.searchRoomQuery) return this.rooms;
      return this.rooms.filter((r) =>
        r.room_name.toLowerCase().includes(record.searchRoomQuery.toLowerCase())
      );
    },

    // Select a room from dropdown
    // When user selects a room from the dropdown
    selectRoom(record, room) {
      // Only update if room changed
      if (record.room_id !== room.room_id) {
        record.room_id = room.room_id;
        record.room_name = room.room_name;
        record.room_type = room.room_type;
      }
      record.searchRoomQuery = room.room_name; // for display only
      record.showRoomDropdown = false;
    },
    openConflictModal(record) {
      const conflicts = this.getConflictingRecords(record);
      if (!conflicts.length) return;

      this.conflictRecords = conflicts;
      this.conflictModalVisible = true;
    },

    closeConflictModal() {
      this.conflictModalVisible = false;
      this.conflictRecords = [];
    },
    getConflictsInCell(slot, day, instructor) {
      const cellRecords = this.getScheduleForCell(slot, day, instructor);
      const conflicts = cellRecords
        .map((r) => this.getConflictingRecords(r))
        .flat()
        .filter((r) => r.faculty_name !== instructor);
      return conflicts;
    },

    async loadData() {
      try {
        const fetchDataStore = useFetchDataStore();
        await fetchDataStore.fetchFinalSchedules();
        this.fullSchedules = Array.isArray(fetchDataStore.final_schedules)
          ? fetchDataStore.final_schedules
          : [];
      } catch (error) {
        console.error("Failed to load full schedules:", error);
        this.fullSchedules = [];
      }
    },

    getConflictingRecords(record) {
      const checkAgainst = [
        ...(this.fullSchedules || []),
        ...(this.localData || []),
      ];
      return checkAgainst.filter((r) => {
        if (r.id === record.id) return false;
        if (r.room_id !== record.room_id) return false;
        if (r.day !== record.day) return false;
        const rStart = Number(r.start_hour);
        const rEnd = rStart + Number(r.duration);
        const newStart = Number(record.start_hour);
        const newEnd = newStart + Number(record.duration);
        return Math.max(rStart, newStart) < Math.min(rEnd, newEnd);
      });
    },

    hasRoomConflict(record) {
      return this.getConflictingRecords(record).length > 0;
    },

    getConflictTooltip(record) {
      const conflicts = this.getConflictingRecords(record);
      if (!conflicts.length) return "";
      return conflicts
        .map(
          (c) =>
            `Conflict with: ${c.faculty_name} (${c.course_code}) in ${c.room_name}`
        )
        .join("\n");
    },

    formatTime(h) {
      const period = h >= 12 ? "PM" : "AM";
      const hour = h % 12 || 12;
      return `${hour}:00 ${period}`;
    },

    getScheduleForCell(slot, day, instructor) {
      return (this.localData || []).filter(
        (r) =>
          r.faculty_name === instructor &&
          r.day === day &&
          r.start_hour < slot.end &&
          r.start_hour + r.duration > slot.start
      );
    },

    isStartingSlot(item, slot) {
      return item.start_hour === slot.start;
    },

    getBlockTop(item, slotStart) {
      return (item.start_hour - slotStart) * this.hourHeight;
    },

    getBlockHeight(item) {
      return item.duration * this.hourHeight;
    },

    getTypeColor(type) {
      switch (type) {
        case "Lecture":
          return "bg-green-200 border-green-400";
        case "Laboratory":
          return "bg-blue-200 border-blue-400";
        default:
          return "bg-gray-200 border-gray-400";
      }
    },

    onDragStart(event, record) {
      this.draggedRecord = record;
      event.dataTransfer.effectAllowed = "move";
    },

    async onDrop(event, instructor, day, startHour) {
      if (!this.draggedRecord) return;

      const tempRecord = {
        ...this.draggedRecord,
        faculty_name: instructor,
        day,
        start_hour: startHour,
      };

      const conflicts = this.getConflictingRecords(tempRecord);
      if (conflicts.length > 1) {
        const conflictDetails = conflicts
          .map(
            (c) =>
              `Faculty: ${c.faculty_name}, Day: ${c.day}, Time: ${c.time_slot} `
          )
          .join("\n");

        toast.error(`Room conflict detected!\n${conflictDetails}`);
        return;
      }

      // Update local record
      Object.assign(this.draggedRecord, tempRecord);

      // Immediately save to backend
      try {
        await axios.patch(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${this.draggedRecord.id}`,
          this.draggedRecord
        );
        toast.success("Schedule updated successfully!");
      } catch (error) {
        toast.error("Failed to update schedule!");
        console.error(error);
      } finally {
        this.draggedRecord = null;
      }
    },
    async saveEdit() {
      this.saving = true;
      try {
        const payloads = this.localData.map((record) => {
          const payload = { ...record };
          // Remove frontend-only props
          delete payload.searchRoomQuery;
          delete payload.showRoomDropdown;
          return axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${record.id}`,
            payload
          );
        });

        await Promise.all(payloads);

        toast.success("Schedules saved!");
        this.$emit("saved", [...this.localData]);
        this.$emit("close");
      } catch (err) {
        console.error(err);
        toast.error("Failed to save schedules");
      } finally {
        this.saving = false;
      }
    },
  },
  mounted() {
    this.fetchRooms();
    this.loadData();
  },
};
</script>

<style scoped>
td {
  transition: background 0.2s;
  position: relative;
}
</style>
