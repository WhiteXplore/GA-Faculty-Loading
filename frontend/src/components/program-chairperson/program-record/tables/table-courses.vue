<template>
  <div v-if="isTable" class=" ">
    <div class="text-sm flex justify-between">
      <div class="text-[13px] text-text mt-4 font-regular">Pages / Courses</div>

      <div
        @click="toggleAdd"
        class="flex items-center gap-2 px-3 py-2 bg-white text-green-600 rounded-xl shadow-sm hover:shadow-md border border-green-500 hover:bg-defaultGreen hover:text-white transition-all duration-300 cursor-pointer"
      >
        <div
          class="flex items-center justify-center w-5 h-5 bg-green-100 rounded-full group-hover:bg-white transition-colors duration-300"
        >
          <icon
            :name="'circle-add'"
            class="w-4 h-4 text-green-600 transition-colors duration-300 group-hover:text-green-600"
          />
        </div>
        <span class="font-medium text-sm">Add Course</span>
      </div>
    </div>

    <div class="text-[14px] bg-white rounded-xl">
      <div class="mt-4 overflow-x-auto border p-2 rounded-xl">
        <!-- Top controls -->
        <div
          class="text-gray-700 flex justify-between items-start mt-1 flex-wrap gap-2"
        >
          <!-- Items Per Page -->
          <div class="flex items-center">
            <select
              v-model="itemsPerPage"
              class="px-1 py-1 border rounded-md"
              @change="changePage(1)"
            >
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
            </select>
            <span class="ml-2">Per page</span>
          </div>

          <!-- Curriculum Filter + Search -->
          <div class="flex items-center gap-2">
            <!-- Curriculum Filter -->
            <select
              v-model="selectedCurriculum"
              class="px-3 py-2 border rounded-md"
              @change="changePage(1)"
            >
              <option value="">All Courses</option>
              <option
                v-for="(curr, idx) in uniqueCurriculums"
                :key="idx"
                :value="curr"
              >
                {{ curr }}
              </option>
            </select>

            <!-- Search -->
            <input
              v-model="searchQuery"
              type="text"
              class="px-3 w-[250px] py-2 border rounded-md"
              placeholder="Search..."
              @input="changePage(1)"
            />
          </div>
        </div>

        <!-- Table -->
        <div class="w-full rounded-xl shadow overflow-hidden">
          <div
            class="overflow-y-auto transition-all duration-300"
            :class="tableHeightClass"
          >
            <table
              class="min-w-full table-auto border-separate border-spacing-y-2 text-sm text-gray-700"
            >
              <thead
                class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
              >
                <tr>
                  <th class="px-4 py-3 text-left rounded-tl-lg font-normal">
                    ID
                  </th>
                  <th class="px-4 py-2 text-left font-normal">Curriculum</th>
                  <th class="px-4 py-2 text-left font-normal">Course Code</th>
                  <th class="px-4 py-2 text-left font-normal">
                    Course Description
                  </th>
                  <th class="px-4 py-2 text-center font-normal">Semester</th>
                  <th class="px-4 py-2 text-center font-normal">Year Level</th>
                  <th class="px-4 py-2 text-center font-normal">
                    Lecture <br />
                    (Hours)
                  </th>
                  <th class="px-4 py-2 text-center font-normal">
                    Laboratory <br />
                    (Hours)
                  </th>
                  <th class="px-4 py-2 text-center font-normal">
                    Credit <br />
                    (Units)
                  </th>
                  <th class="px-4 py-2 text-left font-normal">Pre-requisite</th>
                  <th class="px-4 py-2 text-left rounded-tr-lg font-normal">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(courses_data, index) in paginatedData"
                  :key="courses_data.course_id"
                  class="bg-white hover:bg-green-50 transition-all border border-gray-200 rounded-md shadow-sm"
                >
                  <td class="px-4 py-2 text-left">{{ startIndex + index }}</td>
                  <td class="px-4 py-2 text-left">
                    {{ courses_data.curriculum?.curriculum_name }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    {{ courses_data.course_code }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    {{ courses_data.course_description }}
                  </td>
                  <td class="px-4 py-2 text-center">
                    {{ courses_data.course_semester }}
                  </td>
                  <td class="px-4 py-2 text-center">
                    {{ courses_data.course_level }}
                  </td>
                  <td class="px-4 py-2 text-center">
                    {{ courses_data.course_lec }}
                  </td>
                  <td class="px-4 py-2 text-center">
                    {{ courses_data.course_lab }}
                  </td>
                  <td class="px-4 py-2 text-center">
                    {{ courses_data.course_lec + courses_data.course_lab }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    {{ courses_data.course_requisite }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    <div class="flex gap-2">
                      <button
                        class="px-3 py-1 h-8 border border-green-300 hover:bg-green-200 text-green-800 rounded-lg flex items-center gap-1"
                        @click="toggleEdit(courses_data)"
                      >
                        <icon name="edit" /> Edit
                      </button>
                      <button
                        class="px-3 py-1 h-8 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                        @click="toggleDelete(courses_data)"
                      >
                        <icon name="delete" /> Delete
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="paginatedData.length === 0">
                  <td colspan="10" class="text-center py-8 text-gray-400">
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
            <span>
              Showing {{ startIndex }} to {{ endIndex }} of
              {{ filteredData.length }} entries
            </span>
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
    </div>
  </div>
  <addCourses v-if="isAddCourses" @close="closeView" @refresh="loadCourses" />
  <addCourses
    v-if="showEditModal && selectedCourse"
    :courseData="selectedCourse"
    @close="closeModal"
    @refresh="loadCourses"
  />
  <!-- Delete Confirmation Modal -->
  <div
    v-if="showDeleteModal"
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50 w-min-screen"
  ></div>
  <div
    v-if="showDeleteModal"
    class="rounded-xl shadow-lg w-[300px] md:w-[400px] bg-white py-6 px-4 flex flex-col items-center fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50"
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
      Are you sure you want to delete this record? This action cannot be undone.
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
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import addCourses from "../modals/add-courses.vue";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TableCourses",
  components: {
    icon,
    addCourses,
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      selectedCurriculum: "", // ✅ new filter
      isAddCourses: false,
      isEdit: false,
      isTable: true,
      isUploadData: false,
      showDeleteModal: false,
      recordToDelete: null,
      selectedServiceRecord: null,
      selectedCourse: null,
      showEditModal: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["courses"]),

    uniqueCurriculums() {
      const names = this.courses.map(
        (item) => item.curriculum?.curriculum_name
      );
      return [...new Set(names.filter((n) => n))];
    },

    filteredData() {
      const query = this.searchQuery.toLowerCase();
      return this.courses.filter((item) => {
        const matchesSearch =
          item.course_code?.toLowerCase().includes(query) ||
          item.course_description?.toLowerCase().includes(query) ||
          item.curriculum?.curriculum_name?.toLowerCase().includes(query);

        const matchesCurriculum =
          !this.selectedCurriculum ||
          item.curriculum?.curriculum_name === this.selectedCurriculum;

        return matchesSearch && matchesCurriculum;
      });
    },

    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredData.slice(start, start + this.itemsPerPage);
    },
    startIndex() {
      return this.filteredData.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    endIndex() {
      const end = this.currentPage * this.itemsPerPage;
      return end > this.filteredData.length ? this.filteredData.length : end;
    },
    pageNumbers() {
      return Array.from({ length: this.totalPages }, (_, i) => i + 1);
    },
    tableHeightClass() {
      const count = this.paginatedData.length;
      return count <= 10 ? "h-auto" : "h-[65vh]";
    },
  },
  methods: {
    async loadCourses() {
      const store = useFetchDataStore();
      await store.fetchCourses();
    },
    toggleUploadData() {
      this.isUploadData = true;
      this.isTable = true;
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

      const courseId = this.recordToDelete.course_id;

      axios
        .delete(`http://localhost:8000/courses/delete-id/${courseId}`)
        .then(() => {
          this.recordToDelete = null;
          this.showDeleteModal = false;
          // Play sound after successful delete
          const audio = new Audio(require("@/assets/delete.mp3"));
          audio.play();

          this.loadCourses(); // refresh the list from backend
          toast.success("Record deleted successfully");
        })
        .catch((error) => {
          console.error("Delete failed:", error);
          toast.error("Failed to delete record.");
        });
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
    handleBackToTable() {
      this.isEdit = false;
      this.isAddCourses = false;
      this.isUploadData = false;
      this.selectedServiceRecord = null;
      this.isTable = true;
    },
  },
  mounted() {
    this.loadCourses();
  },
};
</script>
