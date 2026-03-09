<template>
  <div v-if="isTable" class=" ">
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages / Prospectus
      </div>

      <div
        @click="toggleAdd"
        class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
      >
        <div
          class="flex items-center justify-center w-5 h-5 bg-white rounded-full group-hover:bg-green-100 transition-colors duration-300"
        >
          <icon
            :name="'circle-add'"
            class="w-4 h-4 text-defaultGreen transition-colors duration-300 group-hover:text-defaultGreen"
          />
        </div>
        <span class="font-medium text-sm">Generate Report</span>
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
              class="appearance-none rounded-full border border-green-600 bg-white px-3 py-1 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
              @change="changePage(1)"
            >
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
            </select>
            <!-- Custom arrow -->
            <div
              class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-defaultGreen transition-colors"
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

        <!-- Search -->
        <div class="relative w-full sm:w-64 md:w-72 lg:w-80">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search..."
            class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
            @input="changePage(1)"
          />
          <!-- Search icon -->
          <div
            class="absolute inset-y-0 left-3 flex items-center text-defaultGreen pointer-events-none transition-colors"
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
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <table class="min-w-full text-sm text-gray-700 border-collapse">
          <thead
            class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
          >
            <tr>
              <th class="w-10 px-4 py-2 text-left rounded-tl-lg font-normal">
                ID
              </th>
              <th class="px-4 py-3 text-left font-normal">Institute</th>
              <th class="px-4 py-3 text-left rounded-tr-lg font-normal">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(reportCurriculum_data, index) in paginatedData"
              :key="reportCurriculum_data.curriculum_id"
              class="hover:bg-green-50 transition-all border-t"
            >
              <td class="px-4 py-2 text-left">{{ startIndex + index }}</td>
              <td class="px-4 py-2 text-left">
                {{ reportCurriculum_data.institute_name }}
              </td>

              <td class="px-4 py-2 text-left">
                <div class="flex gap-2">
                  <router-link
                    :to="{
                      path: `/view-curriculum-offers/${reportCurriculum_data.institute_id}`,
                      query: activeSchoolYear
                        ? {
                            sy_start: activeSchoolYear.start_year,
                            sy_end: activeSchoolYear.end_year,
                            semester: activeSchoolYear.semester,
                          }
                        : {},
                    }"
                    class="px-3 py-1 h-8 border border-blue-300 hover:bg-blue-200 text-blue-800 rounded-lg flex items-center gap-1"
                  >
                    <icon name="eye" /> View
                  </router-link>
                </div>
              </td>
            </tr>
            <tr v-if="paginatedData.length === 0">
              <td colspan="5" class="text-center py-8 text-gray-400">
                No records found
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-gray-700 text-sm">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredData.length }} entries
        </div>
        <div class="flex items-center gap-1 text-sm">
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
              class="px-3 py-1 rounded-md hover:bg-green-300"
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
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";
import { eventBus } from "@/bus/event-bus";

export default {
  name: "TablePrograms",
  components: {
    icon,
  },

  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAdd: false,
      isEdit: false,
      isTable: true,
      isUploadData: false,
      showDeleteModal: false,
      recordToDelete: null,
      selectedPrograms: null,
      showEditModal: false,

      // ✅ SAME AS TableCourses
      activeSchoolYear: null,
      stopEventBus: null,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["detailedReportCurriculum", "courses"]),

    /**
     * 🔹 Filter institutes list by search
     */
    filteredData() {
      const q = this.searchQuery.toLowerCase();

      return this.detailedReportCurriculum.filter((item) =>
        item.institute_name?.toLowerCase().includes(q),
      );
    },

    /**
     * 🔹 PAGINATION
     */
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
      return Math.min(
        this.currentPage * this.itemsPerPage,
        this.filteredData.length,
      );
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

    /**
     * 🔹 MAP: institute_id → programs → curriculum years
     */
    curriculumYearsByInstitute() {
      const map = {};

      this.courses.forEach((c) => {
        const instituteId = c.curriculum?.program?.institute?.institute_id;
        const programId = c.curriculum?.program_id;

        if (!instituteId || !programId) return;

        const key = `${instituteId}-${programId}`;

        if (!map[key]) {
          map[key] = {
            institute_id: instituteId,
            program_id: programId,
            program_name: c.curriculum?.program?.program_name,
            start_year: c.curriculum?.curriculum_start_year,
            end_year: c.curriculum?.curriculum_end_year,
          };
        }
      });

      return Object.values(map);
    },
  },

  methods: {
    async loadReportCurriculums() {
      const store = useFetchDataStore();
      await store.fetchReportCurriculum();
    },

    toggleAdd() {
      this.isAdd = true;
      this.isTable = true;
    },

    toggleDelete(item) {
      this.recordToDelete = item;
      this.showDeleteModal = true;
    },

    confirmDelete() {
      if (!this.recordToDelete) return;

      axios
        .delete(
          process.env.VUE_APP_API_BASE_URL +
            `/programs/delete-id/${this.recordToDelete.program_id}`,
        )
        .then(() => {
          this.showDeleteModal = false;
          this.recordToDelete = null;
          this.loadReportCurriculums();
          toast.success("Record deleted successfully");
        })
        .catch(() => {
          toast.error("Failed to delete record.");
        });
    },

    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
  },

  async mounted() {
    const store = useFetchDataStore();

    await this.loadReportCurriculums();

    if (!this.courses.length) {
      await store.fetchCourses();
    }

    // ✅ SAME ACTIVE YEAR LISTENER AS TableCourses
    this.stopEventBus = eventBus.on((newYear) => {
      if (!newYear) return;
      this.activeSchoolYear = newYear;
    });
  },

  beforeUnmount() {
    this.stopEventBus?.();
  },
};
</script>
