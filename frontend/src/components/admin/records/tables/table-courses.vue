<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between">
      <div class="text-[13px] text-text mt-4">Pages / Courses</div>
      <div class="flex items-center gap-2">
        <div
          @click="refreshTable"
          class="flex items-center gap-2 px-3 py-2 bg-blue-800 text-white rounded-xl shadow-sm hover:shadow-md border border-blue-800 hover:bg-white hover:text-blue-800 transition-all duration-300 cursor-pointer"
        >
          <div
            class="flex items-center justify-center w-5 h-5 bg-white rounded-full group-hover:bg-white transition-colors duration-300"
          >
            <icon
              :name="'refresh'"
              class="w-5 h-5 text-blue-800 transition-colors duration-300 group-hover:text-blue-600"
            />
          </div>
          <span class="font-medium text-sm">Refresh</span>
        </div>

        <div
          @click="isUploadModal = true"
          class="flex items-center gap-2 px-3 py-2 bg-defaultGreen text-white rounded-xl shadow-sm hover:shadow-md border border-defaultGreen hover:bg-white hover:text-defaultGreen transition-all duration-300 cursor-pointer"
        >
          <div
            class="flex items-center justify-center w-5 h-5 bg-white rounded-full group-hover:bg-green-100 transition-colors duration-300"
          >
            <icon
              :name="'upload'"
              class="w-5 h-5 text-defaultGreen transition-colors duration-300 group-hover:text-green-600"
            />
          </div>
          <span class="font-medium text-sm">Upload Course</span>
        </div>

        <div
          @click="toggleAdd"
          class="flex items-center gap-2 px-3 py-2 bg-defaultGreen text-white rounded-xl shadow-sm hover:shadow-md border border-defaultGreen hover:bg-white hover:text-defaultGreen transition-all duration-300 cursor-pointer"
        >
          <div
            class="flex items-center justify-center w-5 h-5 bg-white rounded-full group-hover:bg-green-100 transition-colors duration-300"
          >
            <icon
              :name="'circle-add'"
              class="w-4 h-4 text-defaultGreen transition-colors duration-300 group-hover:text-green-600"
            />
          </div>
          <span class="font-medium text-sm">Add Course</span>
        </div>
      </div>
    </div>

    <!-- Controls -->
    <div class="mt-4 overflow-x-auto border p-3 rounded-xl bg-white">
      <div
        class="flex justify-between items-center flex-wrap gap-3 text-gray-700 bg-white"
      >
        <!-- Items per page -->
        <div class="flex items-center gap-2">
          <div class="relative">
            <select
              v-model.number="itemsPerPage"
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

        <!-- Filters -->
        <div class="flex items-center gap-3 flex-wrap">
          <!-- Curriculum Filter -->
          <div class="relative">
            <select
              v-model="selectedCurriculum"
              class="appearance-none rounded-full border border-green-600 bg-white px-4 py-2 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
              @change="changePage(1)"
            >
              <option value="">All Curriculums</option>
              <option
                v-for="(curr, idx) in uniqueCurriculums"
                :key="idx"
                :value="curr"
              >
                {{ curr }}
              </option>
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

          <!-- Search -->
          <div class="relative">
            <input
              v-model="searchQuery"
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
      </div>

      <!-- Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <!-- Scrollable body wrapper -->
        <div class="max-h-[65vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead
              class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
            >
              <tr>
                <th class="px-4 py-3 text-left">Course Code</th>
                <th class="px-4 py-3 text-left">Course Title</th>
                <th class="px-4 py-3 text-center">Semester</th>
                <th class="px-4 py-3 text-center">Year Level</th>
                <th class="px-4 py-3 text-center">Lecture</th>
                <th class="px-4 py-3 text-center">Lab</th>
                <th class="px-4 py-3 text-center">Units</th>
                <th class="px-4 py-3 text-center">Pre-requisite</th>
                <th class="px-4 py-3 text-center rounded-tr-lg">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="c in paginatedData"
                :key="c.course_id"
                class="hover:bg-green-50 transition-all border-t"
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
                <td class="px-4 py-3">
                  <div class="flex justify-center gap-2">
                    <button
                      class="px-3 py-1 border border-green-300 hover:bg-green-200 text-green-800 rounded-lg flex items-center gap-1"
                      @click="toggleEdit(c)"
                    >
                      <icon name="edit" /> Edit
                    </button>
                    <button
                      class="px-3 py-1 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                      @click="toggleDelete(c)"
                    >
                      <icon name="delete" /> Delete
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="paginatedData.length === 0">
                <td colspan="11" class="text-center py-8 text-gray-400">
                  No records found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-gray-700">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredData.length }} entries
        </div>
        <div class="flex items-center">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400"
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
            class="px-3 py-1 mx-1 rounded-md hover:bg-green-300"
          >
            {{ page }}
          </button>
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
  </div>

  <!-- Add / Edit Modals -->
  <addCourses v-if="isAddCourses" @close="closeView" @refresh="loadCourses" />
  <addCourses
    v-if="showEditModal && selectedCourse"
    :courseData="selectedCourse"
    @close="closeModal"
    @refresh="loadCourses"
  />
  <uploadCourses
    v-if="isUploadModal"
    @close="isUploadModal = false"
    @refresh="loadCourses"
  />

  <!-- Delete Confirmation -->
  <div v-if="showDeleteModal" class="fixed inset-0 z-50">
    <div class="absolute inset-0 bg-gray-800 bg-opacity-40"></div>
    <div
      class="rounded-xl border w-[300px] md:w-[400px] bg-white py-6 px-4 flex flex-col items-center absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
    >
      <div
        class="rounded-full w-16 h-16 md:w-20 md:h-20 flex justify-center items-center bg-red-300 animate-pulse"
      >
        <icon
          name="question"
          class="w-8 h-8 md:w-10 md:h-10 text-white flex justify-center items-center"
        />
      </div>
      <h1 class="text-[14px] md:text-[16px] font-semibold mt-4">
        Delete Confirmation
      </h1>
      <p class="mt-2 text-[12px] md:text-[13px] text-center px-8">
        Are you sure you want to delete this record? This action cannot be
        undone.
      </p>
      <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>
      <div class="tracking-wide flex gap-2 mt-4">
        <button
          class="bg-red-400 p-2 px-3 text-[11px] md:text-[13px] rounded-md text-white hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md"
          @click="showDeleteModal = false"
        >
          No, Cancel
        </button>
        <button
          class="bg-green-400 p-2 px-3 text-[11px] md:text-[13px] rounded-md text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
          @click="confirmDelete"
        >
          Yes, Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import addCourses from "../modals/add-courses.vue";
import uploadCourses from "../modals/upload-course.vue";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

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
      isEdit: false,
      isTable: true,
      isUploadData: false,
      isUploadModal: false,
      showDeleteModal: false,
      recordToDelete: null,
      selectedCourse: null,
      showEditModal: false,
      user: null,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, [
      "courses",
      "year",

      "activeYear",
      "curriculums",
    ]),
    uniqueCurriculums() {
      // Get all program names from course curricula
      const names = this.filteredCourses.map(
        (c) => c.curriculum?.program?.program_name
      );
      return [...new Set(names.filter(Boolean))];
    },

    filteredCourses() {
      let result = this.courses || [];
      const currentUser = this.user;

      // 🔹 Filter by Program Chairperson's institute & program
      if (currentUser?.role === "Program Chairperson") {
        result = result.filter(
          (c) =>
            String(c.curriculum?.program?.institute?.institute_id) ===
              String(currentUser.institute_id) &&
            String(c.curriculum?.program_id) === String(currentUser.program_id)
        );
      }

      // 🔹 Filter by Active Year and Semester using curriculum info
      if (this.activeYear?.is_active) {
        result = result.filter(
          (c) =>
            String(c.curriculum?.curriculum_start_year) ===
              String(this.activeYear.start_year) &&
            String(c.curriculum?.curriculum_end_year) ===
              String(this.activeYear.end_year) &&
            Number(c.course_semester) === Number(this.activeYear.semester)
        );
      }

      // Filter by selected curriculum (program name)
      if (this.selectedCurriculum && this.selectedCurriculum !== "") {
        result = result.filter(
          (c) => c.curriculum?.program?.program_name === this.selectedCurriculum
        );
      }

      // 🔹 Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(
          (c) =>
            c.course_code?.toLowerCase().includes(query) ||
            c.course_title?.toLowerCase().includes(query) ||
            c.curriculum?.curriculum_name?.toLowerCase().includes(query)
        );
      }

      console.log("Filtered Courses:", result); // 🔹 Log filtered courses

      return result;
    },

    filteredData() {
      return this.filteredCourses;
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredData.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;
    },

    pageNumbers() {
      const total = this.totalPages;
      if (total <= 3) return Array.from({ length: total }, (_, i) => i + 1);

      let start = this.currentPage - 1;
      let end = this.currentPage + 1;

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

    startIndex() {
      return this.filteredData.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      const end = this.currentPage * this.itemsPerPage;
      return Math.min(end, this.filteredData.length);
    },
  },

  methods: {
    async refreshTable() {
      const store = useFetchDataStore();
      try {
        await store.fetchActiveYears(); // refresh active year
        await this.loadCourses(); // refresh courses
        this.currentPage = 1;
        toast.success("Table refreshed successfully");
      } catch (error) {
        console.error("Failed to refresh table:", error);
        toast.error("Failed to refresh table");
      }
    },
    async loadCourses() {
      const store = useFetchDataStore();
      await store.fetchCourses();
    },

    async fetchCurriculums() {
      const store = useFetchDataStore();
      try {
        await store.fetchCurriculums(); // Fetch curriculum data from the store
        console.log("Curriculums:", store.curriculums); // Log to console
      } catch (error) {
        console.error("Failed to fetch curriculums:", error);
      }
    },
    async fetchUser() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          }
        );
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

    toggleAdd() {
      this.isAddCourses = true;
      this.isTable = true;
    },

    toggleEdit(item) {
      this.selectedCourse = item;
      this.showEditModal = true;
    },

    toggleDelete(item) {
      this.recordToDelete = item;
      this.showDeleteModal = true;
    },

    confirmDelete() {
      if (!this.recordToDelete || isNaN(this.recordToDelete.course_id)) {
        toast.error("Invalid course ID.");
        return;
      }
      axios
        .delete(
          process.env.VUE_APP_API_BASE_URL +
            `/courses/delete-id/${this.recordToDelete.course_id}`
        )
        .then(() => {
          this.showDeleteModal = false;
          this.recordToDelete = null;
          this.loadCourses();
          toast.success("Record deleted successfully");
        })
        .catch(() => toast.error("Failed to delete record"));
    },

    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },

    closeView() {
      this.isAddCourses = false;
      this.isUploadData = false;
    },

    closeModal() {
      this.showEditModal = false;
      this.selectedCourse = null;
    },
  },

  watch: {
    // 🔹 Watch activeYear in store
    activeYear: {
      async handler(newVal, oldVal) {
        if (newVal && newVal !== oldVal) {
          await this.loadCourses();
          this.currentPage = 1;
        }
      },
      immediate: true,
    },
  },

  async mounted() {
    await this.fetchUser();
    await this.loadCourses();
    await this.fetchCurriculums();
  },

  beforeUnmount() {
    const store = useFetchDataStore();
    store.stopActiveYearPolling(); // Stop polling when component unmounts
  },
};
</script>
