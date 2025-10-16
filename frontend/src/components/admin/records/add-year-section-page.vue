<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-md">Add Year/Section</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Program Card -->
      <div
        v-if="userProgram"
        class="border p-4 rounded-xl bg-white shadow-sm hover:shadow-md transition-all"
      >
        <div class="flex justify-between items-center">
          <div>
            <h2 class="text-lg font-bold text-gray-800">
              {{ userProgram.program_name }}
            </h2>
            <p class="text-sm text-gray-600">
              Code: {{ userProgram.program_code }}
            </p>
            <p class="text-sm text-gray-600" v-if="userProgram.institute">
              Institute: {{ userProgram.institute.institute_name }}
            </p>
          </div>
          <div class="flex gap-3">
            <button
              @click="openYearSectionModal"
              class="flex items-center gap-2 px-4 py-3 bg-defaultGreen text-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300"
            >
              <icon name="add-students" class="w-5 h-5" />
              <span class="font-medium">Add Year/Section</span>
            </button>
            <button
              @click="openAssignCoursesModal"
              class="flex items-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300"
            >
              <icon name="setting" class="w-5 h-5" />
              <span class="font-medium">Assign Courses</span>
            </button>
          </div>
        </div>

        <!-- Instructions -->
        <div class="mt-4 bg-blue-50 p-3 rounded-md">
          <h3 class="font-bold text-sm text-blue-800 mb-2">Instructions:</h3>
          <ul class="text-xs text-blue-700 space-y-1 list-disc list-inside">
            <li>Click "Add Year/Section" to configure class sections</li>
            <li>Select the school year for the sections</li>
            <li>Set the number of sections for each year level (1st-4th)</li>
            <li>Define the class size for each section</li>
            <li>Sections will be automatically named (A, B, C, etc.)</li>
          </ul>
        </div>
      </div>

      <!-- Loading State -->
      <div
        v-else-if="loading"
        class="border p-8 rounded-xl bg-white shadow-sm text-center"
      >
        <p class="text-gray-500">Loading program information...</p>
      </div>

      <!-- No Program Found -->
      <div
        v-else
        class="border p-8 rounded-xl bg-white shadow-sm text-center"
      >
        <icon name="question" class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-500">No program found for your account.</p>
        <p class="text-sm text-gray-400 mt-2">
          Please contact the administrator.
        </p>
      </div>

      <!-- Created Sections Table -->
      <div v-if="userProgram && filteredClasses.length > 0" class="mt-4">
        <div class="border p-4 rounded-xl bg-white shadow-sm">
          <div class="flex justify-between items-center mb-3">
            <h3 class="font-bold text-md text-gray-800">
              Created Sections for {{ activeSchoolYearName }}
            </h3>
            <span class="text-sm text-gray-600">
              Total: {{ filteredClasses.length }} section(s)
            </span>
          </div>

          <!-- Table -->
          <div class="overflow-x-auto">
            <table class="min-w-full text-sm text-gray-700">
              <thead class="bg-defaultGreen text-white">
                <tr>
                  <th class="px-4 py-2 text-left rounded-tl-lg">#</th>
                  <th class="px-4 py-2 text-left">Section Name</th>
                  <th class="px-4 py-2 text-center">Class Size</th>
                  <th class="px-4 py-2 text-left rounded-tr-lg">School Year</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(cls, index) in filteredClasses"
                  :key="cls.class_id"
                  class="border-b hover:bg-green-50"
                >
                  <td class="px-4 py-2">{{ index + 1 }}</td>
                  <td class="px-4 py-2 font-semibold">{{ cls.set_name }}</td>
                  <td class="px-4 py-2 text-center">{{ cls.class_size }}</td>
                  <td class="px-4 py-2">{{ cls.schoolYear?.school_year_name }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- No Sections Message -->
      <div
        v-else-if="userProgram && !loading && filteredClasses.length === 0"
        class="mt-4 border p-8 rounded-xl bg-white shadow-sm text-center"
      >
        <p class="text-gray-500">
          No sections created for {{ activeSchoolYearName }} yet.
        </p>
        <p class="text-sm text-gray-400 mt-2">
          Click "Add Year/Section" to create sections for this school year.
        </p>
      </div>

      <!-- Assigned Courses by Year Level -->
      <div v-if="userProgram && assignedCourses.length > 0" class="mt-4">
        <div class="border p-4 rounded-xl bg-white shadow-sm">
          <div class="flex justify-between items-center mb-3">
            <h3 class="font-bold text-md text-gray-800">
              Assigned Courses for {{ activeSchoolYearName }}
            </h3>
            <button
              @click="openAssignCoursesModal"
              class="px-3 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
            >
              <icon name="setting" class="w-4 h-4 inline mr-1" />
              Edit Assignments
            </button>
          </div>

          <!-- Year Level Tabs/Sections -->
          <div class="space-y-4">
            <div
              v-for="year in [1, 2, 3, 4]"
              :key="year"
              class="border rounded-lg overflow-hidden"
            >
              <!-- Year Header -->
              <div
                @click="toggleYearDisplay(year)"
                class="flex justify-between items-center p-3 bg-gray-100 hover:bg-gray-200 cursor-pointer transition-colors"
              >
                <div class="flex items-center gap-2">
                  <icon
                    :name="
                      expandedYearsDisplay.includes(year)
                        ? 'arrow-down'
                        : 'arrow-right'
                    "
                    class="w-4 h-4 text-gray-600"
                  />
                  <h4 class="font-bold text-sm text-gray-800">
                    {{ getYearLabel(year) }}
                  </h4>
                  <span
                    v-if="getCoursesByYearLevel(year).length > 0"
                    class="px-2 py-1 bg-green-500 text-white text-xs rounded-full"
                  >
                    {{ getCoursesByYearLevel(year).length }} course(s)
                  </span>
                </div>
              </div>

              <!-- Year Content -->
              <div
                v-if="expandedYearsDisplay.includes(year)"
                class="p-4 bg-white"
              >
                <div
                  v-if="getCoursesByYearLevel(year).length > 0"
                  class="grid grid-cols-1 md:grid-cols-2 gap-3"
                >
                  <div
                    v-for="assignment in getCoursesByYearLevel(year)"
                    :key="assignment.id"
                    class="p-3 border border-gray-200 rounded-lg hover:border-green-400 transition-colors"
                  >
                    <p class="font-semibold text-sm text-gray-800">
                      {{ assignment.course?.course_code }}
                    </p>
                    <p class="text-xs text-gray-600 mt-1">
                      {{ assignment.course?.course_description }}
                    </p>
                    <p class="text-xs text-gray-500 mt-1">
                      Curriculum:
                      {{ assignment.course?.curriculum?.curriculum_name }}
                    </p>
                  </div>
                </div>
                <div v-else class="text-center py-6 text-gray-500 text-sm">
                  <p>No courses assigned for this year level yet.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Courses Assigned Message -->
      <div
        v-else-if="userProgram && !loading && assignedCourses.length === 0"
        class="mt-4 border p-8 rounded-xl bg-white shadow-sm text-center"
      >
        <icon name="question" class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-500">
          No courses assigned to year levels for {{ activeSchoolYearName }} yet.
        </p>
        <p class="text-sm text-gray-400 mt-2">
          Click "Assign Courses" to assign courses to each year level.
        </p>
        <button
          @click="openAssignCoursesModal"
          class="mt-4 px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
        >
          <icon name="setting" class="w-5 h-5 inline mr-2" />
          Assign Courses Now
        </button>
      </div>
    </div>
  </div>

  <!-- Add Year/Section Modal -->
  <addYearSection
    v-if="showYearSectionModal && userProgram"
    :programData="userProgram"
    @close="closeYearSectionModal"
    @refresh="loadUserProgram"
  />

  <!-- Assign Year Courses Modal -->
  <assignYearCourses
    v-if="showAssignCoursesModal && userProgram"
    :programData="userProgram"
    @close="closeAssignCoursesModal"
    @refresh="loadAssignedCourses"
  />
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import addYearSection from "./modals/add-year-section.vue";
import assignYearCourses from "./modals/assign-year-courses.vue";
import axios from "axios";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState } from "pinia";

export default {
  name: "AddYearSectionPage",
  components: { icon, addYearSection, assignYearCourses },
  data() {
    return {
      showYearSectionModal: false,
      showAssignCoursesModal: false,
      userProgram: null,
      user: null,
      loading: true,
      classes: [],
      schoolYears: [],
      activeSchoolYearId: null,
      assignedCourses: [],
      expandedYearsDisplay: [1, 2, 3, 4], // All expanded by default
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["year"]),
    activeSchoolYearName() {
      const activeSchoolYear = this.schoolYears.find((sy) => sy.is_active);
      return activeSchoolYear
        ? `${activeSchoolYear.school_year_name} - ${this.getSemesterLabel(
            activeSchoolYear.semester
          )}`
        : "Current School Year";
    },
    filteredClasses() {
      if (!this.userProgram || !this.activeSchoolYearId) return [];

      return this.classes.filter(
        (cls) =>
          String(cls.program_id) === String(this.userProgram.program_id) &&
          String(cls.school_year_id) === String(this.activeSchoolYearId)
      );
    },
  },
  watch: {
    year() {
      // Refresh when school year changes in topbar
      this.loadActiveSchoolYear();
      this.loadClasses();
      this.loadAssignedCourses();
    },
  },
  methods: {
    async fetchUser() {
      try {
        const response = await axios.get("http://localhost:8000/auth/me", {
          withCredentials: true,
        });
        if (response.data) {
          this.user = response.data;
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },
    async loadUserProgram() {
      try {
        this.loading = true;
        const response = await axios.get(
          "http://localhost:8000/programs/get-programs"
        );
        const programs = response.data;

        // Filter to get user's program
        if (this.user) {
          if (this.user.role === "Program Chairperson") {
            this.userProgram = programs.find(
              (p) =>
                String(p.institute?.institute_id) ===
                  String(this.user.institute_id) &&
                String(p.program_id) === String(this.user.program_id)
            );
          } else if (this.user.role === "Admin") {
            // For admin, could show all programs or let them select
            // For now, show a message that they should use Programs page
            toast.info(
              "Admins should use the Programs page to add year/sections"
            );
            this.$router.push("/programs");
          }
        }
      } catch (error) {
        console.error("Failed to load program:", error);
        toast.error("Failed to load program information");
      } finally {
        this.loading = false;
      }
    },
    async loadClasses() {
      try {
        const response = await axios.get(
          "http://localhost:8000/class/get-classes"
        );
        this.classes = response.data;
      } catch (error) {
        console.error("Failed to load classes:", error);
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
    async loadActiveSchoolYear() {
      await this.loadSchoolYears();
      const activeSchoolYear = this.schoolYears.find((sy) => sy.is_active);
      if (activeSchoolYear) {
        this.activeSchoolYearId = activeSchoolYear.school_year_id;
      }
    },
    getSemesterLabel(semester) {
      if (semester === 1) return "1st Semester";
      if (semester === 2) return "2nd Semester";
      return "";
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
    toggleYearDisplay(year) {
      const index = this.expandedYearsDisplay.indexOf(year);
      if (index > -1) {
        this.expandedYearsDisplay.splice(index, 1);
      } else {
        this.expandedYearsDisplay.push(year);
      }
    },
    getCoursesByYearLevel(yearLevel) {
      return this.assignedCourses.filter(
        (assignment) => assignment.year_level === yearLevel
      );
    },
    async loadAssignedCourses() {
      if (!this.userProgram || !this.activeSchoolYearId) return;

      try {
        const response = await axios.get(
          "http://localhost:8000/program-year-courses/get-by-program-and-school-year",
          {
            params: {
              program_id: this.userProgram.program_id,
              school_year_id: this.activeSchoolYearId,
            },
          }
        );
        this.assignedCourses = response.data;
      } catch (error) {
        console.error("Failed to load assigned courses:", error);
      }
    },
    openYearSectionModal() {
      this.showYearSectionModal = true;
    },
    closeYearSectionModal() {
      this.showYearSectionModal = false;
      this.loadClasses(); // Refresh classes after closing modal
    },
    openAssignCoursesModal() {
      this.showAssignCoursesModal = true;
    },
    closeAssignCoursesModal() {
      this.showAssignCoursesModal = false;
      this.loadAssignedCourses(); // Refresh assigned courses after closing modal
    },
  },
  async mounted() {
    await this.fetchUser();
    await this.loadUserProgram();
    await this.loadActiveSchoolYear();
    await this.loadClasses();
    await this.loadAssignedCourses();
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>

