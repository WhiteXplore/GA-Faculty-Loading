<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mt-6 mb-2">
      <div class="text-[13px] text-gray-700">
        Pages / Class & Assigned Courses
      </div>
      <span class="text-sm bg-defaultGreen text-white px-3 py-1 rounded-full">
        {{ filteredClasses.length }} Classes
      </span>
    </div>

    <!-- Classes with Courses Section -->
    <div class="overflow-x-auto border p-3 rounded-xl bg-white">
      <!-- Controls -->
      <div
        class="flex justify-between items-center flex-wrap gap-3 text-gray-700 bg-white"
      >
        <div class="flex justify-between items-center gap-4 w-full rounded-lg">
          <div class="flex items-center gap-2">
            <div class="relative">
              <select
                v-model="itemsPerPage"
                class="appearance-none rounded-full border border-green-600 bg-white px-3 py-1 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
                @change="changePage(1)"
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
            <span class="text-sm font-medium">Per page</span>
          </div>
          <div class="relative">
            <input
              v-model="classSearch"
              type="text"
              placeholder="Search..."
              class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full sm:w-[280px] transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
              @input="changePage(1)"
            />
            <!-- Search icon -->
            <div
              class="absolute inset-y-0 left-3 flex items-center text-green-700 pointer-events-none"
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

        <!-- Table -->
        <div class="w-full mt-1 rounded-xl border bg-white overflow-hidden">
          <div class="max-h-[69vh] overflow-y-auto">
            <table class="min-w-full text-sm text-gray-700 border-collapse">
              <thead
                class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
              >
                <tr>
                  <th class="px-4 py-3 text-left font-semibold w-[10%]">
                    Year & Section
                  </th>
                  <th class="px-4 py-3 text-left font-semibold w-[20%]">
                    Program
                  </th>
                  <th class="px-4 py-3 text-center font-semibold w-[10%]">
                    Class Size
                  </th>
                  <th class="px-4 py-3 text-center font-semibold w-[15%]">
                    School Year
                  </th>
                  <th class="px-4 py-3 text-center font-semibold w-[15%]">
                    Assigned Courses
                  </th>
                </tr>
              </thead>

              <!-- Table Body -->
              <tbody>
                <tr
                  v-for="cls in paginatedClasses"
                  :key="cls.class_id"
                  class="hover:bg-green-50 transition-all border-t"
                >
                  <!-- <td class="px-4 py-3 text-gray-600">
                    {{ classStartIndex + index }}
                  </td> -->
                  <td class="px-4 py-3 text-gray-800 text-left">
                    {{ cls.set_name }}
                  </td>
                  <td class="px-4 py-3">
                    {{ cls.program?.program_name || "N/A" }}
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span
                      class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full"
                    >
                      {{ cls.class_size }} students
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center">
                    {{ cls.schoolYear?.school_year_name || "N/A" }}
                  </td>
                  <td class="px-4 py-3 flex justify-center items-center">
                    <button
                      @click="showClassCourses(cls)"
                      class="px-3 py-2 h-8 border border-blue-300 hover:bg-blue-200 text-blue-800 rounded-lg flex items-center gap-1"
                    >
                      <icon name="eye" /> View
                    </button>
                  </td>
                </tr>

                <!-- Empty State -->
                <tr v-if="filteredClasses.length === 0">
                  <td colspan="6" class="px-4 py-8 text-center text-gray-500">
                    No classes found
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pagination -->
        <div class="flex justify-between items-center mt-4 w-full">
          <div class="text-gray-700 text-sm">
            Showing {{ classStartIndex }} to {{ classEndIndex }} of
            {{ filteredClasses.length }} entries
          </div>

          <div class="flex items-center gap-1 text-sm">
            <!-- Prev -->
            <button
              @click="changePage(classPage - 1)"
              :disabled="classPage === 1"
              class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400 disabled:opacity-50"
            >
              &lt;
            </button>

            <!-- Page Numbers -->
            <span v-for="page in paginatedNumbers" :key="'page-' + page">
              <button
                @click="changePage(page)"
                :class="{
                  'bg-defaultGreen text-white': classPage === page,
                  'bg-gray-200 text-gray-700': classPage !== page,
                }"
                class="px-3 py-1 rounded-md hover:bg-green-300"
              >
                {{ page }}
              </button>
            </span>

            <!-- Next -->
            <button
              @click="changePage(classPage + 1)"
              :disabled="classPage === classTotalPages"
              class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400 disabled:opacity-50"
            >
              &gt;
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Course Details Modal -->
    <div
      v-if="showCoursesModal"
      class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center"
      @click.self="closeCoursesModal"
    >
      <div
        class="bg-white rounded-xl shadow-2xl w-[800px] max-h-[80vh] overflow-y-auto"
      >
        <div
          class="bg-defaultGreen text-white px-6 py-4 flex justify-between items-center sticky top-0"
        >
          <h3 class="font-bold text-lg">
            Courses for {{ selectedClass?.set_name }}
          </h3>
          <button
            @click="closeCoursesModal"
            class="text-white hover:text-gray-200"
          >
            <icon name="close" class="w-6 h-6" />
          </button>
        </div>

        <div class="p-6">
          <div v-if="classCourses.length > 0" class="space-y-3">
            <div
              v-for="(course, index) in classCourses"
              :key="course.id"
              class="p-4 border border-gray-200 rounded-lg hover:border-purple-400 transition-colors"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <p class="font-bold text-gray-800">
                    {{ index + 1 }}. {{ course.course?.course_code }}
                  </p>
                  <p class="text-sm text-gray-600 mt-1">
                    {{ course.course?.course_description }}
                  </p>
                  <div class="mt-2 flex gap-4 text-xs text-gray-500">
                    <span
                      >Year Level:
                      {{ getYearLevelLabel(course.year_level) }}</span
                    >
                    <span>Lec: {{ course.course?.course_lec || 0 }} hrs</span>
                    <span>Lab: {{ course.course?.course_lab || 0 }} hrs</span>
                    <span>Units: {{ course.course?.course_credit || 0 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            <icon
              name="question"
              class="w-16 h-16 text-gray-300 mx-auto mb-4"
            />
            <p>No courses assigned to this class yet.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import axios from "axios";
import { toast } from "vue3-toastify";

export default {
  name: "TableClassAssignedCourses",
  components: { icon },
  data() {
    return {
      user: null,
      classes: [],
      classCourses: [],
      selectedClass: null,
      showCoursesModal: false,

      // Filters
      classSearch: "",
      selectedProgram: "",

      // Pagination
      classPage: 1,
      itemsPerPage: 10,

      loading: true,
    };
  },
  computed: {
    filteredClasses() {
      let result = this.classes;

      if (this.classSearch) {
        const query = this.classSearch.toLowerCase();
        result = result.filter((c) =>
          c.set_name?.toLowerCase().includes(query),
        );
      }

      if (this.selectedProgram) {
        result = result.filter(
          (c) => c.program?.program_name === this.selectedProgram,
        );
      }

      if (this.user?.role === "Program Chairperson" && this.user?.program_id) {
        result = result.filter((c) => c.program_id === this.user.program_id);
      }

      // Sort by year level and section letter
      result = result.sort((a, b) => {
        const yearA = this.extractYearLevel(a.set_name) || 0;
        const yearB = this.extractYearLevel(b.set_name) || 0;

        if (yearA !== yearB) return yearA - yearB;

        // Extract section letter (last character after dash, e.g., 'A' in '1st Year - A')
        const sectionA = a.set_name?.split("-").pop().trim() || "";
        const sectionB = b.set_name?.split("-").pop().trim() || "";

        return sectionA.localeCompare(sectionB);
      });

      return result;
    },
    paginatedNumbers() {
      const total = this.classTotalPages;

      if (total <= 3) {
        return Array.from({ length: total }, (_, i) => i + 1);
      }

      let start = this.classPage - 1;
      let end = this.classPage + 1;

      if (start < 1) {
        start = 1;
        end = 3;
      }

      if (end > total) {
        end = total;
        start = total - 2;
      }

      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    },

    paginatedClasses() {
      const start = (this.classPage - 1) * this.itemsPerPage;
      return this.filteredClasses.slice(start, start + this.itemsPerPage);
    },
    classTotalPages() {
      return Math.ceil(this.filteredClasses.length / this.itemsPerPage) || 1;
    },
    classStartIndex() {
      return this.filteredClasses.length === 0
        ? 0
        : (this.classPage - 1) * this.itemsPerPage + 1;
    },
    classEndIndex() {
      const end = this.classPage * this.itemsPerPage;
      return Math.min(end, this.filteredClasses.length);
    },
    uniquePrograms() {
      const programs = this.classes
        .map((c) => c.program?.program_name)
        .filter(Boolean);
      return [...new Set(programs)];
    },
  },
  methods: {
    changePage(page) {
      if (page < 1 || page > this.classTotalPages) return;
      this.classPage = page;
    },
    async fetchUser() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          },
        );
        this.user = res.data;
      } catch (err) {
        console.error("Failed to fetch user:", err);
      }
    },
    async loadClasses() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/class/get-classes",
        );
        this.classes = response.data;
      } catch (error) {
        console.error("Failed to load classes:", error);
        toast.error("Failed to load classes data");
      }
    },
    async showClassCourses(cls) {
      this.selectedClass = cls;
      this.showCoursesModal = true;

      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/program-year-courses/get-by-program-and-school-year",
          {
            params: {
              program_id: cls.program_id, // courses for this program
              school_year_id: cls.school_year_id,
            },
          },
        );

        const yearLevel = this.extractYearLevel(cls.set_name);

        // Filter by year level (ignore section)
        let courses = response.data.filter((c) => c.year_level === yearLevel);

        // Deduplicate by course_id
        const uniqueCoursesMap = new Map();
        courses.forEach((c) => {
          if (!uniqueCoursesMap.has(c.course.course_id)) {
            uniqueCoursesMap.set(c.course.course_id, c);
          }
        });

        this.classCourses = Array.from(uniqueCoursesMap.values());
      } catch (error) {
        console.error("Failed to load class courses:", error);
        this.classCourses = [];
      }
    },
    closeCoursesModal() {
      this.showCoursesModal = false;
      this.selectedClass = null;
      this.classCourses = [];
    },
    getYearLevelLabel(level) {
      const labels = {
        1: "1st Year",
        2: "2nd Year",
        3: "3rd Year",
        4: "4th Year",
      };
      return labels[level] || `Year ${level}`;
    },
    extractYearLevel(setName) {
      if (!setName) return null;
      const match = setName.match(/(\d+)(?:st|nd|rd|th)\s*year/i);
      return match ? parseInt(match[1]) : null;
    },
  },
  async mounted() {
    this.loading = true;
    await this.fetchUser();
    await this.loadClasses();
    this.loading = false;
  },
};
</script>
