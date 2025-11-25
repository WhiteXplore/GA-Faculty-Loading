<template>
  <div class="flex flex-col gap-4 h-[87vh]">
    <!-- Top Controls -->
    <div class="flex flex-wrap justify-between items-center mb-4 gap-3">
      <div class="text-sm text-gray-600 mt-2 font-medium">
        Pages / Faculty Loads
      </div>

      <div class="flex gap-3 flex-wrap">
        <!-- Toggle View Button -->
        <button
          @click="showFacultyTable = !showFacultyTable"
          class="group flex items-center gap-2 px-4 py-2 border border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white rounded-xl shadow-sm transition"
        >
          <div
            class="p-1 bg-blue-100 rounded-full flex items-center justify-center group-hover:bg-white transition"
          >
            <icon
              name="users"
              class="w-4 h-4 text-blue-600 group-hover:text-blue-600"
            />
          </div>
          <span class="font-medium text-sm">
            {{ showFacultyTable ? "View Cards" : "View Faculty" }}
          </span>
        </button>

        <!-- Auto Generation -->
        <button
          @click="generateSchedule"
          class="flex items-center gap-2 px-4 py-2 bg-defaultGreen text-white rounded-xl shadow-sm hover:shadow-md border border-defaultGreen hover:bg-white hover:text-defaultGreen transition-all duration-300"
        >
          <div
            class="flex items-center justify-center w-5 h-5 bg-white rounded-full transition-colors duration-300"
          >
            <icon name="arrow-path" class="w-4 h-4 text-defaultGreen" />
          </div>
          <span class="font-medium text-sm">Auto Generation</span>
        </button>

        <!-- Save Schedule -->
        <button
          @click="saveScheduled"
          class="flex items-center gap-2 px-4 py-2 bg-defaultGreen text-white rounded-xl shadow-sm hover:shadow-md border border-defaultGreen hover:bg-white hover:text-defaultGreen transition-all duration-300"
        >
          <div
            class="flex items-center justify-center w-5 h-5 bg-white rounded-full transition-colors duration-300"
          >
            <icon name="circle-check" class="w-4 h-4 text-defaultGreen" />
          </div>
          <span class="font-medium text-sm">Save this schedule</span>
        </button>
      </div>
    </div>

    <div class="flex flex-wrap items-center gap-4 mb-2">
      <!-- Back Button -->
      <button
        v-if="
          !showFacultyTable && Object.keys(filteredGroupedSchedule).length === 1
        "
        @click="backToFacultyTable"
        class="flex items-center gap-2 px-4 py-2 border border-gray-400 rounded-xl shadow-sm hover:bg-gray-100 transition"
      >
        <icon name="arrow-left" class="w-4 h-4" />
        <span class="font-medium text-sm">Back to Table</span>
      </button>

      <!-- Filters (pushed to the end) -->
      <div class="flex flex-wrap items-center gap-4 ml-auto">
        <!-- Institute Filter -->
        <div class="flex items-center gap-2">
          <select
            v-model="selectedInstituteId"
            class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-green-500 focus:border-green-500 w-[180px]"
          >
            <option value="">All Institutes</option>
            <option
              v-for="institute in uniqueInstitutes"
              :key="institute.id"
              :value="institute.id"
            >
              {{ institute.name }}
            </option>
          </select>
        </div>

        <!-- Program Filter -->
        <div class="flex items-center gap-2">
          <select
            v-model="selectedProgramId"
            :disabled="!selectedInstituteId"
            class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:bg-gray-100 disabled:cursor-not-allowed w-[180px]"
          >
            <option value="">All Programs</option>
            <option
              v-for="program in filteredPrograms"
              :key="program.id"
              :value="program.id"
            >
              {{ program.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Scrollable Content -->
    <div class="flex-1 overflow-y-auto">
      <!-- Faculty Table -->
      <div
        v-if="showFacultyTable"
        class="bg-white rounded-xl border p-5 shadow-sm h-full overflow-auto"
      >
        <div class="overflow-x-auto max-h-[100%]">
          <table
            class="min-w-full text-sm text-gray-700 border-collapse table-auto"
          >
            <thead class="bg-defaultGreen text-white sticky top-0 z-10">
              <tr>
                <th class="px-5 py-3 text-left font-semibold whitespace-nowrap">
                  Faculty Name
                </th>
                <th
                  class="px-5 py-3 text-center font-semibold w-[150px] whitespace-nowrap"
                >
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(slots, instructor) in paginatedFaculty"
                :key="instructor"
                class="hover:bg-green-50 border-t transition-colors"
              >
                <td
                  class="px-5 py-3 font-medium text-gray-800 whitespace-nowrap"
                >
                  {{ instructor }}
                </td>
                <td class="px-5 py-3 text-center">
                  <button
                    @click="viewFacultySchedule(instructor)"
                    class="flex items-center justify-center gap-1 mx-auto px-3 py-1.5 border border-blue-400 text-blue-700 hover:bg-blue-100 rounded-lg text-sm font-medium transition"
                  >
                    <icon name="eye" class="w-4 h-4" /> View
                  </button>
                </td>
              </tr>
              <tr
                v-if="!Object.keys(filteredGroupedSchedule).length"
                class="text-center bg-gray-50"
              >
                <td colspan="2" class="py-5 text-gray-500">
                  No faculty found.
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div
            v-if="totalPages > 1"
            class="flex justify-center items-center gap-3 mt-4 text-sm"
          >
            <button
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-3 py-1.5 border rounded-lg hover:bg-gray-100 disabled:opacity-50"
            >
              Prev
            </button>
            <span class="font-medium"
              >Page {{ currentPage }} of {{ totalPages }}</span
            >
            <button
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="px-3 py-1.5 border rounded-lg hover:bg-gray-100 disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      </div>

      <!-- Faculty Cards -->
      <div
        v-else
        :class="[
          'gap-6 overflow-y-auto pr-2 grid',
          Object.keys(filteredGroupedSchedule).length === 1
            ? 'grid-cols-1'
            : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
        ]"
        style="height: 100%"
      >
        <div
          v-for="(records, instructor) in filteredGroupedSchedule"
          :key="instructor"
          class="bg-white rounded-xl border flex flex-col"
        >
          <!-- Header -->
          <div
            class="bg-gray-700 text-white text-center py-3 font-semibold text-sm"
          >
            {{ instructor }}
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
                  <td
                    class="px-4 py-4 border border-gray-200 font-medium text-center whitespace-nowrap"
                  >
                    {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                  </td>
                  <td
                    v-for="day in days"
                    :key="day"
                    class="relative border border-gray-200 text-left align-top h-[60px] p-0"
                  >
                    <template
                      v-for="item in getScheduleForCell(slot, day, instructor)"
                      :key="item.course_name + item.start_hour + item.room_name"
                    >
                      <div
                        v-if="isStartingSlot(item, slot)"
                        :class="[
                          'absolute inset-x-1 border rounded-lg text-[11px] text-gray-800 shadow-sm overflow-hidden transition-all duration-200 whitespace-nowrap',
                          getTypeColor(item.type),
                        ]"
                        :style="{
                          top: getBlockTop() + 'px',
                          height: getBlockHeight(item) + 'px',
                          width: 'calc(100% - 0.5rem)',
                        }"
                      >
                        <div class="p-2 leading-snug truncate">
                          <p class="font-semibold truncate">
                            {{ item.course_code }}
                          </p>
                          <p class="text-gray-600 truncate">
                            {{ item.room_name }}
                          </p>
                          <button
                            v-if="item.conflict"
                            @click="openConflictModal(item)"
                            class="mt-2 w-full text-center px-2 py-1 text-[10px] rounded bg-red-100 text-red-600 hover:bg-red-200 transition"
                          >
                            ⚠ View Conflict
                          </button>
                        </div>
                      </div>
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div
      v-if="loading"
      class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50"
    >
      <div class="relative flex items-center justify-center">
        <div
          class="absolute w-52 h-44 bg-gradient-to-r from-green-400/30 to-emerald-500/30 rounded-3xl animate-ping"
        ></div>
        <div
          class="relative flex flex-col items-center justify-center bg-white/90 backdrop-blur-md p-8 rounded-3xl shadow-2xl border border-white/30"
        >
          <div class="relative mb-4">
            <div
              class="w-12 h-12 border-4 border-green-400 border-t-transparent rounded-full animate-spin"
            ></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-green-600 text-sm font-semibold"
                >{{ Math.floor(progress) }}%</span
              >
            </div>
          </div>
          <div class="text-gray-700 font-semibold text-[15px] tracking-wide">
            Generating Schedule...
          </div>
          <div class="text-xs text-gray-500 mt-1">
            Please wait while we finalize your data.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import icon from "@/assets/icon.vue";
import { useFetchDataStore } from "@/store/fetch-data-store";

export default {
  name: "FacultySchedule",
  components: { icon },

  data() {
    return {
      user: {},
      schedule: [],
      groupedSchedule: {},
      filteredGroupedSchedule: {},
      loading: false,
      error: null,
      showFacultyTable: false,
      selectedInstructor: null,
      scheduleGenerated: false,
      selectedInstituteId: "",
      selectedProgramId: "",
      days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],

      // 8 AM to 5 PM
      timeSlots: Array.from({ length: 12 }, (_, i) => ({
        start: 8 + i,
        end: 9 + i,
      })),

      progress: 0,
      progressInterval: null,
      showConflictModal: false,
      selectedConflict: {},
      currentPage: 1,
      itemsPerPage: 10,
      timeSlotHeight: 60,
    };
  },

  computed: {
    // Map institute IDs to their names
    uniqueInstitutes() {
      const store = useFetchDataStore();
      const institutes = store.institutes || [];
      return Array.from(new Set(this.schedule.map((s) => s.institute_id))).map(
        (id) => {
          const inst = institutes.find((i) => i.institute_id === id);
          return inst
            ? { id, name: inst.institute_name }
            : { id, name: `Institute ${id}` };
        }
      );
    },

    // Map program IDs to their names (filtered by selectedInstituteId if any)
    filteredPrograms() {
      const store = useFetchDataStore();
      const programs = store.programs || [];
      let programIds;

      if (!this.selectedInstituteId) {
        programIds = Array.from(
          new Set(this.schedule.map((s) => s.program_id))
        );
      } else {
        programIds = Array.from(
          new Set(
            this.schedule
              .filter((s) => s.institute_id == this.selectedInstituteId)
              .map((s) => s.program_id)
          )
        );
      }

      return programIds.map((id) => {
        const prog = programs.find((p) => p.program_id === id);
        return prog
          ? { id, name: prog.program_name }
          : { id, name: `Program ${id}` };
      });
    },

    paginatedFaculty() {
      const allFaculty = Object.entries(this.filteredGroupedSchedule);
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return Object.fromEntries(allFaculty.slice(start, end));
    },

    totalPages() {
      return Math.ceil(
        Object.keys(this.filteredGroupedSchedule).length / this.itemsPerPage
      );
    },
  },

  watch: {
    selectedInstituteId() {
      this.filterSchedules();
      this.selectedProgramId = "";
    },
    selectedProgramId() {
      this.filterSchedules();
    },
  },

  methods: {
    async loadFetchData() {
      const store = useFetchDataStore();
      await store.fetchPrograms();
      await store.fetchInstitutes(); // fetch institutes for dropdown

      // After institutes are fetched, log matching institute names
      this.logInstituteNames();
    },

    logInstituteNames() {
      const store = useFetchDataStore();
      const institutes = store.institutes || [];
      if (!this.schedule || !institutes.length) return;

      this.schedule.forEach((s) => {
        const inst = institutes.find((i) => i.institute_id === s.institute_id);
        if (inst);
      });
    },

    backToFacultyTable() {
      this.filteredGroupedSchedule = this.groupedSchedule; // reset to all faculty
      this.showFacultyTable = true; // show the table
      this.currentPage = 1; // optional: go to first page
    },

    normalizeHour(hour) {
      hour = Number(hour);
      if (Number.isNaN(hour)) return hour;
      return hour <= 7 ? hour + 12 : hour;
    },

    isStartingSlot(item, slot) {
      return this.normalizeHour(item.start_hour) === slot.start;
    },

    checkConflicts() {
      const conflicts = [];
      const allSchedules = this.schedule;

      for (let i = 0; i < allSchedules.length; i++) {
        for (let j = i + 1; j < allSchedules.length; j++) {
          const a = allSchedules[i];
          const b = allSchedules[j];

          const sameDay = a.day === b.day;
          const sameRoom = a.room_name === b.room_name;
          const sameCourse = a.course_code === b.course_code;

          const aStart = this.normalizeHour(a.start_hour);
          const aEnd = aStart + Number(a.duration);

          const bStart = this.normalizeHour(b.start_hour);
          const bEnd = bStart + Number(b.duration);

          const overlap = aEnd > bStart && aStart < bEnd;

          if (sameDay && sameRoom && sameCourse && overlap) {
            conflicts.push({ a, b });
          }
        }
      }
      return conflicts;
    },

    formatTime(hour) {
      const h = hour % 12 === 0 ? 12 : hour % 12;
      const period = hour >= 12 ? "PM" : "AM";
      return `${h}:00 ${period}`;
    },

    filterSchedules() {
      let filtered = { ...this.groupedSchedule };

      if (this.selectedInstituteId)
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some((s) => s.institute_id == this.selectedInstituteId)
          )
        );

      if (this.selectedProgramId)
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some((s) => s.program_id == this.selectedProgramId)
          )
        );

      this.filteredGroupedSchedule = filtered;
      this.changePage(1);
    },

    getScheduleForCell(slot, day, instructor) {
      const schedules = this.filteredGroupedSchedule[instructor] || [];

      return schedules.filter((item) => {
        if (item.day !== day) return false;

        const start = this.normalizeHour(item.start_hour);
        const end = start + Number(item.duration);

        return end > slot.start && start < slot.end;
      });
    },

    getBlockHeight(item) {
      return Math.max(1, Number(item.duration)) * this.timeSlotHeight - 1;
    },

    getBlockTop() {
      return 0;
    },

    getTypeColor(room_type) {
      if (!room_type) return "bg-green-100 border-green-400";

      const normalized = room_type.toLowerCase();
      if (normalized === "laboratory" || normalized === "lab") {
        return "bg-blue-100 border-blue-400";
      }
      return "bg-green-100 border-green-400";
    },

    viewFacultySchedule(instructor) {
      this.filteredGroupedSchedule = {
        [instructor]: this.groupedSchedule[instructor],
      };
      this.showFacultyTable = false;
    },

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) this.currentPage = page;
    },

    openConflictModal(item) {
      this.selectedConflict = item;
      this.showConflictModal = true;
    },
    closeConflictModal() {
      this.showConflictModal = false;
      this.selectedConflict = {};
    },

    async fetchUser() {
      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/auth/me`,
          { withCredentials: true }
        );
        this.user = res.data || {};
      } catch {
        this.user = {};
      }
    },

    async fetchSchedule() {
      this.loading = true;
      this.progress = 0;
      this.progressInterval = setInterval(() => {
        if (this.progress < 90) this.progress += Math.random() * 10;
      }, 200);

      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/generated-scheduled/load`
        );
        const allSchedules = res.data.data.scheduled_meetings || [];
        this.schedule = allSchedules;
        this.groupedSchedule = this.groupByInstructor(this.schedule);
        this.filteredGroupedSchedule = this.groupedSchedule;

        // log institute names after fetching schedule
        this.logInstituteNames();
      } catch {
        this.error = "Failed to fetch schedule.";
      } finally {
        clearInterval(this.progressInterval);
        this.progress = 100;
        setTimeout(() => (this.loading = false), 400);
      }
    },

    groupByInstructor(schedules) {
      return schedules.reduce((acc, s) => {
        const instructor = s.faculty_name || "Unknown Faculty";
        if (!acc[instructor]) acc[instructor] = [];
        acc[instructor].push(s);
        return acc;
      }, {});
    },

    async generateSchedule() {
      await this.fetchSchedule();
      this.scheduleGenerated = true;
      this.showFacultyTable = false;

      const conflicts = this.checkConflicts();
      if (conflicts.length) {
        console.warn("Conflicts detected:", conflicts);
        alert(
          `⚠️ ${conflicts.length} conflicts detected! Check console for details.`
        );
      }
    },

    async saveScheduled() {
      alert("💾 Schedule saved successfully (placeholder).");
    },
  },

  async mounted() {
    await this.fetchUser();
    if (this.scheduleGenerated) await this.fetchSchedule();
    this.loadFetchData();
  },
};
</script>
