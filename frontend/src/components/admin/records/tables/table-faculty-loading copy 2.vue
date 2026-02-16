<template>
  <div class="flex flex-col gap-3 h-[90vh]">
    <!-- TODO  Top Controls -->
    <div class="flex flex-wrap justify-between items-center gap-3">
      <div class="text-sm text-gray-600 mt-2 font-medium">
        Pages / Faculty Loads
      </div>

      <div class="flex gap-3 flex-wrap">
        <!-- TODO  Toggle View Button -->
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

        <!-- TODO  Auto Generation -->
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

        <!-- TODO  Save Schedule -->
        <button
          v-if="appearSave"
          @click="showConfirmSaved = true"
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

    <div class="flex flex-wrap items-center gap-4">
      <!-- TODO  Back Button -->
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

      <!-- TODO  Filters (pushed to the end) -->
      <div class="flex items-center gap-3 flex-wrap ml-auto" v-if="appearSave">
        <!-- TODO  Institute Filter -->
        <div class="relative">
          <select
            v-model="selectedInstituteId"
            class="appearance-none rounded-full border border-green-600 bg-white px-4 py-2 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md w-[200px]"
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

          <!-- TODO  Custom arrow -->
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

        <!-- TODO  Program Filter -->
        <div class="relative">
          <select
            v-model="selectedProgramId"
            :disabled="!selectedInstituteId"
            class="appearance-none rounded-full w-auto border border-green-600 bg-white px-4 py-2 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md disabled:bg-gray-100 disabled:border-gray-300 disabled:text-gray-400 disabled:cursor-not-allowed"
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

          <!-- TODO  Custom arrow -->
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
      </div>
    </div>

    <!-- TODO  Scrollable Content -->
    <div class="flex-1 overflow-y-auto">
      <!-- TODO  ========================= -->
      <!-- TODO  Faculty Table View -->
      <!-- TODO  ========================= -->
      <div v-if="showFacultyTable">
        <div class="overflow-x-auto border p-3 rounded-xl bg-white">
          <!-- TODO  Top Controls -->
          <div
            class="flex justify-between items-center flex-wrap gap-3 text-gray-700 bg-white"
          >
            <!-- TODO  Items per page -->
            <div class="flex items-center gap-2">
              <div class="relative">
                <select
                  v-model="itemsPerPage"
                  class="appearance-none rounded-full border border-green-600 bg-white px-3 py-1 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
                  @change="changePage(1)"
                >
                  <option value="10">10</option>
                  <option value="15">15</option>
                  <option value="20">20</option>
                </select>
                <div
                  class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-defaultGreen"
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
              <span class="text-sm font-medium text-gray-600">Per page</span>
            </div>

            <!-- TODO  Search -->
            <div class="relative w-full sm:w-64 md:w-72 lg:w-80">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search faculty..."
                class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
                @input="changePage(1)"
              />
              <div
                class="absolute inset-y-0 left-3 flex items-center text-defaultGreen pointer-events-none"
              >
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <circle cx="11" cy="11" r="8" />
                  <path d="M21 21l-4.35-4.35" />
                </svg>
              </div>
            </div>
          </div>

          <!-- TODO  Table -->
          <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
            <div class="max-h-[69vh] overflow-y-auto">
              <table class="min-w-full text-sm text-gray-700 border-collapse">
                <thead
                  class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
                >
                  <tr>
                    <th
                      class="px-5 py-3 text-left font-semibold whitespace-nowrap"
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
            </div>
          </div>

          <!-- TODO  Pagination -->
          <div class="flex justify-between items-center mt-4">
            <div class="text-gray-700 text-sm">
              Showing {{ startIndex }} to {{ endIndex }} of
              {{ Object.keys(filteredGroupedSchedule).length }} faculty
            </div>
            <div class="flex items-center">
              <button
                @click="changePage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400 disabled:opacity-50"
              >
                &lt;
              </button>

              <span v-for="page in pageNumbers" :key="'page-' + page">
                <button
                  @click="changePage(page)"
                  :class="{
                    'bg-defaultGreen text-white': currentPage === page,
                    'bg-gray-200 text-gray-700': currentPage !== page,
                  }"
                  class="px-3 py-1 rounded-md hover:bg-green-300"
                >
                  {{ page }}
                </button>
              </span>

              <button
                @click="changePage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400 disabled:opacity-50"
              >
                &gt;
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else>
        <!-- TODO  Faculty Cards -->
        <div
          v-if="Object.keys(filteredGroupedSchedule).length"
          class="gap-6 overflow-y-auto pr-2 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 h-full"
        >
          <div
            v-for="(records, instructor) in filteredGroupedSchedule"
            :key="instructor"
            class="bg-white rounded-xl border flex flex-col"
          >
            <!-- TODO  Header -->
            <div
              class="flex justify-between items-center bg-defaultGreen text-white px-4 py-3 font-semibold text-sm rounded-t-xl"
            >
              <span class="text-lg font-bold">{{ instructor }}</span>
              <div v-if="facultyTotalUnits[instructor]">
                <p class="font-normal">
                  Total Units:
                  {{ facultyTotalUnits[instructor].totalUnits }}
                </p>
              </div>
            </div>

            <!-- TODO  Schedule Table -->
            <div class="flex-1 overflow-auto">
              <table class="w-full text-left border-collapse text-[11px]">
                <thead class="sticky top-0 bg-gray-100 z-10">
                  <tr class="text-gray-700">
                    <th
                      class="px-4 py-2 border border-gray-200 w-24 text-center"
                    >
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
                        v-for="item in getScheduleForCell(
                          slot,
                          day,
                          instructor,
                        )"
                        :key="
                          item.course_name + item.start_hour + item.room_name
                        "
                      >
                        <div
                          v-if="isStartingSlot(item, slot)"
                          :class="[
                            'absolute inset-x-1 border rounded-lg text-[11px] text-gray-800 shadow-sm overflow-hidden transition-all duration-200 whitespace-nowrap',
                            getTypeColor(item.type),
                          ]"
                          :style="{
                            top: getBlockTop(item, slot) + 'px',
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
                            <p class="text-gray-600 truncate">
                              {{ item.set_name }}
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

        <!-- TODO  Fallback ONLY for Faculty Cards -->
        <div
          v-else
          class="flex flex-col items-center justify-center h-full text-center text-gray-500"
        >
          <icon
            name="information-circle"
            class="w-12 h-12 mb-4 text-gray-400"
          />
          <p class="text-lg font-semibold mb-2">No schedule data available</p>
          <p class="text-sm text-gray-400">
            Please click
            <span class="font-medium text-defaultGreen">"Auto Generation"</span>
            to generate schedule data.
          </p>
        </div>
      </div>
    </div>

    <!-- TODO  Loading Overlay -->
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
              <span class="text-defaultGreen text-sm font-semibold"
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
    <!-- TODO  Confirm Save Modal -->
    <div
      v-if="showConfirmSaved"
      class="fixed inset-0 flex items-center justify-center bg-black/30 z-50"
    >
      <div class="bg-white rounded-2xl shadow-2xl p-6 w-96">
        <!-- TODO  Header -->
        <div class="flex justify-between items-center border-b pb-3 mb-4">
          <div class="flex gap-1 items-center">
            <icon
              name="exclamation-circle"
              class="text-green-900 w-7 p-1 rounded-full bg-green-200"
            />
            <h3 class="text-lg font-semibold text-gray-800">Confirm Save</h3>
          </div>

          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 transition"
          >
            ✕
          </button>
        </div>

        <!-- TODO  Message -->
        <p class="text-gray-600 mb-6">
          Are you sure you want to save this schedule?
        </p>

        <!-- TODO  Buttons -->
        <div class="flex justify-center gap-2 text-sm">
          <button
            @click="showConfirmSaved = false"
            class="px-4 py-2 border rounded-xl hover:bg-gray-100 transition"
          >
            Cancel
          </button>
          <button
            @click="saveScheduledConfirmed"
            class="px-4 py-2 bg-defaultGreen text-white rounded-xl hover:bg-green-600 transition"
          >
            Yes, Save
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import icon from "@/assets/icon.vue";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { toast } from "vue3-toastify";
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
      showConfirmSaved: false,
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

      schoolYears: [],
      appearSave: false,
    };
  },

  computed: {
    coursesList() {
      const store = useFetchDataStore();
      return store.courses || [];
    }, // Total units per faculty
    facultyTotalUnits() {
      const result = {};

      Object.entries(this.filteredGroupedSchedule).forEach(
        ([faculty, schedules]) => {
          let totalLecture = 0;
          let totalLab = 0;

          schedules.forEach((sched) => {
            const course = this.coursesList.find(
              (c) => c.course_code === sched.course_code,
            );
            if (!course) return;

            const duration = Number(sched.duration || 0); // e.g., 1.5
            if (sched.type === "Lecture") {
              // Standard lecture assumed 3 hours
              const unitsPerSlot =
                (duration / 3) * Number(course.course_lec || 0);
              totalLecture += unitsPerSlot;
            } else if (sched.type === "Laboratory") {
              // Standard lab assumed 3 hours
              const unitsPerSlot =
                (duration / 3) * Number(course.course_lab || 0);
              totalLab += unitsPerSlot;
            }
          });

          result[faculty] = {
            lectureUnits: totalLecture,
            labUnits: totalLab,
            totalUnits: totalLecture + totalLab,
          };
        },
      );

      return result;
    },
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
        },
      );
    },

    // Map program IDs to their names (filtered by selectedInstituteId if any)
    filteredPrograms() {
      const store = useFetchDataStore();
      const programs = store.programs || [];
      let programIds;

      if (!this.selectedInstituteId) {
        programIds = Array.from(
          new Set(this.schedule.map((s) => s.program_id)),
        );
      } else {
        programIds = Array.from(
          new Set(
            this.schedule
              .filter((s) => s.institute_id == this.selectedInstituteId)
              .map((s) => s.program_id),
          ),
        );
      }

      return programIds.map((id) => {
        const prog = programs.find((p) => p.program_id === id);
        return prog
          ? { id, name: prog.program_name }
          : { id, name: `Program ${id}` };
      });
    },

    // Compute latest active school year dynamically
    latestActiveSchoolYear() {
      if (!this.schoolYears.length) return null;
      const activeYears = this.schoolYears.filter((y) => y.is_active);
      if (!activeYears.length) return null;
      return activeYears.reduce((latest, current) =>
        new Date(current.updated_at) > new Date(latest.updated_at)
          ? current
          : latest,
      );
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    endIndex() {
      return Math.min(
        this.currentPage * this.itemsPerPage,
        Object.keys(this.filteredGroupedSchedule).length,
      );
    },
    totalPages() {
      return Math.ceil(
        Object.keys(this.filteredGroupedSchedule).length / this.itemsPerPage,
      );
    },
    pageNumbers() {
      return Array.from({ length: this.totalPages }, (_, i) => i + 1);
    },
    paginatedFaculty() {
      const allFaculty = Object.entries(this.filteredGroupedSchedule);
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return Object.fromEntries(allFaculty.slice(start, end));
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
      await store.fetchInstitutes();
      await store.fetchCourses();
    },

    backToFacultyTable() {
      this.filteredGroupedSchedule = this.groupedSchedule;
      this.showFacultyTable = true;
      this.currentPage = 1;
    },

    normalizeHour(hour) {
      hour = Number(hour);
      if (Number.isNaN(hour)) return hour;
      return hour <= 7 ? hour + 12 : hour;
    },

    isStartingSlot(item, slot) {
      const start = this.normalizeHour(item.start_hour);
      return start >= slot.start && start < slot.end;
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
            schedules.some((s) => s.institute_id == this.selectedInstituteId),
          ),
        );

      if (this.selectedProgramId)
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some((s) => s.program_id == this.selectedProgramId),
          ),
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
    getBlockTop(item, slot) {
      const itemStart = this.normalizeHour(item.start_hour);
      const slotStart = slot.start;

      const offsetHours = itemStart - slotStart;
      return offsetHours * this.timeSlotHeight;
    },
    getBlockHeight(item) {
      return Math.max(1, Number(item.duration)) * this.timeSlotHeight - 1;
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
          { withCredentials: true },
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
          `${process.env.VUE_APP_API_BASE_URL}/generated-scheduled/load`,
        );

        const allSchedules = res.data.data.scheduled_meetings || [];

        this.schedule = allSchedules;
        this.groupedSchedule = this.groupByInstructor(this.schedule);
        this.filteredGroupedSchedule = this.groupedSchedule;
      } catch {
        this.error = "Failed to fetch schedule.";
      } finally {
        clearInterval(this.progressInterval);
        this.progress = 100;
        setTimeout(() => (this.loading = false), 400);
      }
    },

    async groupByInstructor(schedules) {
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
      this.appearSave = true;
      const conflicts = this.checkConflicts();
      if (conflicts.length) {
        console.warn("Conflicts detected:", conflicts);
        alert(
          `⚠️ ${conflicts.length} conflicts detected! Check console for details.`,
        );
      }
    },

    async fetchSchoolYears() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years",
        );
        this.schoolYears = res.data.map((y) => ({ ...y }));
      } catch (err) {
        console.error("Failed to fetch school years:", err);
      }
    },

    async saveScheduledConfirmed() {
      this.showConfirmSaved = false;

      try {
        // Always fetch latest school years before saving
        await this.fetchSchoolYears();

        const latestSchoolYear = this.latestActiveSchoolYear;
        if (!latestSchoolYear) {
          alert("❌ No active school year found. Cannot save schedule.");
          return;
        }

        const payload = this.schedule.map((item) => ({
          class_id: item.class_id,
          set_name: item.set_name,
          course_code: item.course_code,
          program_id: item.program_id,
          institute_id: item.institute_id,
          type: item.type,
          day: item.day,
          start_hour: item.start_hour,
          duration: item.duration,
          time_slot: `${this.formatTime(item.start_hour)} - ${this.formatTime(
            item.start_hour + Number(item.duration),
          )}`,
          room_id: item.room_id,
          room_name: item.room_name,
          room_type: item.room_type,
          room_capacity: item.room_capacity,
          class_size: item.class_size,
          faculty_id: item.faculty_id,
          faculty_name: item.faculty_name,
          school_year: latestSchoolYear.school_year_name,
          semester: latestSchoolYear.semester,
        }));

        await axios.post(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/bulk`,
          payload,
          { withCredentials: true },
        );

        toast.success("Schedule saved successfully!");
      } catch (error) {
        console.error(error);
        alert("❌ Failed to save schedule.");
      }
    },
  },

  async mounted() {
    await this.fetchUser();
    this.loadFetchData();
    if (this.scheduleGenerated) await this.fetchSchedule();
    await this.fetchSchoolYears(); // ensure school years are loaded on mount
  },
};
</script>
