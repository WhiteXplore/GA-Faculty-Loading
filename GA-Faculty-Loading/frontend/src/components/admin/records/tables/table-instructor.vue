<template>
  <div v-if="isTable" class=" ">
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages / Faculty List
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
        <span class="font-medium text-sm">Add Instructor</span>
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
              placeholder="Search..."
              @input="changePage(1)"
            />
          </div>
        </div>

        <!-- Table -->
        <div class="w-full rounded-xl overflow-hidden">
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
                  <th class="px-4 py-3 text-left font-normal">Instructors</th>
                  <th class="px-4 py-3 text-left font-normal">Instutute</th>
                  <th class="px-4 py-3 text-left font-normal">Program</th>
                  <th class="px-4 py-3 text-left font-normal">Job Status</th>
                  <th class="px-4 py-3 text-left rounded-tr-lg font-normal">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(instructor_data, index) in paginatedData"
                  :key="instructor_data.instructor_id"
                  class="hover:bg-green-50 transition-all border-t"
                >
                  <td class="px-4 py-2 text-left">
                    {{ startIndex + index }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    {{ instructor_data.instructor_fname }}
                    {{ instructor_data.instructor_mname }}
                    {{ instructor_data.instructor_lname }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    {{ instructor_data.institute?.institute_name }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    {{ instructor_data.program?.program_name }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    {{ instructor_data.instructor_jobtype }}
                  </td>
                  <td class="px-4 py-2 text-left">
                    <div class="flex gap-2">
                      <button
                        class="w-[90px] h-8 border border-green-300 hover:bg-green-200 text-defaultGreen rounded-lg flex items-center justify-center gap-1 text-sm"
                        @click="toggleEdit(instructor_data)"
                      >
                        <icon name="edit" /> Edit
                      </button>
                      <button
                        class="px-3 py-1 h-8 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                        @click="toggleDelete(instructor_data)"
                      >
                        <icon name="delete" /> Delete
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="paginatedData.length === 0">
                  <td colspan="12" class="text-center py-8 text-gray-400">
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

  <AddInstructor
    v-if="isAddFacultyLoad"
    @close="closeView"
    @refresh="loadInstructors"
  />
  <EditInstructor
    v-if="showEditModal && selectedInstructor"
    :instructorData="selectedInstructor"
    @close="closeModal"
    @refresh="loadInstructors"
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
import AddInstructor from "../modals/add-instructor.vue";
import EditInstructor from "../modals/edit-instructor.vue";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TableInstructorPage",
  components: {
    AddInstructor,
    EditInstructor,
    icon,
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAddFacultyLoad: false,
      isRecordVisible: false,
      isEdit: false,
      isTable: true,
      showDeleteModal: false,
      recordToDelete: null,
      selectedInstructor: null, // 🔁 Renamed for clarity
      showEditModal: false, // ✅ Needed to show/hide modal
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["instructors"]),

    filteredData() {
      const query = this.searchQuery.toLowerCase();
      return this.instructors.filter((item) =>
        `${item.instructor_fname} ${item.instructor_mname} ${item.instructor_lname}`
          .toLowerCase()
          .includes(query),
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
    async loadInstructors() {
      const store = useFetchDataStore();
      await store.fetchInstructors();
    },
    toggleAdd() {
      this.isAddFacultyLoad = true;
      this.isTable = true;
    },
    toggleEdit(item) {
      this.selectedInstructor = item;
      this.showEditModal = true;
    },

    toggleDelete(item) {
      this.recordToDelete = item;
      this.showDeleteModal = true;
    },
    async confirmDelete() {
      if (!this.recordToDelete) return;
      try {
        await axios.delete(
          process.env.VUE_APP_API_BASE_URL +
            `/instructors/delete-id/${this.recordToDelete.instructor_id}`,
        );

        // Play sound after successful delete
        const audio = new Audio(require("@/assets/delete.mp3"));
        audio.play();

        // Refresh store
        const store = useFetchDataStore();
        await store.fetchInstructors();

        this.recordToDelete = null;
        this.showDeleteModal = false;
        toast.success("Instructor deleted successfully");
      } catch (error) {
        toast.error("Failed to delete record");
        console.error("Delete error:", error);
      }
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
    closeView() {
      this.isAddFacultyLoad = false;
      this.isUploadData = false;
    },
    closeModal() {
      this.showEditModal = false;
      this.selectedInstructor = null;
    },
    handleBackToTable() {
      this.isRecordVisible = false;
      this.isEdit = false;
      this.isAddFacultyLoad = false;
      this.isUploadData = false;
      this.isTable = true;
    },
  },
  mounted() {
    this.loadInstructors();
  },
};
</script>
