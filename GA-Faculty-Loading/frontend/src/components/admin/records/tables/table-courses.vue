<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4">Pages / Courses</div>
      <div class="flex items-center gap-2">
        <!-- Upload & Add -->
        <div
          @click="isUploadModal = true"
          class="flex items-center gap-2 px-3 py-2 border bg-blue-700 text-white border-blue-700 rounded-xl hover:bg-white hover:text-blue-700 hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-blue-500 bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon name="uploads" />
          </div>
          <span class="font-medium text-sm">Upload Course</span>
        </div>

        <div
          @click="toggleAdd"
          class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon name="circle-add" />
          </div>

          <span class="font-medium text-sm">Add Course</span>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="mt-4 overflow-x-auto border p-3 rounded-xl bg-white">
      <!-- Top Controls -->
      <div
        class="flex justify-between items-center flex-wrap gap-3 text-gray-700 bg-white"
      >
        <!-- Items per page -->
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
        <div class="flex gap-2">
          <!-- Curriculum filter -->
          <div class="relative" v-if="user?.role === 'Admin'">
            <select
              v-model="selectedCurriculum"
              @change="currentPage = 1"
              class="rounded-full border border-green-600 px-4 py-1.5 text-green-900 text-sm font-semibold shadow-sm cursor-pointer"
            >
              <option value="">All Curriculums</option>
              <option
                v-for="curr in uniqueCurriculums"
                :key="curr"
                :value="curr"
              >
                {{ curr }}
              </option>
            </select>
          </div>

          <!-- Search input -->
          <div class="relative w-full sm:w-[280px]">
            <input
              v-model="searchQuery"
              @input="currentPage = 1"
              type="text"
              placeholder="Search courses..."
              class="rounded-full border border-green-600 px-4 py-2 pl-10 text-sm shadow-sm w-full"
            />
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
      </div>

      <!-- Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[69vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead
              class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
            >
              <tr>
                <th class="px-4 py-3 text-left font-normal">Course Code</th>
                <th class="px-4 py-3 text-left font-normal">Course Title</th>
                <th class="px-4 py-3 text-center font-normal">Semester</th>
                <th class="px-4 py-3 text-center font-normal">Year Level</th>
                <th class="px-4 py-3 text-center font-normal">Lecture</th>
                <th class="px-4 py-3 text-center font-normal">Lab</th>
                <th class="px-4 py-3 text-center font-normal">Units</th>
                <th class="px-4 py-3 text-center font-normal">Pre-requisite</th>
                <th class="px-4 py-3 text-center rounded-tr-lg font-normal">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="c in paginatedData"
                :key="c.course_id"
                class="hover:bg-green-50 border-t transition-all"
              >
                <td class="px-4 py-3">{{ c.course_code }}</td>
                <td class="px-4 py-3">{{ c.course_title }}</td>
                <td class="px-4 py-3 text-center">{{ c.course_semester }}</td>
                <td class="px-4 py-3 text-center">{{ c.course_level }}</td>
                <td class="px-4 py-3 text-center">{{ c.course_lec }}</td>
                <td class="px-4 py-3 text-center">{{ c.course_lab }}</td>
                <td class="px-4 py-3 text-center">
                  {{ c.course_lec + c.course_lab }}
                </td>
                <td class="px-4 py-3 text-center">
                  {{ c.course_requisite || "-" }}
                </td>
                <td class="px-4 py-3 flex justify-center">
                  <div class="flex gap-2">
                    <button
                      class="w-[90px] h-8 border border-green-300 hover:bg-green-200 text-defaultGreen rounded-lg flex items-center justify-center gap-1"
                      @click="toggleEdit(c)"
                    >
                      <icon name="edit" /> Edit
                    </button>
                    <button
                      class="px-3 py-1 h-8 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                      @click="toggleDelete(c)"
                    >
                      <icon name="delete" /> Delete
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="paginatedData.length === 0">
                <td colspan="9" class="text-center py-8 text-gray-400">
                  No records found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-gray-700 text-sm">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredCourses.length }} entries
        </div>
        <div class="flex items-center gap-1 text-sm">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 rounded-l-md hover:bg-gray-400"
          >
            &lt;
          </button>
          <button
            v-for="page in pageNumbers"
            :key="'page-' + page"
            @click="changePage(page)"
            :class="{
              'bg-defaultGreen text-white': currentPage === page,
              'bg-gray-200 text-gray-700': currentPage !== page,
            }"
            class="px-3 py-1 rounded-md hover:bg-green-300"
          >
            {{ page }}
          </button>
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 bg-gray-300 rounded-r-md hover:bg-gray-400"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Add/Edit/Upload Modals -->

  <addCourses
    v-if="(showEditModal && selectedCourse) || isAddCourses"
    :courseData="selectedCourse"
    @close="closeModal"
    @refresh="loadCourses"
  />
  <uploadCourses
    v-if="isUploadModal"
    @close="isUploadModal = false"
    @refresh="loadCourses"
  />
</template>

<script>
import icon from "@/assets/icon.vue";
import addCourses from "../modals/add-courses.vue";
import uploadCourses from "../modals/upload-course.vue";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";
import { eventBus } from "@/bus/event-bus";

export default {
  name: "TableCourses",
  components: { icon, addCourses, uploadCourses },

  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      selectedCurriculum: "",
      isAddCourses: false,
      isTable: true,
      isUploadModal: false,
      showEditModal: false,
      selectedCourse: null,
      user: null,
      activeSchoolYear: null,
      stopEventBus: null,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["courses", "activeYear"]),

    uniqueCurriculums() {
      const names = this.courses
        .map((c) => c.curriculum?.program?.program_name)
        .filter(Boolean);
      return [...new Set(names)];
    },

    filteredCourses() {
      let result = this.courses || [];

      if (this.user?.role === "Program Chairperson") {
        result = result.filter(
          (c) =>
            String(c.curriculum?.program?.institute?.institute_id) ===
              String(this.user.institute_id) &&
            String(c.curriculum?.program_id) === String(this.user.program_id),
        );
      }

      if (this.activeSchoolYear) {
        result = result.filter(
          (c) =>
            String(c.curriculum?.curriculum_start_year) ===
              String(this.activeSchoolYear.start_year) &&
            String(c.curriculum?.curriculum_end_year) ===
              String(this.activeSchoolYear.end_year) &&
            Number(c.course_semester) ===
              Number(this.activeSchoolYear.semester),
        );
      }

      if (this.selectedCurriculum) {
        result = result.filter(
          (c) =>
            c.curriculum?.program?.program_name === this.selectedCurriculum,
        );
      }

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        result = result.filter(
          (c) =>
            c.course_code?.toLowerCase().includes(q) ||
            c.course_title?.toLowerCase().includes(q) ||
            c.curriculum?.curriculum_name?.toLowerCase().includes(q),
        );
      }

      return result;
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredCourses.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredCourses.length / this.itemsPerPage) || 1;
    },

    pageNumbers() {
      const total = this.totalPages;
      if (total <= 3) return Array.from({ length: total }, (_, i) => i + 1);
      let start = this.currentPage - 1;
      let end = this.currentPage + 1;
      if (start < 1) start = 1;
      if (end > total) end = total;
      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    },

    startIndex() {
      return this.filteredCourses.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(
        this.currentPage * this.itemsPerPage,
        this.filteredCourses.length,
      );
    },
  },

  methods: {
    async fetchUser() {
      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/auth/me`,
          { withCredentials: true },
        );
        this.user = res.data || null;
      } catch {
        this.$router.push("/");
      }
    },

    async loadCourses() {
      const store = useFetchDataStore();
      await store.fetchCourses();
    },

    toggleAdd() {
      this.selectedCourse = null;
      this.showEditModal = false;
      this.isAddCourses = true;
    },
    toggleEdit(course) {
      this.isAddCourses = false;
      this.selectedCourse = course;
      this.showEditModal = true;
    },
    closeModal() {
      this.isAddCourses = false;
      this.showEditModal = false;
      this.selectedCourse = null;
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
  },

  mounted() {
    this.fetchUser();
    this.loadCourses();

    this.stopEventBus = eventBus.on((newYear) => {
      if (!newYear) return;
      this.activeSchoolYear = newYear;
      this.currentPage = 1;
      this.loadCourses();
    });
  },

  beforeUnmount() {
    this.stopEventBus?.();
  },
};
</script>
