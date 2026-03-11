<template>
  <div v-if="isTable" class=" ">
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages / Exam Schedules
      </div>
      <div class="flex gap-3">
        <div class="flex gap-3">
          <select
            class="w-[8vw] border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
          >
            <option disabled selected>Select Semester</option>
            <option value="1st">1st Semester</option>
            <option value="2nd">2nd Semester</option>
            <option value="3rd">3rd Semester</option>
            <option value="4th">4th Semester</option>
          </select>
          <select
            class="w-[8vw] border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
          >
            <option disabled selected>Select School Year</option>
            <option value="2023-2024">2023-2024</option>
            <option value="2024-2025">2024-2025</option>
            <option value="2025-2026">2025-2026</option>
          </select>
        </div>
        <div
          @click="toggleGenerate"
          class="cursor-pointer flex gap-2 items-center tracking-wider bg-defaultGreen text-white hover:text-green-700 p-3 py-2 rounded-md hover:bg-green-300 hover:shadow-lg"
        >
          <icon :name="''"></icon>
          <button>Generate Schedules</button>
        </div>
      </div>
    </div>

    <div class="text-[14px] bg-white rounded-xl">
      <div class="mt-4 overflow-x-auto border p-2 rounded-xl">
        <!-- Controls -->
        <div class="text-gray-700 flex justify-between items-start mt-1">
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
          <div class="flex items-center">
            <input
              v-model="searchQuery"
              type="text"
              class="px-3 w-[300px] py-3 border rounded-md"
              placeholder="Search..."
              @input="changePage(1)"
            />
          </div>
        </div>

        <!-- Loading Animation -->
        <div v-if="isLoading" class="flex justify-center items-center py-10">
          <svg
            class="animate-spin h-8 w-8 text-green-700"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            />
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
          </svg>
          <span class="ml-3 text-gray-700 text-sm"
            >Generating schedules...</span
          >
        </div>

        <!-- Table -->
        <div v-if="!isLoading" class="w-full mt-3 rounded-t-lg overflow-x-auto">
          <div
            class="overflow-y-auto transition-all duration-300"
            :class="tableHeightClass"
          >
            <table
              class="min-w-full table-fixed border-collapse text-text text-[13px]"
            >
              <thead class="bg-[#147452] text-white rounded-t-lg">
                <tr>
                  <th class="px-2 py-3 text-left border-b">#</th>
                  <th class="px-2 py-3 text-left border-b">Instructor</th>
                  <th class="px-2 py-3 text-left border-b">Institutes</th>
                  <th class="px-2 py-3 text-left border-b">Course Code</th>
                  <th class="px-2 py-3 text-left border-b">Program</th>
                  <th class="px-2 py-3 text-left border-b">Year</th>
                  <th class="px-2 py-3 text-left border-b">Set</th>
                  <th class="px-2 py-3 text-left border-b">Class Size</th>
                  <th class="px-2 py-3 text-left border-b">Room Name</th>
                  <th class="px-2 py-3 text-left border-b">Room Size</th>
                  <th class="px-2 py-3 text-left border-b">Proctor</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(exam, index) in paginatedData"
                  :key="exam.exam_schedule_id"
                  :class="{ 'bg-green-50 border-b ': (index + 1) % 2 === 0 }"
                >
                  <td class="px-2 py-1 border-b text-left">
                    {{ startIndex + index }}
                  </td>
                  <td class="px-2 py-1 border-b text-left">
                    {{ exam.instructor }}
                  </td>
                  <td class="px-2 py-1 border-b text-left">
                    {{ exam.institute }}
                  </td>
                  <td class="px-2 py-1 border-b text-left">
                    {{ exam.course_code }}
                  </td>
                  <td class="px-2 py-1 border-b text-left">
                    {{ exam.program }}
                  </td>
                  <td class="px-2 py-1 border-b text-left">{{ exam.year }}</td>
                  <td class="px-2 py-1 border-b text-left">{{ exam.set }}</td>
                  <td class="px-2 py-1 border-b text-left">
                    {{ exam.class_size }}
                  </td>
                  <td class="px-2 py-1 border-b text-left">
                    {{ exam.room_name }}
                  </td>
                  <td class="px-2 py-1 border-b text-left">
                    {{ exam.room_size }}
                  </td>
                  <td class="px-2 py-1 border-b text-left">
                    {{ exam.proctor }}
                  </td>
                </tr>
                <tr v-if="!isLoading && paginatedData.length === 0">
                  <td
                    colspan="11"
                    class="text-center py-4 text-gray-500 italic"
                  >
                    No generated data
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="!isLoading" class="flex justify-between items-center mt-4">
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
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";

export default {
  name: "TableExamSchedules",
  components: {
    icon,
  },
  data() {
    return {
      exam_schedule_data: [],
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAdd: false,
      isEdit: false,
      isTable: true,
      isUploadData: false,
      showDeleteModal: false,
      recordToDelete: null,
      isLoading: false,
    };
  },
  computed: {
    filteredData() {
      const query = this.searchQuery.toLowerCase();
      return this.exam_schedule_data.filter((item) =>
        `${item.instructor || ""}`.toLowerCase().includes(query),
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
    toggleGenerate() {
      this.isLoading = true;
      this.isAdd = true;
      this.isTable = true;

      // Simulate data generation
      setTimeout(() => {
        this.exam_schedule_data = [
          {
            exam_schedule_id: 1,
            instructor: "John Doe",
            institute: "Engineering",
            course_code: "ENG101",
            program: "BSECE",
            year: "1",
            set: "A",
            class_size: "30",
            room_name: "Room 101",
            room_size: "40",
            proctor: "Prof. Smith",
          },
        ];
        this.isLoading = false;
        toast.success("Exam schedules generated successfully!");
      }, 2000);
    },
    toggleDelete(item) {
      this.recordToDelete = item;
      this.showDeleteModal = true;
    },
    confirmDelete() {
      if (!this.recordToDelete) return;
      this.exam_schedule_data = this.exam_schedule_data.filter(
        (item) =>
          item.exam_schedule_id !== this.recordToDelete.exam_schedule_id,
      );
      this.recordToDelete = null;
      this.showDeleteModal = false;
      toast.success("Record deleted successfully");
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
    closeView() {
      this.isAdd = false;
      this.isUploadData = false;
    },
    handleBackToTable() {
      this.isEdit = false;
      this.isAdd = false;
      this.isUploadData = false;
      this.isTable = true;
    },
  },
};
</script>
