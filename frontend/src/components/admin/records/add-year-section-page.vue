<template>
  <div class="p-4 md:p-6 space-y-6 text-[13px]">
    <!-- HEADER -->
    <!-- <div
      class="flex items-center justify-between bg-gradient-to-r from-green-600 to-green-500 text-white px-5 py-3 rounded-xl shadow-sm"
    >
      <h1 class="text-lg font-semibold tracking-wide">
        Year & Section Management
      </h1>
      <div class="flex gap-2">
        <button
          @click="openYearSectionModal"
          class="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all"
        >
          <icon name="add-students" class="w-4 h-4" />
          <span class="text-sm font-medium">Add Section</span>
        </button>
        <button
          @click="openAssignCoursesModal"
          class="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all"
        >
          <icon name="setting" class="w-4 h-4" />
          <span class="text-sm font-medium">Assign Courses</span>
        </button>
      </div>
    </div> -->

    <!-- MAIN CONTENT -->
    <div class="space-y-6">
      <!-- Program Card -->
      <div
        v-if="userProgram"
        class="bg-white border border-green-100 p-5 rounded-2xl shadow-sm hover:shadow-md transition-all"
      >
        <div
          class="flex flex-col md:flex-row md:items-center md:justify-between gap-3"
        >
          <!-- Program Info -->
          <div>
            <h2 class="text-lg font-bold text-gray-800">
              {{ userProgram.program_name }}
            </h2>
            <div class="text-sm text-gray-600">
              <p>Code: {{ userProgram.program_code }}</p>
              <p v-if="userProgram.institute">
                Institute: {{ userProgram.institute.institute_name }}
              </p>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="flex gap-3">
            <button
              @click="openYearSectionModal"
              class="flex items-center gap-2 px-4 py-2 bg-defaultGreen text-white rounded-lg shadow-sm hover:bg-green-700 transition"
            >
              <icon name="add-students" class="w-4 h-4" />
              <span>Add Year/Section</span>
            </button>
            <button
              @click="openAssignCoursesModal"
              class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg shadow-sm hover:bg-blue-700 transition"
            >
              <icon name="setting" class="w-4 h-4" />
              <span>Assign Courses</span>
            </button>
          </div>
        </div>

        <!-- Instructions -->
        <div class="mt-5 bg-blue-50 border border-blue-100 p-4 rounded-lg">
          <h3 class="font-semibold text-sm text-blue-900 mb-2">Instructions</h3>
          <ul class="text-xs text-blue-700 list-disc list-inside space-y-1">
            <li>Click "Add Year/Section" to configure sections.</li>
            <li>Select the school year for the new sections.</li>
            <li>Set number of sections for each year level (1st–4th).</li>
            <li>Define the class size for each section.</li>
            <li>Sections will be automatically named (A, B, C, etc.).</li>
          </ul>
        </div>
      </div>

      <!-- Loading State -->
      <div
        v-else-if="loading"
        class="bg-white border p-8 rounded-xl shadow-sm text-center"
      >
        <p class="text-gray-500 animate-pulse">
          Loading program information...
        </p>
      </div>

      <!-- No Program Found -->
      <div v-else class="bg-white border p-8 rounded-xl shadow-sm text-center">
        <icon name="question" class="w-14 h-14 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-600 font-medium">
          No program found for your account.
        </p>
        <p class="text-sm text-gray-400 mt-1">
          Please contact the administrator.
        </p>
      </div>

      <!-- SECTIONS TABLE -->
      <div
        v-if="userProgram && filteredClasses.length > 0"
        class="bg-white border p-5 rounded-2xl shadow-sm"
      >
        <div class="flex justify-between items-center mb-3">
          <h3 class="font-semibold text-gray-800">
            Created Sections – {{ activeSchoolYearName }}
          </h3>
          <span class="text-xs text-gray-500">
            {{ filteredClasses.length }} section(s)
          </span>
        </div>

        <div class="overflow-x-auto rounded-lg border">
          <table class="min-w-full text-sm">
            <thead class="bg-defaultGreen text-white text-left">
              <tr>
                <th class="px-4 py-2 rounded-tl-lg">#</th>
                <th class="px-4 py-2">Section Name</th>
                <th class="px-4 py-2 text-center">Class Size</th>
                <th class="px-4 py-2 rounded-tr-lg">School Year</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(cls, index) in filteredClasses"
                :key="cls.class_id"
                class="border-b hover:bg-green-50 transition-colors"
              >
                <td class="px-4 py-2">{{ index + 1 }}</td>
                <td class="px-4 py-2 font-medium">{{ cls.set_name }}</td>
                <td class="px-4 py-2 text-center">{{ cls.class_size }}</td>
                <td class="px-4 py-2">
                  {{ cls.schoolYear?.school_year_name }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- NO SECTIONS -->
      <div
        v-else-if="userProgram && !loading && filteredClasses.length === 0"
        class="bg-white border p-8 rounded-xl shadow-sm text-center"
      >
        <p class="text-gray-600">
          No sections created for {{ activeSchoolYearName }} yet.
        </p>
        <p class="text-sm text-gray-400 mt-1">
          Click "Add Year/Section" to create sections.
        </p>
      </div>

      <!-- ASSIGNED COURSES -->
      <div
        v-if="userProgram && assignedCourses.length > 0"
        class="bg-white border p-5 rounded-2xl shadow-sm"
      >
        <div class="flex justify-between items-center mb-3">
          <h3 class="font-semibold text-gray-800">
            Assigned Courses – {{ activeSchoolYearName }}
          </h3>
          <button
            @click="openAssignCoursesModal"
            class="px-3 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition"
          >
            <icon name="setting" class="w-4 h-4 inline mr-1" />
            Edit
          </button>
        </div>

        <div class="space-y-3">
          <div
            v-for="year in [1, 2, 3, 4]"
            :key="year"
            class="border rounded-lg overflow-hidden"
          >
            <!-- Year Header -->
            <div
              @click="toggleYearDisplay(year)"
              class="flex justify-between items-center p-3 bg-gray-50 hover:bg-gray-100 cursor-pointer transition"
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
                <h4 class="font-semibold text-sm text-gray-800">
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
            <transition name="fade">
              <div
                v-if="expandedYearsDisplay.includes(year)"
                class="p-4 bg-white"
              >
                <div
                  v-if="getCoursesByYearLevel(year).length > 0"
                  class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3"
                >
                  <div
                    v-for="assignment in getCoursesByYearLevel(year)"
                    :key="assignment.id"
                    class="p-3 border rounded-lg hover:border-green-400 transition"
                  >
                    <p class="font-medium text-gray-800">
                      {{ assignment.course?.course_code }}
                    </p>
                    <p class="text-xs text-gray-600 mt-1">
                      {{ assignment.course?.course_description }}
                    </p>
                    <p class="text-xs text-gray-500 mt-1 italic">
                      {{ assignment.course?.curriculum?.curriculum_name }}
                    </p>
                  </div>
                </div>
                <div v-else class="py-6 text-center text-gray-500 text-sm">
                  No courses assigned for this year level.
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- NO ASSIGNED COURSES -->
      <div
        v-else-if="userProgram && !loading && assignedCourses.length === 0"
        class="bg-white border p-8 rounded-xl shadow-sm text-center"
      >
        <icon name="question" class="w-14 h-14 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-600">
          No courses assigned to year levels for {{ activeSchoolYearName }} yet.
        </p>
        <p class="text-sm text-gray-400 mt-1">
          Click "Assign Courses" to start assigning.
        </p>
        <button
          @click="openAssignCoursesModal"
          class="mt-4 px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition"
        >
          <icon name="setting" class="w-5 h-5 inline mr-2" />
          Assign Courses Now
        </button>
      </div>
    </div>
  </div>

  <!-- MODALS -->
  <addYearSection
    v-if="showYearSectionModal && userProgram"
    :programData="userProgram"
    @close="closeYearSectionModal"
    @refresh="loadUserProgram"
  />
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
import addYearSection from "../../program-chairperson/program-record/modals/add-year-section.vue";
import assignYearCourses from "../../program-chairperson/program-record/modals/assign-year-courses.vue";
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
