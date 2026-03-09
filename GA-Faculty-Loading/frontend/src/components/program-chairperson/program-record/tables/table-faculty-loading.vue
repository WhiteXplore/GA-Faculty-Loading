<template>
  <div v-if="isTable">
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages / Final Schedules
      </div>
    </div>

    <div class="text-[14px] bg-white rounded-xl">
      <div class="mt-4 overflow-x-auto border p-2 rounded-xl">
        <!-- Top controls -->
        <div class="text-gray-700 flex justify-between items-start mt-1">
          <!-- Items Per Page -->
          <div class="flex items-center">
            <select
              v-model="itemsPerPage"
              class="px-1 py-1 border rounded-md"
              @change="changePage(1)"
            >
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
            </select>
            <span class="ml-2">Per page</span>
          </div>

          <!-- Search -->
          <div class="flex items-center">
            <input
              v-model="searchQuery"
              type="text"
              class="px-3 w-[300px] py-2 border rounded-md"
              placeholder="Search by faculty, course, or room..."
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
                  <th
                    class="px-4 py-3 w-10 text-left rounded-tl-lg font-normal"
                  >
                    ID
                  </th>
                  <th class="px-4 py-3 text-left font-normal">Faculty</th>
                  <th class="px-4 py-3 text-left font-normal">Course</th>
                  <th class="px-4 py-3 text-left font-normal">Room</th>
                  <th class="px-4 py-3 text-left font-normal">Day</th>
                  <th class="px-4 py-3 text-left font-normal">Time</th>
                  <th class="px-4 py-3 text-left rounded-tr-lg font-normal">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(schedule, index) in paginatedData"
                  :key="schedule.id"
                  class="hover:bg-green-50 transition-all border-t"
                >
                  <td class="px-4 py-2 text-left">
                    {{ startIndex + index }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    {{ schedule.faculty_name }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    {{ schedule.course_code }}
                  </td>
                  <td class="px-4 py-2 text-left">{{ schedule.room_name }}</td>
                  <td class="px-4 py-2 text-left">{{ schedule.day }}</td>
                  <td class="px-4 py-2 text-left">{{ schedule.time_slot }}</td>
                  <td class="px-4 py-2 text-left">
                    <div class="flex gap-2">
                      <button
                        class="w-[90px] h-8 border border-green-300 hover:bg-green-200 text-defaultGreen rounded-lg flex items-center justify-center gap-1 text-sm"
                        @click="toggleEdit(schedule)"
                      >
                        <icon name="edit" /> Edit
                      </button>
                      <button
                        class="px-3 py-1 h-8 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                        @click="toggleDelete(schedule)"
                      >
                        <icon name="delete" /> Delete
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="paginatedData.length === 0">
                  <td colspan="12" class="text-center py-8 text-gray-400">
                    No schedules found
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
  </div>

  <!-- Delete Confirmation Modal -->
  <div
    v-if="showDeleteModal"
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div
      class="rounded-xl shadow-lg w-[300px] md:w-[400px] bg-white py-6 px-4 flex flex-col items-center"
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
        Are you sure you want to delete this schedule? This action cannot be
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
import axios from "axios";
import { toast } from "vue3-toastify";

export default {
  name: "TableFinalSchedules",
  components: { icon },
  data() {
    return {
      finalSchedules: [],
      loading: false,
      error: null,
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isTable: true,
      showDeleteModal: false,
      recordToDelete: null,
      selectedSchedule: null,
    };
  },
  computed: {
    filteredData() {
      const query = this.searchQuery.toLowerCase();
      return this.finalSchedules.filter(
        (item) =>
          item.faculty_name.toLowerCase().includes(query) ||
          item.course_code.toLowerCase().includes(query) ||
          item.room_name.toLowerCase().includes(query),
      );
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
  },
  methods: {
    async fetchFinalSchedules() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/final-generated-class-schedule/get-all-final-schedules",
        );
        this.finalSchedules = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch final schedules";
        toast.error(this.error);
      } finally {
        this.loading = false;
      }
    },
    toggleEdit(schedule) {
      this.selectedSchedule = schedule;
      // open your edit modal here
    },
    toggleDelete(schedule) {
      this.recordToDelete = schedule;
      this.showDeleteModal = true;
    },
    async confirmDelete() {
      if (!this.recordToDelete) return;
      try {
        await axios.delete(
          process.env.VUE_APP_API_BASE_URL +
            `/final-generated-class-schedule/delete/${this.recordToDelete.id}`,
        );
        toast.success("Schedule deleted successfully");
        this.fetchFinalSchedules();
        this.showDeleteModal = false;
        this.recordToDelete = null;
      } catch (error) {
        toast.error("Failed to delete schedule");
        console.error(error);
      }
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
  },
  mounted() {
    this.fetchFinalSchedules();
  },
};
</script>
