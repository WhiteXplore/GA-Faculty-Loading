<template>
  <div>
    <!-- Table / Auto Generation Button -->
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
                :name="'user-group'"
                class="w-4 h-4 text-blue-600 group-hover:text-blue-600"
              />
            </div>
            <span class="font-medium text-sm">View Faculty</span>
          </div>

          <!-- Auto Generation Button -->
          <div
            @click="generateSchedule"
            class="group flex items-center gap-2 px-4 py-2 border border-green-600 text-green-600 hover:bg-green-600 hover:text-white rounded-xl shadow-sm cursor-pointer transition"
          >
            <div
              class="p-1 bg-green-100 rounded-full flex items-center justify-center group-hover:bg-white transition"
            >
              <icon
                :name="'arrow-path'"
                class="w-4 h-4 text-green-600 group-hover:text-green-600"
              />
            </div>
            <span class="font-medium text-sm">Auto Generation</span>
          </div>

          <!-- Save this schedule -->
          <div
            @click="saveScheduled"
            class="group flex items-center gap-2 px-4 py-2 border border-green-600 text-green-600 hover:bg-green-600 hover:text-white rounded-xl shadow-sm cursor-pointer transition"
          >
            <div
              class="p-1 bg-green-100 rounded-full flex items-center justify-center group-hover:bg-white transition"
            >
              <icon
                :name="'circle-check'"
                class="w-4 h-4 text-green-600 group-hover:text-green-600"
              />
            </div>
            <span class="font-medium text-sm">Save this schedule</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Faculty Table -->
    <div v-if="showFacultyTable" class="mt-6 bg-white rounded-xl border p-5">
      <!-- FILTER BAR -->

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
              <option value="5">5</option>
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

      <!-- FACULTY TABLE -->
      <div
        class="w-full mt-5 rounded-xl border bg-white overflow-hidden shadow-sm max-h-[500px] overflow-y-auto"
      >
        <table class="min-w-full text-sm text-gray-700 border-collapse">
          <thead class="bg-defaultGreen text-white sticky top-0 z-10">
            <tr>
              <th class="px-4 py-3 text-left">Faculty Name</th>
              <th class="px-4 py-3 text-center w-28">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(slots, instructor) in paginatedFaculty"
              :key="instructor"
              class="hover:bg-green-50 transition-all border-t"
            >
              <td class="px-4 py-3 text-gray-700 font-medium truncate">
                {{ instructor }}
              </td>
              <td class="px-4 py-3 text-center">
                <button
                  @click="viewFacultySchedule(instructor)"
                  class="px-3 py-1 h-8 border border-blue-300 hover:bg-blue-200 text-blue-800 rounded-lg flex items-center gap-1"
                >
                  <icon name="eye" /> View
                </button>
              </td>
            </tr>

            <tr
              v-if="!Object.keys(filteredFacultyByInstituteAndProgram).length"
              class="text-center"
            >
              <td colspan="2" class="py-4 text-gray-500">No faculty found.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="flex justify-between items-center mt-4">
        <div class="text-gray-700">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredData.length }} faculty
        </div>
        <div class="flex items-center">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400"
          >
            &lt;
          </button>
          <span v-for="page in pageNumbers" :key="'page-' + page">
            <button
              @click="changePage(page)"
              :class="{
                ' bg-defaultGreen text-white': currentPage === page,
                'bg-gray-200 text-gray-700': currentPage !== page,
              }"
              class="px-3 py-1 mx-1 rounded-md hover:bg-green-300"
            >
              {{ page }}
            </button>
          </span>
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div
      v-if="loading"
      class="fixed inset-0 flex items-center justify-center bg-black/40 z-50"
    >
      <div
        class="space-y-5 flex flex-col items-center justify-center p-5 bg-white rounded-3xl shadow-lg"
      >
        <div class="flex space-x-2">
          <span class="w-3 h-3 bg-green-500 rounded-full bounce-delay-0"></span>
          <span
            class="w-3 h-3 bg-green-500 rounded-full bounce-delay-200"
          ></span>
          <span
            class="w-3 h-3 bg-green-500 rounded-full bounce-delay-400"
          ></span>
        </div>
        <div class="text-gray-700 font-medium">
          Generating Schedule... {{ Math.floor(progress) }}%
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center text-red-600 font-medium py-6">
      {{ error }}
    </div>

    <!-- Schedule Display -->
    <div
      v-else-if="!showFacultyTable"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 h-[70vh]"
    >
      <div
        v-for="(slots, instructor) in filteredGroupedSchedule"
        :key="instructor"
        class="bg-white rounded-2xl shadow-md overflow-hidden border border-gray-200 flex flex-col"
      >
        <!-- Instructor Header -->
        <div
          class="bg-defaultGreen text-white text-center py-3 font-semibold text-lg"
        >
          {{ instructor }}
        </div>

        <!-- Scrollable Table -->
        <div class="overflow-x-auto overflow-y-auto flex-1">
          <table class="w-full text-sm text-left border-collapse">
            <thead class="sticky top-0 bg-gray-100 z-10">
              <tr class="text-gray-700 text-sm">
                <th class="px-4 py-2 border border-gray-200 w-24">Time</th>
                <th
                  v-for="day in days"
                  :key="day"
                  class="px-4 py-2 border border-gray-200 text-center w-30"
                >
                  {{ day }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="slot in timeSlots"
                :key="slot.start + slot.end"
                class="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition"
              >
                <td
                  class="px-4 py-3 border border-gray-200 font-medium text-gray-700 text-xs w-24"
                >
                  {{ slot.start }} - {{ slot.end }}
                </td>

                <td
                  v-for="day in days"
                  :key="day"
                  class="relative px-2 py-2 border border-gray-200 text-center align-top min-h-[80px]"
                >
                  <template
                    v-for="item in getScheduleForCell(slot, day, instructor)"
                    :key="item.course_name + item.start_hour + item.room_name"
                  >
                    <div
                      v-if="isStartingSlot(item, slot)"
                      :rowspan="getRowSpan(item)"
                      :class="[
                        'absolute inset-x-1 border rounded-lg text-xs text-gray-800 shadow-sm overflow-hidden transition-all duration-200',
                        getTypeColor(item.type),
                      ]"
                      :style="{
                        top: '4px',
                        height: getBlockHeight(item) + 'px',
                        minHeight: '75px',
                        maxHeight: '90px',
                        width: 'calc(100% - 0.5rem)',
                      }"
                    >
                      <div class="p-2 text-[12px] leading-snug truncate">
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
                          class="mt-2 w-full text-center px-2 py-1 text-xs rounded bg-red-100 text-red-600 hover:bg-red-200 transition"
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
            <p class="text-gray-600">📍 Room: {{ conflict.room_name }}</p>
            <p class="text-gray-600">👨‍🏫 Faculty: {{ conflict.faculty_name }}</p>
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
      days: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      timeSlots: [
        { start: "8:00 AM", end: "9:00 AM" },
        { start: "9:00 AM", end: "10:00 AM" },
        { start: "10:00 AM", end: "11:00 AM" },
        { start: "11:00 AM", end: "12:00 PM" },
        { start: "12:00 PM", end: "1:00 PM" },
        { start: "1:00 PM", end: "2:00 PM" },
        { start: "2:00 PM", end: "3:00 PM" },
        { start: "3:00 PM", end: "4:00 PM" },
        { start: "4:00 PM", end: "5:00 PM" },
        { start: "5:00 PM", end: "6:00 PM" },
      ],
      progress: 0,
      progressInterval: null,
      showConflictModal: false,
      selectedConflict: {},
      selectedInstituteId: "",
      selectedProgramId: "",
      currentPage: 1,
      itemsPerPage: 10,
    };
  },
  computed: {
    paginatedFaculty() {
      const allFaculty = Object.entries(
        this.filteredFacultyByInstituteAndProgram
      );
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return Object.fromEntries(allFaculty.slice(start, end));
    },

    totalPages() {
      return Math.ceil(
        Object.keys(this.filteredFacultyByInstituteAndProgram).length /
          this.itemsPerPage
      );
    },
    startIndex() {
      if (Object.keys(this.filteredFacultyByInstituteAndProgram).length === 0)
        return 0;
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      const total = Object.keys(
        this.filteredFacultyByInstituteAndProgram
      ).length;
      const end = this.currentPage * this.itemsPerPage;
      return end > total ? total : end;
    },

    pageNumbers() {
      const pages = [];
      for (let i = 1; i <= this.totalPages; i++) {
        pages.push(i);
      }
      return pages;
    },

    // Get unique faculty_institute_id values
    uniqueInstituteIds() {
      const ids = new Set();
      Object.values(this.groupedSchedule).forEach((facultySlots) => {
        facultySlots.forEach((slot) => {
          if (slot.faculty_institute_id) ids.add(slot.faculty_institute_id);
        });
      });
      return Array.from(ids);
    },

    // Get unique program_id values filtered by selected institute
    filteredProgramIds() {
      const ids = new Set();
      Object.values(this.groupedSchedule).forEach((facultySlots) => {
        facultySlots.forEach((slot) => {
          if (
            (!this.selectedInstituteId ||
              slot.faculty_institute_id == this.selectedInstituteId) &&
            slot.program_id
          ) {
            ids.add(slot.program_id);
          }
        });
      });
      return Array.from(ids);
    },

    // Filter faculty by both institute and program
    filteredFacultyByInstituteAndProgram() {
      const filtered = {};
      for (const [instructor, slots] of Object.entries(this.groupedSchedule)) {
        const match = slots.some((s) => {
          const matchesInstitute =
            !this.selectedInstituteId ||
            s.faculty_institute_id == this.selectedInstituteId;
          const matchesProgram =
            !this.selectedProgramId || s.program_id == this.selectedProgramId;
          return matchesInstitute && matchesProgram;
        });
        if (match) filtered[instructor] = slots;
      }
      return filtered;
    },
  },
  watch: {
    // Reset program selection when institute changes
    selectedInstituteId() {
      this.selectedProgramId = "";
    },
  },
  methods: {
    filteredData() {
      return Object.keys(this.filteredFacultyByInstituteAndProgram);
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    viewFacultySchedule(instructor) {
      this.selectedInstructor = instructor;
      this.filteredGroupedSchedule = {
        [instructor]: this.groupedSchedule[instructor],
      };
      this.showFacultyTable = false;
    },
    // ... keep all your existing methods unchanged
    getRowSpan(item) {
      const start = this.convertToMinutes(item.start_hour);
      const end = this.convertToMinutes(item.end_hour);
      const duration = end - start;
      return Math.ceil(duration / 60);
    },
    isStartingSlot(item, slot) {
      const slotStart = this.timeToMinutes(slot.start);
      const itemStart = this.convertToMinutes(item.start_hour);
      return itemStart >= slotStart && itemStart < slotStart + 60;
    },
    getTypeColor(type) {
      switch (type) {
        case "Lecture":
          return "bg-green-100 border-green-400";
        case "Laboratory":
          return "bg-blue-100 border-blue-400";
        default:
          return "bg-gray-100 border-gray-300";
      }
    },
    getBlockHeight(item) {
      const start = this.convertToMinutes(item.start_hour);
      const end = this.convertToMinutes(item.end_hour);
      return ((end - start) / 60) * 40;
    },
    deduplicateSchedules(schedules) {
      const seen = new Set();
      return schedules.filter((s) => {
        const key = `${s.course_id}-${s.room_id}-${s.faculty_id}-${s.start_hour}-${s.end_hour}-${s.day}-${s.set}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    },
    async generateSchedule() {
      await this.fetchSchedule();
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
          "http://localhost:8000/generated-scheduled/load"
        );

        if (response.data.success && response.data.data) {
          const allSchedules = Object.values(response.data.data).flatMap(
            (set) => set.best_schedule || []
          );
          const deduped = this.deduplicateSchedules(allSchedules);
          const filtered = deduped.filter(
            (s) => s.institute_id === this.user.institute_id
          );
          this.schedule = filtered;
          this.groupedSchedule = this.groupByInstructor(this.schedule);
          this.filteredGroupedSchedule = this.groupedSchedule;
        } else {
          this.error = "Invalid schedule format.";
        }
      } catch (err) {
        console.error(err);
        this.error = "Failed to fetch schedule.";
      } finally {
        clearInterval(this.progressInterval);
        this.progress = 100;
        setTimeout(() => {
          this.loading = false;
          this.progress = 0;
        }, 300);
      }
    },
    groupByInstructor(schedule) {
      return schedule.reduce((acc, item) => {
        const instructor = item.faculty_name || "Unknown";
        if (!acc[instructor]) acc[instructor] = [];
        acc[instructor].push(item);
        return acc;
      }, {});
    },
    getScheduleForCell(slot, day, instructor) {
      const instructorSlots = this.groupedSchedule[instructor] || [];
      const slotStart = this.timeToMinutes(slot.start);
      const slotEnd = this.timeToMinutes(slot.end);
      return instructorSlots.filter((item) => {
        const itemDay = item.day?.slice(0, 3);
        const itemStart = this.convertToMinutes(item.start_hour);
        const itemEnd = this.convertToMinutes(item.end_hour);
        return slotStart < itemEnd && itemStart < slotEnd && itemDay === day;
      });
    },
    timeToMinutes(timeStr) {
      let [time, ampm] = timeStr.split(" ");
      let [h, m] = time.split(":").map(Number);
      if (ampm === "PM" && h !== 12) h += 12;
      if (ampm === "AM" && h === 12) h = 0;
      return h * 60 + m;
    },
    convertToMinutes(hour) {
      return Math.floor(hour) * 60 + Math.round((hour % 1) * 60);
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
        const res = await axios.get("http://localhost:8000/auth/me", {
          withCredentials: true,
        });
        if (res.data) {
          this.user = res.data;
        } else {
          this.$router.push("/");
        }
      } catch (err) {
        console.error("Failed to fetch user:", err);
        this.$router.push("/");
      }
    },
  },
  async mounted() {
    await this.fetchUser();
  },
};
</script>
