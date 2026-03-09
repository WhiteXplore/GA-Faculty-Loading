<template>
  <div
    class="fixed inset-0 flex justify-center items-center bg-gray-800 bg-opacity-40 z-50 min-h-screen"
    @click.self="closeModal"
  >
    <div
      class="bg-white rounded-[20px] shadow-2xl border border-green-100 w-[40%] animate-slideUp"
    >
      <!-- HEADER -->
      <div
        class="flex justify-between items-center px-6 py-4 bg-defaultGreen text-white rounded-t-[20px] shadow"
      >
        <h2 class="text-xl font-semibold">Assign Courses to Year Levels</h2>
        <button
          @click="closeModal"
          class="bg-white/20 hover:bg-white/30 rounded-full p-1 transition"
        >
          <icon name="close" class="w-5 h-5 text-white" />
        </button>
      </div>

      <!-- BODY -->
      <div class="p-6 space-y-6 text-[13px] max-h-[80vh] overflow-y-auto">
        <div class="flex flex-col space-y-2">
          <!-- PROGRAM INFO -->
          <div class="p-4 bg-gray-50 border rounded-xl">
            <div
              class="flex flex-col md:flex-row md:items-center md:justify-between gap-2"
            >
              <p class="text-gray-700">
                <span class="font-bold">Program:</span>
                {{ programData?.program_name }}
              </p>
              <p class="text-gray-700">
                <span class="font-bold">School Year:</span>
                {{ activeSchoolYearName }}
              </p>
            </div>
          </div>

          <!-- INSTRUCTIONS -->
          <div class="p-4 bg-blue-50 border rounded-xl">
            <h3 class="font-bold text-gray-800">Instructions</h3>
            <ul
              class="list-disc list-inside text-gray-700 space-y-1 text-[12px]"
            >
              <li>Select courses for each year level (1st - 4th year)</li>
              <li>
                All sections in the same year level will have these courses
              </li>
              <li>Search by course code or description</li>
              <li>Click a year level to expand or collapse</li>
              <li>Click “Save All” to finalize your assignments</li>
            </ul>
          </div>
        </div>

        <!-- YEAR LEVEL SECTIONS -->
        <div class="space-y-4">
          <div
            v-for="year in [1, 2, 3, 4]"
            :key="year"
            class="border border-gray-200 rounded-xl overflow-hidden shadow-sm bg-white/80 backdrop-blur-sm transition-all"
          >
            <!-- YEAR HEADER -->
            <div
              @click="toggleYear(year)"
              class="flex justify-between items-center px-5 py-3 bg-gray-100 hover:bg-green-50 cursor-pointer transition-colors"
            >
              <div class="flex items-center gap-3">
                <icon
                  :name="
                    expandedYears.includes(year) ? 'arrow-down' : 'arrow-right'
                  "
                  class="w-5 h-5 text-defaultGreen"
                />
                <h3 class="font-semibold text-gray-800">
                  {{ getYearLabel(year) }}
                </h3>
                <span
                  v-if="yearCourses[year]?.length"
                  class="ml-2 px-2 py-0.5 bg-defaultGreen text-white text-xs rounded-full"
                >
                  {{ yearCourses[year].length }} course(s)
                </span>
              </div>

              <button
                @click.stop="clearYearCourses(year)"
                v-if="yearCourses[year]?.length"
                class="px-3 py-1 bg-red-500 text-white text-xs rounded-lg hover:bg-red-600 transition-colors"
              >
                Clear All
              </button>
            </div>

            <!-- YEAR CONTENT -->
            <transition name="fade">
              <div
                v-if="expandedYears.includes(year)"
                class="p-5 space-y-4 bg-white"
              >
                <!-- SEARCH BOX -->
                <div class="relative">
                  <input
                    v-model="searchQueries[year]"
                    type="text"
                    placeholder="Search courses..."
                    class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none text-sm"
                    @focus="showDropdown[year] = true"
                    @input="showDropdown[year] = true"
                  />

                  <!-- DROPDOWN -->
                  <div
                    v-if="
                      showDropdown[year] && filteredCoursesForYear(year).length
                    "
                    class="absolute top-full mt-1 w-full bg-white border border-gray-300 rounded-lg shadow-lg max-h-56 overflow-y-auto z-10"
                  >
                    <div
                      v-for="course in filteredCoursesForYear(year)"
                      :key="course.course_id"
                      @mousedown="addCourseToYear(year, course)"
                      class="px-4 py-2 hover:bg-green-50 cursor-pointer border-b last:border-b-0 transition-colors"
                    >
                      <p class="font-semibold text-sm text-gray-800">
                        {{ course.course_code }}
                      </p>
                      <p class="text-xs text-gray-600">
                        {{ course.course_description }}
                      </p>
                      <p class="text-xs text-gray-500">
                        Curriculum: {{ course.curriculum?.curriculum_name }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- SELECTED COURSES -->
                <div v-if="yearCourses[year]?.length">
                  <h4 class="font-semibold text-gray-700 mb-2 text-sm">
                    Selected Courses
                  </h4>
                  <div class="space-y-2">
                    <div
                      v-for="course in yearCourses[year]"
                      :key="course.course_id"
                      class="flex justify-between items-center p-3 bg-green-50 border border-green-200 rounded-lg"
                    >
                      <div>
                        <p class="font-semibold text-sm text-gray-800">
                          {{ course.course_code }}
                        </p>
                        <p class="text-xs text-gray-600">
                          {{ course.course_description }}
                        </p>
                      </div>
                      <button
                        @click="removeCourseFromYear(year, course.course_id)"
                        class="text-red-500 hover:text-red-700 transition-colors"
                      >
                        <icon name="delete" class="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>

                <!-- NO COURSES -->
                <!-- NO COURSES (Clean Centered Design) -->
                <div
                  v-else
                  class="flex flex-col items-center justify-center py-12 px-6 text-center bg-gradient-to-br from-green-50/70 to-white/70 border border-dashed border-green-300 rounded-xl shadow-inner backdrop-blur-sm"
                >
                  <!-- Icon Circle -->
                  <div>
                    <icon
                      name="question"
                      class="w-16 h-16 mb-4 rounded-full flex items-center justify-center bg-green-100 shadow-sm text-defaultGreen"
                    />
                  </div>

                  <!-- Texts -->
                  <p class="text-gray-800 font-medium text-sm">
                    No courses selected for this year level
                  </p>
                  <p class="text-gray-500 text-xs mt-1">
                    Use the search box above or button below to add courses
                  </p>

                  <!-- Optional Action Button -->
                  <button
                    @click="showDropdown[year] = true"
                    class="mt-5 px-4 py-2 bg-defaultGreen hover:bg-green-600 text-white text-xs font-medium rounded-lg shadow-sm transition-all"
                  >
                    Add Course
                  </button>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- FOOTER -->
      <div class="flex justify-end gap-2 pt-4 border-t p-4">
        <button
          @click="closeModal"
          class="bg-gray-100 text-gray-600 p-2 px-3 rounded-lg hover:bg-white border hover:border-gray-800 hover:text-gray-800"
        >
          Cancel
        </button>
        <button
          @click="saveAllYearCourses"
          :disabled="!hasAnyCoursesSelected"
          class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800"
        >
          Save All
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import axios from "axios";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState } from "pinia";

export default {
  name: "AssignYearCourses",
  components: { icon },
  props: {
    programData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      expandedYears: [1], // Start with 1st year expanded
      yearCourses: {
        1: [],
        2: [],
        3: [],
        4: [],
      },
      searchQueries: {
        1: "",
        2: "",
        3: "",
        4: "",
      },
      showDropdown: {
        1: false,
        2: false,
        3: false,
        4: false,
      },
      allCourses: [],
      schoolYears: [],
      existingAssignments: [],
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["year"]),
    activeSchoolYearId() {
      const activeSchoolYear = this.schoolYears.find((sy) => sy.is_active);
      return activeSchoolYear ? activeSchoolYear.school_year_id : null;
    },
    activeSchoolYearName() {
      const activeSchoolYear = this.schoolYears.find((sy) => sy.is_active);
      return activeSchoolYear
        ? `${activeSchoolYear.school_year_name} - ${this.getSemesterLabel(
            activeSchoolYear.semester,
          )}`
        : "Current School Year";
    },
    hasAnyCoursesSelected() {
      return Object.values(this.yearCourses).some(
        (courses) => courses.length > 0,
      );
    },
  },
  methods: {
    toggleYear(year) {
      const index = this.expandedYears.indexOf(year);
      if (index > -1) {
        this.expandedYears.splice(index, 1);
      } else {
        this.expandedYears.push(year);
      }
    },
    getYearLabel(year) {
      const labels = {
        1: "1st Year",
        2: "2nd Year",
        3: "3rd Year",
        4: "4th Year",
      };
      return labels[year] || `${year} Year`;
    },
    getSemesterLabel(semester) {
      if (semester === 1) return "1st Semester";
      if (semester === 2) return "2nd Semester";
      return "";
    },
    filteredCoursesForYear(year) {
      const query = this.searchQueries[year]?.toLowerCase() || "";
      const selectedIds = this.yearCourses[year].map((c) => c.course_id);

      // Filter courses for this program only
      let programCourses = this.allCourses.filter(
        (c) =>
          c.curriculum?.program_id === this.programData.program_id &&
          !selectedIds.includes(c.course_id),
      );

      // Apply search filter
      if (query) {
        programCourses = programCourses.filter(
          (c) =>
            c.course_code?.toLowerCase().includes(query) ||
            c.course_description?.toLowerCase().includes(query) ||
            c.curriculum?.curriculum_name?.toLowerCase().includes(query),
        );
      }

      return programCourses.slice(0, 50); // Limit results for performance
    },
    addCourseToYear(year, course) {
      // Check if course is already added
      const exists = this.yearCourses[year].some(
        (c) => c.course_id === course.course_id,
      );
      if (!exists) {
        this.yearCourses[year].push(course);
        this.searchQueries[year] = ""; // Clear search
        this.showDropdown[year] = false;
      }
    },
    removeCourseFromYear(year, courseId) {
      this.yearCourses[year] = this.yearCourses[year].filter(
        (c) => c.course_id !== courseId,
      );
    },
    clearYearCourses(year) {
      this.yearCourses[year] = [];
    },
    async loadCourses() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/courses/get-courses",
        );
        this.allCourses = response.data;
      } catch (error) {
        console.error("Failed to load courses:", error);
        toast.error("Failed to load courses");
      }
    },
    async loadSchoolYears() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years",
        );
        this.schoolYears = response.data;
      } catch (error) {
        console.error("Failed to load school years:", error);
      }
    },
    async loadExistingAssignments() {
      if (!this.programData?.program_id || !this.activeSchoolYearId) return;

      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/program-year-courses/get-by-program-and-school-year",
          {
            params: {
              program_id: this.programData.program_id,
              school_year_id: this.activeSchoolYearId,
            },
          },
        );

        this.existingAssignments = response.data;

        // Populate yearCourses with existing assignments
        this.existingAssignments.forEach((assignment) => {
          const yearLevel = assignment.year_level;
          const course = assignment.course;
          if (course && yearLevel >= 1 && yearLevel <= 4) {
            const exists = this.yearCourses[yearLevel].some(
              (c) => c.course_id === course.course_id,
            );
            if (!exists) {
              this.yearCourses[yearLevel].push(course);
            }
          }
        });
      } catch (error) {
        console.error("Failed to load existing assignments:", error);
      }
    },
    async saveAllYearCourses() {
      if (!this.activeSchoolYearId) {
        toast.error("No active school year selected");
        return;
      }

      try {
        // Prepare bulk data
        const bulkData = [];
        for (let year = 1; year <= 4; year++) {
          const courses = this.yearCourses[year];
          courses.forEach((course) => {
            bulkData.push({
              program_id: this.programData.program_id,
              course_id: course.course_id,
              year_level: year,
              school_year_id: this.activeSchoolYearId,
            });
          });
        }

        if (bulkData.length === 0) {
          toast.warning("No courses selected to save");
          return;
        }

        // Delete existing assignments for this program and school year
        for (let year = 1; year <= 4; year++) {
          await axios.delete(
            process.env.VUE_APP_API_BASE_URL +
              "/program-year-courses/delete-by-year-level",
            {
              params: {
                program_id: this.programData.program_id,
                year_level: year,
                school_year_id: this.activeSchoolYearId,
              },
            },
          );
        }

        // Create new assignments
        await axios.post(
          process.env.VUE_APP_API_BASE_URL +
            "/program-year-courses/create-bulk",
          bulkData,
        );

        toast.success("Course assignments saved successfully!");
        this.$emit("refresh");
        this.closeModal();
      } catch (error) {
        console.error("Failed to save course assignments:", error);
        toast.error("Failed to save course assignments");
      }
    },
    closeModal() {
      this.$emit("close");
    },
  },
  async mounted() {
    await this.loadSchoolYears();
    await this.loadCourses();
    await this.loadExistingAssignments();
  },
};
</script>
