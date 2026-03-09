<template>
  <div>
    <!-- Top Controls -->
    <div v-if="isTable" class="mb-6">
      <div class="flex justify-between items-center">
        <div class="text-sm text-gray-600 mt-4 font-medium">
          Pages / Faculty Loads
        </div>

        <div class="flex gap-3">
          <!-- View Faculty Button -->
          <div
            @click="showFacultyTable = !showFacultyTable"
            class="group flex items-center gap-2 px-4 py-2 border border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white rounded-xl shadow-sm cursor-pointer transition"
          >
            <div
              class="p-1 bg-blue-100 rounded-full flex items-center justify-center group-hover:bg-white transition"
            >
              <icon
                name="users"
                class="w-4 h-4 text-blue-600 group-hover:text-blue-600"
              />
            </div>
            <span class="font-medium text-sm">View Faculty</span>
          </div>

          <!-- Auto Generation Button -->
          <div
            @click="generateSchedule"
            class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
          >
            <div
              class="flex items-center justify-center w-5 h-5 bg-white rounded-full group-hover:bg-green-100 transition-colors duration-300"
            >
              <icon
                name="arrow-path"
                class="w-4 h-4 text-defaultGreen transition-colors duration-300 group-hover:text-defaultGreen"
              />
            </div>
            <span class="font-medium text-sm">Auto Generation</span>
          </div>

          <!-- Save Schedule -->
          <div
            @click="saveScheduled"
            class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
          >
            <div
              class="flex items-center justify-center w-5 h-5 bg-white rounded-full group-hover:bg-green-100 transition-colors duration-300"
            >
              <icon
                name="circle-check"
                class="w-4 h-4 text-defaultGreen transition-colors duration-300 group-hover:text-defaultGreen"
              />
            </div>
            <span class="font-medium text-sm">Save this schedule</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Faculty Table -->
    <div
      v-if="showFacultyTable && !selectedInstructor"
      class="mt-6 bg-white rounded-xl border p-5"
    >
      <div
        class="flex flex-wrap items-center justify-between gap-4 mb-3 text-gray-700"
      >
        <!-- Items per page -->
        <div class="flex items-center gap-2">
          <label class="text-sm font-medium">Show:</label>
          <div class="relative">
            <select
              v-model="itemsPerPage"
              @change="changePage(1)"
              class="appearance-none rounded-lg border border-green-600 bg-white px-3 py-1.5 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
            >
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
            </select>
            <!-- Custom arrow -->
            <div
              class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-green-700"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </div>
          </div>
          <span class="text-sm font-medium">per page</span>
        </div>

        <!-- Institute & Program Filter Dropdowns -->
        <div class="flex flex-wrap items-center gap-4">
          <!-- Institute Filter -->
          <div class="flex items-center gap-2">
            <label
              for="instituteFilter"
              class="text-sm text-gray-600 font-medium"
            >
              Institute:
            </label>
            <select
              id="instituteFilter"
              v-model="selectedInstituteId"
              class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-green-500 focus:border-green-500 w-[180px]"
            >
              <option value="">All Institutes</option>
              <option
                v-for="institute in uniqueInstituteIds"
                :key="institute"
                :value="institute"
              >
                Institute {{ institute }}
              </option>
            </select>
          </div>

          <!-- Program Filter -->
          <div class="flex items-center gap-2">
            <label
              for="programFilter"
              class="text-sm text-gray-600 font-medium"
            >
              Program:
            </label>
            <select
              id="programFilter"
              v-model="selectedProgramId"
              :disabled="!selectedInstituteId"
              class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:bg-gray-100 disabled:cursor-not-allowed w-[180px]"
            >
              <option value="">All Programs</option>
              <option
                v-for="programId in filteredProgramIds"
                :key="programId"
                :value="programId"
              >
                Program {{ programId }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Table -->
      <div
        class="w-full mt-4 rounded-xl border bg-white overflow-hidden shadow-sm max-h-[500px] overflow-y-auto"
      >
        <table
          class="min-w-full text-sm text-gray-700 border-collapse table-auto"
        >
          <thead class="bg-defaultGreen text-white sticky top-0 z-10">
            <tr>
              <th
                class="px-5 py-3 text-left font-semibold w-auto whitespace-nowrap"
              >
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
              <td class="px-5 py-3 font-medium text-gray-800 whitespace-nowrap">
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
              <td colspan="2" class="py-5 text-gray-500">No faculty found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Controls -->
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

        <span class="font-medium">
          Page {{ currentPage }} of {{ totalPages }}
        </span>

        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-1.5 border rounded-lg hover:bg-gray-100 disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div
      v-if="loading"
      class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50"
    >
      <div class="relative flex items-center justify-center">
        <!-- Animated Glow Aura -->
        <div
          class="absolute w-52 h-44 bg-gradient-to-r from-green-400/30 to-emerald-500/30 rounded-3xl animate-ping"
        ></div>

        <!-- Card Container -->
        <div
          class="relative flex flex-col items-center justify-center bg-white/90 backdrop-blur-md p-8 rounded-3xl shadow-2xl border border-white/30"
        >
          <!-- Smooth Rotating Loader -->
          <div class="relative mb-4">
            <div
              class="w-12 h-12 border-4 border-green-400 border-t-transparent rounded-full animate-spin"
            ></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-defaultGreen text-sm font-semibold">
                {{ Math.floor(progress) }}%
              </span>
            </div>
          </div>

          <!-- Loading Text -->
          <div class="text-gray-700 font-semibold text-[15px] tracking-wide">
            Generating Schedule...
          </div>

          <!-- Subtext -->
          <div class="text-xs text-gray-500 mt-1">
            Please wait while we finalize your data.
          </div>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center text-red-600 font-medium py-6">
      {{ error }}
    </div>

    <!-- Schedule Display -->
    <div v-else-if="!showFacultyTable" class="relative">
      <!-- Back Button (only shows when viewing one instructor) -->
      <div
        v-if="Object.keys(filteredGroupedSchedule).length === 1"
        class="mb-4"
      >
        <button
          @click="backToFacultyTable"
          class="flex items-center gap-2 px-4 py-2 border border-gray-400 text-gray-700 hover:bg-gray-100 rounded-lg shadow-sm transition"
        >
          <icon name="arrow-left" class="w-4 h-4" />
          <span class="font-medium text-sm">Back to Faculty List</span>
        </button>
      </div>

      <!-- Schedule Cards -->
      <div
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 h-[71.5vh] overflow-y-auto pr-2"
      >
        <div
          v-for="(records, instructor) in filteredGroupedSchedule"
          :key="instructor"
          class="bg-white rounded-xl overflow-hidden border border-gray-200 flex flex-col"
        >
          <!-- Instructor Header -->
          <div
            :class="[
              'text-white text-center py-3 font-semibold text-sm',
              getProgramColor(instructor),
            ]"
          >
            {{ instructor }}
          </div>

          <!-- Scrollable Schedule Table -->
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
                    class="relative border border-gray-200 text-center align-top h-[60px] p-0"
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
                          top: getBlockTop(item),
                          height: getBlockHeight(item) + 'px',
                          width: 'calc(100% - 0.5rem)',
                        }"
                      >
                        <div class="p-2 leading-snug truncate">
                          <p class="font-semibold truncate">
                            {{ item.course_name }}
                          </p>
                          <p class="text-gray-600 truncate">
                            {{ item.room_name }}
                          </p>
                          <p class="text-gray-600 truncate">
                            Set: {{ item.set }}
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

    <!-- Conflict Modal -->
    <div
      v-if="showConflictModal"
      class="fixed inset-0 flex items-center justify-center bg-black/50 z-50"
    >
      <div class="bg-white w-full max-w-lg rounded-2xl shadow-xl p-6 relative">
        <button
          @click="closeConflictModal"
          class="absolute top-3 right-3 text-gray-400 hover:text-gray-600"
        >
          ✖
        </button>

        <h2 class="text-lg font-semibold text-red-600 mb-4">
          ⚠ Schedule Conflict Detected
        </h2>

        <div class="space-y-3 max-h-80 overflow-y-auto pr-2">
          <div
            v-for="conflict in selectedConflict.conflicts"
            :key="conflict.course_name + conflict.room_name"
            class="p-3 bg-red-50 border border-red-200 rounded-lg text-sm"
          >
            <p class="font-semibold text-red-700">
              {{ conflict.course_name }} ({{ conflict.type }})
            </p>
            <p class="text-gray-600">
              🕒 {{ conflict.start_hour }} - {{ conflict.end_hour }}
            </p>
            <p class="text-gray-600">📍 {{ conflict.room_name }}</p>
            <p class="text-gray-600">👨‍🏫 {{ conflict.faculty_name }}</p>
            <p class="text-gray-600">📌 Set: {{ conflict.set }}</p>
          </div>
        </div>

        <div class="mt-5 text-right">
          <button
            @click="closeConflictModal"
            class="px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition"
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
import icon from "@/assets/icon.vue";

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
      isTable: true,
      showFacultyTable: false,
      selectedInstructor: null,
      scheduleGenerated: false,

      // Filter controls
      selectedInstituteId: "",
      selectedProgramId: "",

      days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      timeSlots: [
        { start: 8, end: 9 },
        { start: 9, end: 10 },
        { start: 10, end: 11 },
        { start: 11, end: 12 },
        { start: 12, end: 13 },
        { start: 13, end: 14 },
        { start: 14, end: 15 },
        { start: 15, end: 16 },
        { start: 16, end: 17 },
        { start: 17, end: 18 },
      ],
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
    // 🔹 Get unique Institute IDs from schedule
    uniqueInstituteIds() {
      const ids = new Set(
        this.schedule
          .map((s) => s.institute_id)
          .filter((id) => id !== null && id !== undefined),
      );
      return Array.from(ids);
    },

    // 🔹 Get Programs filtered by selected Institute
    filteredProgramIds() {
      if (!this.selectedInstituteId) {
        const allPrograms = new Set(
          this.schedule
            .map((s) => s.program_id)
            .filter((id) => id !== null && id !== undefined),
        );
        return Array.from(allPrograms);
      }

      const programs = new Set(
        this.schedule
          .filter((s) => s.institute_id == this.selectedInstituteId)
          .map((s) => s.program_id)
          .filter((id) => id !== null && id !== undefined),
      );
      return Array.from(programs);
    },

    // 🔹 Apply pagination to filtered faculty
    paginatedFaculty() {
      const allFaculty = Object.entries(this.filteredGroupedSchedule);
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return Object.fromEntries(allFaculty.slice(start, end));
    },

    // 🔹 Compute total number of pages
    totalPages() {
      return Math.ceil(
        Object.keys(this.filteredGroupedSchedule).length / this.itemsPerPage,
      );
    },
  },

  watch: {
    // 🔹 Watch filters and update faculty list dynamically
    selectedInstituteId() {
      this.filterSchedules();
      this.selectedProgramId = ""; // reset program when institute changes
    },
    selectedProgramId() {
      this.filterSchedules();
    },
  },

  methods: {
    // 🔹 Format time display
    formatTime(hour) {
      const period = hour >= 12 ? "PM" : "AM";
      const displayHour = hour % 12 === 0 ? 12 : hour % 12;
      return `${displayHour}:00 ${period}`;
    },

    backToFacultyTable() {
      this.filteredGroupedSchedule = this.groupedSchedule;
      this.showFacultyTable = true;
      this.selectedInstructor = null;
    },

    async fetchUser() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          },
        );
        if (res.data) {
          this.user = res.data;
        } else {
          this.$router.push("/");
        }
      } catch (err) {
        console.error("❌ Failed to fetch user:", err);
        this.$router.push("/");
      }
    },

    async fetchSchedule() {
      this.loading = true;
      this.error = null;
      this.progress = 0;

      this.progressInterval = setInterval(() => {
        if (this.progress < 90) this.progress += Math.random() * 10;
      }, 200);

      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/generated-scheduled/load",
        );

        if (response.data.success && response.data.data) {
          const allSchedules = Object.values(response.data.data).flatMap(
            (set) => set.best_schedule || [],
          );

          const deduped = this.deduplicateSchedules(allSchedules);

          const filtered = deduped.filter(
            (s) =>
              !this.user.institute_id ||
              s.institute_id === this.user.institute_id,
          );

          this.schedule = filtered;
          this.groupedSchedule = this.groupByInstructor(this.schedule);
          this.filteredGroupedSchedule = this.groupedSchedule;
        } else {
          this.error = "Invalid schedule format.";
        }
      } catch (err) {
        console.error("❌ Fetch failed:", err);
        this.error = "Failed to fetch schedule.";
      } finally {
        clearInterval(this.progressInterval);
        this.progress = 100;
        setTimeout(() => {
          this.loading = false;
          this.progress = 0;
        }, 400);
      }
    },

    // 🔹 Deduplicate same course-day-room combos
    deduplicateSchedules(schedules) {
      const seen = new Set();
      return schedules.filter((item) => {
        const key = `${item.course_name}-${item.day}-${item.start_hour}-${item.room_name}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    },

    // 🔹 Group schedules by instructor name
    groupByInstructor(schedules) {
      return schedules.reduce((acc, s) => {
        const instructor =
          s.faculty_name ||
          s.instructor_name ||
          `${s.instructor_first_name || ""} ${
            s.instructor_last_name || ""
          }`.trim() ||
          "Unknown Faculty";

        if (!acc[instructor]) acc[instructor] = [];
        acc[instructor].push(s);
        return acc;
      }, {});
    },

    // 🔹 Apply institute/program filters dynamically
    filterSchedules() {
      let filtered = { ...this.groupedSchedule };

      // 🔹 Filter by Institute
      if (this.selectedInstituteId) {
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some((s) => s.institute_id == this.selectedInstituteId),
          ),
        );
      }

      // 🔹 Filter by Program
      if (this.selectedProgramId) {
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some((s) => s.program_id == this.selectedProgramId),
          ),
        );
      }

      this.filteredGroupedSchedule = filtered;
      this.changePage(1); // reset pagination to first page
    },

    getScheduleForCell(slot, day, instructor) {
      const instructorSchedules =
        this.filteredGroupedSchedule[instructor] || [];
      return instructorSchedules.filter(
        (item) =>
          item.day === day &&
          Number(item.start_hour) < slot.end &&
          Number(item.end_hour) > slot.start,
      );
    },
    getBlockHeight(item) {
      // Calculate height based on duration
      const duration = Number(item.end_hour) - Number(item.start_hour);

      // Match exact height of each slot row (computed from CSS)
      // Each <tr> uses py-4 (=> 1rem top + 1rem bottom = 2rem ≈ 32px)
      // Each <td> uses border + padding, so effective row height ≈ 56–60px
      const slotHeight = this.timeSlotHeight; // already 64, perfect baseline
      const height = duration * slotHeight;

      return height - 1; // small adjustment for pixel rounding
    },

    getBlockTop(item) {
      // Calculate offset from first slot (8 AM)
      const start = Number(item.start_hour);
      const firstSlot = this.timeSlots[0].start;
      const slotHeight = this.timeSlotHeight;

      // Align exactly to top of time slot rows
      const offset = (start - firstSlot) * slotHeight;

      return offset; // precise top alignment
    },

    // Check if this is the starting time cell for the schedule
    isStartingSlot(item, slot) {
      return Number(item.start_hour) === Number(slot.start);
    },
    getTypeColor(type) {
      return type === "Lecture"
        ? "bg-green-100 border-green-400"
        : "bg-blue-100 border-blue-400";
    },

    getProgramColor(instructor) {
      const slots = this.groupedSchedule[instructor];
      if (!slots || slots.length === 0) return "bg-defaultGreen";

      const programId = slots[0].program_id;
      if (programId === 31) return "bg-violet-600";
      if (programId === 32) return "bg-amber-800";

      const colors = [
        "bg-purple-600",
        "bg-green-600",
        "bg-blue-600",
        "bg-amber-600",
        "bg-pink-600",
      ];
      const index =
        Math.abs(
          instructor.split("").reduce((sum, c) => sum + c.charCodeAt(0), 0),
        ) % colors.length;
      return colors[index];
    },

    viewFacultySchedule(instructor) {
      this.filteredGroupedSchedule = {
        [instructor]: this.groupedSchedule[instructor],
      };
      this.showFacultyTable = false;
    },

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },

    openConflictModal(item) {
      this.selectedConflict = item;
      this.showConflictModal = true;
    },

    closeConflictModal() {
      this.showConflictModal = false;
      this.selectedConflict = {};
    },

    async generateSchedule() {
      await this.fetchSchedule();
      this.scheduleGenerated = true;
    },

    async saveScheduled() {
      alert("💾 Schedule saved successfully (placeholder).");
    },
  },

  async mounted() {
    await this.fetchUser();
    if (this.scheduleGenerated) {
      await this.fetchSchedule();
    }
  },
};
</script>
