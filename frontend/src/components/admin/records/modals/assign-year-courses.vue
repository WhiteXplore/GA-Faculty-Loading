<template>
  <div
    class="fixed top-0 bottom-0 right-0 left-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    @click.self="closeModal"
  >
    <div class="bg-white p-6 rounded-2xl shadow-2xl w-[90%] max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">
          Assign Courses to Year Levels
        </h2>
        <button
          @click="closeModal"
          class="text-gray-500 hover:text-gray-700 transition-colors"
        >
          <icon name="close" class="w-6 h-6" />
        </button>
      </div>

      <!-- Program Info -->
      <div class="mb-6 p-4 bg-green-50 rounded-lg border border-green-200">
        <p class="text-sm text-gray-700">
          <span class="font-bold">Program:</span> {{ programData?.program_name }}
        </p>
        <p class="text-sm text-gray-700">
          <span class="font-bold">School Year:</span> {{ activeSchoolYearName }}
        </p>
      </div>

      <!-- Instructions -->
      <div class="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h3 class="font-bold text-sm text-blue-800 mb-2">Instructions:</h3>
        <ul class="text-xs text-blue-700 space-y-1 list-disc list-inside">
          <li>Select courses for each year level (1st - 4th year)</li>
          <li>All sections in the same year level will have these courses</li>
          <li>You can search for courses by code or description</li>
          <li>Click on a year level to expand/collapse it</li>
          <li>Click "Save All" to apply the assignments</li>
        </ul>
      </div>

      <!-- Year Levels -->
      <div class="space-y-4">
        <div
          v-for="year in [1, 2, 3, 4]"
          :key="year"
          class="border rounded-xl overflow-hidden"
        >
          <!-- Year Header -->
          <div
            @click="toggleYear(year)"
            class="flex justify-between items-center p-4 bg-gray-100 hover:bg-gray-200 cursor-pointer transition-colors"
          >
            <div class="flex items-center gap-3">
              <icon
                :name="expandedYears.includes(year) ? 'arrow-down' : 'arrow-right'"
                class="w-5 h-5 text-gray-600"
              />
              <h3 class="font-bold text-lg text-gray-800">
                {{ getYearLabel(year) }}
              </h3>
              <span
                v-if="yearCourses[year] && yearCourses[year].length > 0"
                class="px-2 py-1 bg-green-500 text-white text-xs rounded-full"
              >
                {{ yearCourses[year].length }} course(s)
              </span>
            </div>
            <button
              @click.stop="clearYearCourses(year)"
              v-if="yearCourses[year] && yearCourses[year].length > 0"
              class="px-3 py-1 bg-red-500 text-white text-xs rounded-lg hover:bg-red-600 transition-colors"
            >
              Clear All
            </button>
          </div>

          <!-- Year Content -->
          <div v-if="expandedYears.includes(year)" class="p-4 bg-white">
            <!-- Search Box -->
            <div class="mb-4 relative">
              <input
                v-model="searchQueries[year]"
                type="text"
                placeholder="Search courses by code or description..."
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                @focus="showDropdown[year] = true"
                @input="showDropdown[year] = true"
              />

              <!-- Dropdown for available courses -->
              <div
                v-if="showDropdown[year] && filteredCoursesForYear(year).length > 0"
                class="absolute top-full mt-1 w-full bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto z-10"
              >
                <div
                  v-for="course in filteredCoursesForYear(year)"
                  :key="course.course_id"
                  @mousedown="addCourseToYear(year, course)"
                  class="px-4 py-3 hover:bg-green-50 cursor-pointer border-b last:border-b-0"
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

            <!-- Selected Courses -->
            <div v-if="yearCourses[year] && yearCourses[year].length > 0">
              <h4 class="font-bold text-sm text-gray-700 mb-2">
                Selected Courses:
              </h4>
              <div class="space-y-2">
                <div
                  v-for="course in yearCourses[year]"
                  :key="course.course_id"
                  class="flex justify-between items-center p-3 bg-green-50 rounded-lg border border-green-200"
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
                    <icon name="delete" class="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>

            <!-- No Courses Selected -->
            <div v-else class="text-center py-8 text-gray-500 text-sm">
              <icon name="question" class="w-12 h-12 text-gray-300 mx-auto mb-2" />
              <p>No courses selected for this year level yet.</p>
              <p class="text-xs text-gray-400 mt-1">Search and click to add courses</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer Actions -->
      <div class="mt-6 flex justify-end gap-3">
        <button
          @click="closeModal"
          class="px-6 py-3 border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-100 transition-colors"
        >
          Cancel
        </button>
        <button
          @click="saveAllYearCourses"
          :disabled="!hasAnyCoursesSelected"
          class="px-6 py-3 bg-defaultGreen text-white rounded-xl hover:bg-green-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
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
            activeSchoolYear.semester
          )}`
        : "Current School Year";
    },
    hasAnyCoursesSelected() {
      return Object.values(this.yearCourses).some((courses) => courses.length > 0);
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
          !selectedIds.includes(c.course_id)
      );

      // Apply search filter
      if (query) {
        programCourses = programCourses.filter(
          (c) =>
            c.course_code?.toLowerCase().includes(query) ||
            c.course_description?.toLowerCase().includes(query) ||
            c.curriculum?.curriculum_name?.toLowerCase().includes(query)
        );
      }

      return programCourses.slice(0, 50); // Limit results for performance
    },
    addCourseToYear(year, course) {
      // Check if course is already added
      const exists = this.yearCourses[year].some(
        (c) => c.course_id === course.course_id
      );
      if (!exists) {
        this.yearCourses[year].push(course);
        this.searchQueries[year] = ""; // Clear search
        this.showDropdown[year] = false;
      }
    },
    removeCourseFromYear(year, courseId) {
      this.yearCourses[year] = this.yearCourses[year].filter(
        (c) => c.course_id !== courseId
      );
    },
    clearYearCourses(year) {
      this.yearCourses[year] = [];
    },
    async loadCourses() {
      try {
        const response = await axios.get(
          "http://localhost:8000/courses/get-courses"
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
          "http://localhost:8000/school-year/get-school-years"
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
          "http://localhost:8000/program-year-courses/get-by-program-and-school-year",
          {
            params: {
              program_id: this.programData.program_id,
              school_year_id: this.activeSchoolYearId,
            },
          }
        );

        this.existingAssignments = response.data;

        // Populate yearCourses with existing assignments
        this.existingAssignments.forEach((assignment) => {
          const yearLevel = assignment.year_level;
          const course = assignment.course;
          if (course && yearLevel >= 1 && yearLevel <= 4) {
            const exists = this.yearCourses[yearLevel].some(
              (c) => c.course_id === course.course_id
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
            "http://localhost:8000/program-year-courses/delete-by-year-level",
            {
              params: {
                program_id: this.programData.program_id,
                year_level: year,
                school_year_id: this.activeSchoolYearId,
              },
            }
          );
        }

        // Create new assignments
        await axios.post(
          "http://localhost:8000/program-year-courses/create-bulk",
          bulkData
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

<style scoped>
/* Add custom scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>




