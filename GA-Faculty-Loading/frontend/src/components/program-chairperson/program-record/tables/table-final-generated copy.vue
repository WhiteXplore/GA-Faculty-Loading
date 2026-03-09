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

        <!-- TODO  Swap Button -->
        <button
          v-if="showCompareSelection"
          @click="swapCourses"
          :disabled="swapSelection.length !== 2"
          class="group flex items-center gap-2 px-4 py-2 border border-yellow-600 text-yellow-600 hover:bg-yellow-600 hover:text-white rounded-xl shadow-sm transition cur"
        >
          <div
            class="p-1 bg-yellow-100 rounded-full flex items-center justify-center group-hover:bg-white transition"
          >
            <icon
              name="arrow-path"
              class="w-4 h-4 text-yellow-600 group-hover:text-yellow-600"
            />
          </div>
          <span class="font-medium text-sm"> Swap </span>
        </button>
        <div
          class="flex items-center gap-3 flex-wrap ml-auto"
          v-if="showCompareSelection"
        >
          <div class="flex gap-2 items-center">
            <select
              v-model="compareInstructorA"
              class="rounded-xl border border-purple-600 px-2 py-2.5 text-sm text-purple-700 shadow-sm"
            >
              <option value="">Select Instructor</option>
              <option
                v-for="instructor in Object.keys(groupedSchedule)"
                :key="'a-' + instructor"
                :value="instructor"
              >
                {{ instructor }}
              </option>
            </select>
            <select
              v-model="compareInstructorB"
              class="rounded-xl border border-purple-600 px-2 py-2.5 text-sm text-purple-700 shadow-sm"
            >
              <option value="">Select Instructor</option>
              <option
                v-for="instructor in Object.keys(groupedSchedule)"
                :key="'b-' + instructor"
                :value="instructor"
              >
                {{ instructor }}
              </option>
            </select>

            <button
              @click="showCompareFacultyCards"
              :disabled="
                !compareInstructorA ||
                !compareInstructorB ||
                compareInstructorA === compareInstructorB
              "
              class="bg-purple-600 text-white px-4 py-2.5 rounded-xl hover:bg-purple-700 transition"
            >
              Compare</button
            ><button
              @click="backFromCompare"
              class="flex items-center gap-2 p-1 border border-gray-400 rounded-full shadow-sm hover:bg-gray-100 transition"
            >
              <icon name="circle-close" class="w-5 h-5" />
            </button>
          </div>
        </div>
        <button
          @click="toggleShowCompareSelection"
          v-if="!showCompareSelection"
          class="bg-purple-600 text-white px-4 py-1 rounded-xl hover:bg-purple-700 transition"
        >
          Compare
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
    </div>

    <!-- TODO  Scrollable Content -->
    <div class="flex-1 overflow-y-auto">
      <!-- TODO  Faculty Table -->
      <div v-if="showFacultyTable">
        <div class="overflow-x-auto border p-3 rounded-xl bg-white">
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

          <!-- TODO  Faculty Table -->
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

      <!-- TODO  Faculty Cards -->
      <div
        v-else
        :class="[
          'gap-6 grid p-2 h-auto',
          showCompareView
            ? 'grid-cols-1 md:grid-cols-2 h-[87vh] overflow-y-auto'
            : Object.keys(filteredGroupedSchedule).length === 1
            ? 'grid-cols-1'
            : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3  overflow-y-auto',
        ]"
      >
        <div
          v-for="(records, instructor) in filteredGroupedSchedule"
          :key="instructor"
          class="bg-white rounded-xl border flex flex-col shadow-sm overflow-hidden"
        >
          <!-- Header -->
          <div
            class="flex justify-between items-center bg-defaultGreen text-white px-4 py-3 font-semibold text-sm rounded-t-xl"
          >
            <div class="flex flex-col">
              <span class="text-lg font-bold">{{ instructor }}</span>

              <div v-if="facultyTotalUnits[instructor]">
                <p class="font-normal">
                  Total Units:
                  {{ facultyTotalUnits[instructor].totalUnits }}
                </p>
              </div>
            </div>

            <button
              @click="openEditInstructorModal(instructor)"
              class="border border-white hover:bg-white hover:text-defaultGreen text-white px-3 py-1 rounded-full text-xs transition"
            >
              Edit
            </button>
          </div>

          <!-- Table wrapper -->
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
                  :style="{ height: timeSlotHeight + 'px' }"
                >
                  <td
                    class="px-4 py-4 border border-gray-200 font-medium text-center whitespace-nowrap"
                  >
                    {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                  </td>
                  <td
                    v-for="day in days"
                    :key="day"
                    class="relative border border-gray-200 text-left align-top p-0 overflow-visible"
                    :style="{ height: timeSlotHeight + 'px' }"
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
                          swapSelection.includes(item)
                            ? 'border-yellow-500 bg-yellow-100'
                            : '',
                        ]"
                        @click="toggleSwapSelection(item)"
                        :style="{
                          top: getBlockTop(item, slot.start) + 'px',
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
                            @click.stop="openConflictModal(item)"
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
  </div>
  <!-- TODO  Edit Instructor Modal -->
  <editSchedule
    :show="showEditModal"
    :instructorData="editInstructorData"
    @close="showEditModal = false"
    @saved="handleModalSaved"
    @deleted="handleDeletedSchedule"
  />
</template>

<script>
import axios from "axios";
import icon from "@/assets/icon.vue";
import { useFetchDataStore } from "@/store/fetch-data-store";
import editSchedule from "../modals/edit-schedule.vue";
import { toast } from "vue3-toastify";

export default {
  name: "FacultySchedule",
  components: { icon, editSchedule },
  data() {
    return {
      user: {},

      groupedSchedule: {},
      filteredGroupedSchedule: {},
      finalSchedules: [],
      loading: false,
      error: null,
      showFacultyTable: false,
      selectedInstructor: null,
      selectedInstituteId: "",
      selectedProgramId: "",
      confirmSaveModal: false,
      days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],

      // 8 AM to 8 PM
      timeSlots: Array.from({ length: 13 }, (_, i) => ({
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
      swapSelection: [],
      showEditModal: false,
      editInstructorData: [],
      compareInstructorA: "",
      compareInstructorB: "",
      showCompareView: false,
      showCompareSelection: false,
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

    uniqueInstitutes() {
      const store = useFetchDataStore();
      const institutes = store.institutes || [];
      return Array.from(
        new Set(this.finalSchedules.map((s) => s.institute_id)),
      ).map((id) => {
        const inst = institutes.find((i) => i.institute_id === id);
        return inst
          ? { id, name: inst.institute_name }
          : { id, name: `Institute ${id}` };
      });
    },
    // Map program IDs to their names (filtered by selectedInstituteId if any)
    filteredPrograms() {
      const store = useFetchDataStore();
      const programs = store.programs || [];

      const programIds = Array.from(
        new Set(
          this.finalSchedules
            .filter((s) =>
              this.selectedInstituteId
                ? String(s.institute_id) === String(this.selectedInstituteId)
                : true,
            )
            .map((s) => s.program_id),
        ),
      );

      return programIds.map((id) => {
        const prog = programs.find((p) => String(p.program_id) === String(id));
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
    searchedFaculty() {
      if (!this.searchQuery) return this.filteredGroupedSchedule;
      const query = this.searchQuery.toLowerCase();
      return Object.fromEntries(
        Object.entries(this.filteredGroupedSchedule).filter(([name]) =>
          name.toLowerCase().includes(query),
        ),
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
    toggleShowCompareSelection() {
      this.showCompareSelection = !this.showCompareSelection;
    },
    backFromCompare() {
      this.filteredGroupedSchedule = { ...this.groupedSchedule };
      this.compareInstructorA = "";
      this.compareInstructorB = "";
      this.showCompareView = false;
      this.showFacultyTable = false;
      this.showCompareSelection = false;
    },
    showCompareFacultyCards() {
      if (!this.compareInstructorA || !this.compareInstructorB) return;

      // Filter groupedSchedule to only the selected instructors
      this.filteredGroupedSchedule = {
        [this.compareInstructorA]:
          this.groupedSchedule[this.compareInstructorA] || [],
        [this.compareInstructorB]:
          this.groupedSchedule[this.compareInstructorB] || [],
      };

      this.showFacultyTable = false; // hide table view
      this.showCompareView = true;
    },
    openEditInstructorModal(instructor) {
      // Send fresh copies of schedules to modal
      this.editInstructorData = (this.groupedSchedule[instructor] || []).map(
        (r) => ({ ...r }),
      );
      this.showEditModal = true;
    },
    handleModalSaved(updatedInstructorSchedules) {
      if (!updatedInstructorSchedules.length) return;

      // Merge updates into finalSchedules
      updatedInstructorSchedules.forEach((updated) => {
        const index = this.finalSchedules.findIndex((s) => s.id === updated.id);
        if (index > -1) {
          this.finalSchedules[index] = { ...updated }; // fresh copy
        } else {
          this.finalSchedules.push({ ...updated });
        }
      });

      // Refresh grouped and filtered schedules
      this.groupedSchedule = this.groupByInstructor(this.finalSchedules);
      this.filteredGroupedSchedule = { ...this.groupedSchedule };

      // Reset pagination
      this.currentPage = 1;

      // If modal is open, update its data with fresh copies
      if (this.showEditModal) {
        const instructorsInModal = Array.from(
          new Set(this.editInstructorData.map((item) => item.faculty_name)),
        );

        this.$nextTick(() => {
          this.editInstructorData = instructorsInModal.flatMap((instructor) => {
            return (this.groupedSchedule[instructor] || []).map((r) => ({
              ...r,
            }));
          });
        });
      }
    },
    handleDeletedSchedule(deletedId) {
      this.finalSchedules = this.finalSchedules.filter(
        (s) => s.id !== deletedId,
      );
      this.groupedSchedule = this.groupByInstructor(this.finalSchedules);
      this.filterSchedules();
    },
    closeEditInstructorModal() {
      this.showEditModal = false;
      this.editInstructorData = {};
    },

    toggleSwapSelection(item) {
      const index = this.swapSelection.indexOf(item);
      if (index > -1) this.swapSelection.splice(index, 1);
      else if (this.swapSelection.length < 2) this.swapSelection.push(item);
      else toast.info("You can only swap 2 courses at a time.");
    },

    async swapCourses() {
      if (this.swapSelection.length !== 2) {
        toast.info("Select exactly 2 courses to swap.");
        return;
      }

      let [courseA, courseB] = this.swapSelection;

      const getTimeRange = (course) => {
        const start = this.normalizeHour(Number(course.start_hour));
        const end = start + Number(course.duration);
        return { start, end };
      };

      const isOverlap = (c1, c2) => {
        const { start: s1, end: e1 } = getTimeRange(c1);
        const { start: s2, end: e2 } = getTimeRange(c2);
        return Math.max(s1, s2) < Math.min(e1, e2);
      };

      const hasSameCourseConflict = (course) =>
        this.finalSchedules.some(
          (s) =>
            s.id !== course.id &&
            s.course_code === course.course_code &&
            s.day === course.day &&
            isOverlap(s, course),
        );

      if (hasSameCourseConflict(courseA) || hasSameCourseConflict(courseB)) {
        toast.error(
          "Cannot swap: a schedule already exists for the same course at the same time and day.",
        );
        return;
      }

      const hasConflict = (course, ignoreIds = []) =>
        this.finalSchedules.some((s) => {
          if (ignoreIds.includes(s.id)) return false;
          if (
            (s.room_id === course.room_id ||
              s.faculty_id === course.faculty_id) &&
            s.day === course.day &&
            s.course_code !== course.course_code &&
            isOverlap(s, course)
          )
            return true;
          return false;
        });

      // Prepare swapped course objects
      const courseAWithBFaculty = {
        ...courseA,
        faculty_id: courseB.faculty_id,
        faculty_name: courseB.faculty_name,
      };
      const courseBWithAFaculty = {
        ...courseB,
        faculty_id: courseA.faculty_id,
        faculty_name: courseA.faculty_name,
      };

      if (
        hasConflict(courseAWithBFaculty, [courseA.id, courseB.id]) ||
        hasConflict(courseBWithAFaculty, [courseA.id, courseB.id])
      ) {
        toast.error(
          "Swap cannot be done due to room or faculty conflict with existing schedules.",
        );
        return;
      }

      // Swap locally
      const tempFacultyId = courseA.faculty_id;
      const tempFacultyName = courseA.faculty_name;

      courseA.faculty_id = courseB.faculty_id;
      courseA.faculty_name = courseB.faculty_name;

      courseB.faculty_id = tempFacultyId;
      courseB.faculty_name = tempFacultyName;

      this.finalSchedules = this.finalSchedules.map((s) => {
        if (s.id === courseA.id) return { ...courseA };
        if (s.id === courseB.id) return { ...courseB };
        return s;
      });

      // Update grouped schedules for UI
      this.groupedSchedule = this.groupByInstructor(this.finalSchedules);
      this.filteredGroupedSchedule = this.showCompareView
        ? {
            [this.compareInstructorA]:
              this.groupedSchedule[this.compareInstructorA] || [],
            [this.compareInstructorB]:
              this.groupedSchedule[this.compareInstructorB] || [],
          }
        : { ...this.groupedSchedule };

      // 🔹 Update edit modal data if it’s open
      if (this.showEditModal) {
        const instructorsInModal = Array.from(
          new Set(this.editInstructorData.map((item) => item.faculty_name)),
        );

        // Refresh modal data using $nextTick to ensure reactivity
        this.$nextTick(() => {
          this.editInstructorData = instructorsInModal.flatMap((instructor) => {
            return (this.groupedSchedule[instructor] || []).map((r) => ({
              ...r,
            }));
          });
        });
      }

      // Update backend
      try {
        await Promise.all([
          axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${courseA.id}`,
            {
              faculty_id: courseA.faculty_id,
              faculty_name: courseA.faculty_name,
            },
          ),
          axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${courseB.id}`,
            {
              faculty_id: courseB.faculty_id,
              faculty_name: courseB.faculty_name,
            },
          ),
        ]);

        // Clear selection and refresh UI
        this.swapSelection = [];
        this.showFacultyTable = false;
        this.showCompareView = true;

        // Force reactive update for tables and cards
        this.$nextTick(() => {
          this.groupedSchedule = { ...this.groupedSchedule };
          this.filteredGroupedSchedule = { ...this.filteredGroupedSchedule };
        });

        toast.success(
          `Courses swapped: ${courseA.course_code} ↔ ${courseB.course_code}`,
        );
      } catch (error) {
        toast.error("Failed to update swap in the database.");
        console.error(error);
      }
    },
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
      // If you are using 1–7 as PM and 8–24 as actual hours
      return hour <= 7 ? hour + 12 : hour;
    },

    formatTime(h) {
      if (h == null) return "";
      const hour = Math.floor(h); // integer hour
      const minutes = Math.round((h - hour) * 60); // decimal -> minutes
      const period = hour >= 12 ? "PM" : "AM";
      const hour12 = hour % 12 || 12;
      const minutesStr = minutes.toString().padStart(2, "0");
      return `${hour12}:${minutesStr} ${period}`;
    },
    isStartingSlot(item, slot) {
      return item.start_hour >= slot.start && item.start_hour < slot.end;
    },
    getBlockTop(item, slotStart) {
      if (!item || item.start_hour == null) return 0;

      const start = this.normalizeHour(Number(item.start_hour));
      return (start - slotStart) * this.timeSlotHeight;
    },

    getBlockHeight(item) {
      if (!item || !item.duration) return this.timeSlotHeight;

      return Number(item.duration) * this.timeSlotHeight - 1;
    },

    filterSchedules() {
      let filtered = { ...this.groupedSchedule };

      if (this.selectedInstituteId) {
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some(
              (s) =>
                String(s.institute_id) === String(this.selectedInstituteId),
            ),
          ),
        );
      }

      if (this.selectedProgramId) {
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some(
              (s) => String(s.program_id) === String(this.selectedProgramId),
            ),
          ),
        );
      }

      this.filteredGroupedSchedule = filtered;
      this.currentPage = 1;
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

    async fetchFinalSchedules() {
      this.loading = true;
      this.error = null;

      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/final-generated-class-schedule/get-all-final-schedules",
          { withCredentials: true },
        );

        let schedules = data || [];
        if (this.user.role === "Program Chairperson") {
          schedules = schedules.filter(
            (s) =>
              s.institute_id === this.user.institute_id &&
              s.program_id === this.user.program_id,
          );
        }

        this.finalSchedules = schedules;
        this.groupedSchedule = this.groupByInstructor(this.finalSchedules);
        this.filteredGroupedSchedule = { ...this.groupedSchedule };

        this.changePage(1);
      } catch (err) {
        this.error = err.message || "Failed to fetch final schedules";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    // Keep your existing groupByInstructor method
    groupByInstructor(schedules) {
      return schedules.reduce((acc, s) => {
        const instructor = s.faculty_name || "Unknown Faculty";
        if (!acc[instructor]) acc[instructor] = [];
        acc[instructor].push(s);
        return acc;
      }, {});
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
  },
  async mounted() {
    await this.fetchUser();
    await this.loadFetchData();
    await this.fetchSchoolYears();
    await this.fetchFinalSchedules();
  },
};
</script>
