<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages / User Accounts
      </div>

      <div
        @click="toggleAdd"
        class="flex items-center gap-2 px-4 py-2 border text-green-600 border-green-600 rounded-xl hover:bg-green-700 hover:shadow-lg cursor-pointer transition duration-200"
      >
        <div
          class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
        >
          <icon :name="'add-account1.1'" class="w-4 h-4" />
        </div>
        <span class="font-medium text-sm">Add Accounts</span>
      </div>
    </div>

    <!-- Table -->
    <div class="mt-4 overflow-x-auto border p-3 rounded-xl bg-white">
      <!-- Top controls -->
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

        <!-- Search -->
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search..."
            class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-[250px] transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
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

      <!-- Data Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <table class="min-w-full text-sm text-gray-700 border-collapse">
          <thead
            class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
          >
            <tr>
              <th class="w-10 px-4 py-3 text-left rounded-tl-lg font-normal">
                ID
              </th>
              <th class="px-4 py-3 text-left font-normal">Name</th>

              <th class="px-4 py-3 text-left font-normal">Institute</th>
              <th class="px-4 py-3 text-left font-normal">Program</th>
              <th class="px-4 py-3 text-left font-normal">Position</th>
              <th class="px-4 py-3 text-left font-normal">Email</th>
              <th class="px-4 py-3 text-left rounded-tr-lg font-normal">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(user, index) in paginatedData"
              :key="user.id"
              class="hover:bg-green-50 transition-all border-t"
            >
              <td class="px-4 py-3 text-left">{{ startIndex + index }}</td>
              <td class="px-4 py-3 text-left">
                {{ user.first_name }} {{ user.last_name }}
              </td>

              <td class="px-4 py-3 text-left">
                {{ getInstituteName(user.institute_id) }}
              </td>
              <td class="px-4 py-3 text-left">
                {{ getProgramName(user.program_id) }}
              </td>
              <td class="px-4 py-3 text-left">{{ user.role }}</td>
              <td class="px-4 py-3 text-left">{{ user.email }}</td>
              <td class="px-4 py-3 text-left">
                <div class="flex gap-2">
                  <button
                    class="px-3 py-1 h-8 border border-green-300 hover:bg-green-200 text-defaultGreen rounded-lg flex items-center gap-1"
                    @click="toggleEdit(user)"
                  >
                    <icon name="edit" /> Edit
                  </button>

                  <button
                    class="px-3 py-1 h-8 border border-red-300 hover:bg-red-200 text-red-900 rounded-lg flex items-center gap-1"
                    @click="toggleDelete(user)"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="paginatedData.length === 0">
              <td colspan="7" class="text-center py-6 text-gray-400">
                No records found
              </td>
            </tr>
          </tbody>
        </table>
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
                'bg-defaultGreen text-white': currentPage === page,
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

  <!-- Modals -->
  <addUsers v-if="isAdd" @close="closeView" @refresh="loadUsers" />
  <addUsers
    v-if="showEditModal && selectedUser"
    :userData="selectedUser"
    @close="closeModal"
    @refresh="loadUsers"
  />

  <!-- Delete Confirmation Modal -->
  <div
    v-if="showDeleteModal"
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  ></div>
  <div
    v-if="showDeleteModal"
    class="rounded-xl shadow-lg w-[300px] md:w-[400px] bg-white py-6 px-4 flex flex-col items-center fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 animate-slideUp"
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
import addUsers from "../modals/add-users.vue";

import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TableUsers",
  components: {
    icon,
    addUsers,
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAdd: false,
      isTable: true,
      showDeleteModal: false,
      recordToDelete: null,
      selectedUser: null, // ✅ fixed
      showEditModal: false,
      isDeleting: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["users", "programs"]),
    filteredData() {
      const query = this.searchQuery.toLowerCase();
      return this.users.filter((user) =>
        `${user.first_name} ${user.last_name} ${user.role} ${user.email}`
          .toLowerCase()
          .includes(query)
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
    async loadUsers() {
      const store = useFetchDataStore();
      await store.fetchUsers();
      await store.fetchPrograms();
    },
    getInstituteName(instituteId) {
      const program = this.programs.find((p) => p.institute_id === instituteId);
      return program ? program.institute.institute_name : "N/A";
    },
    getProgramName(programId) {
      const program = this.programs.find((p) => p.program_id === programId);
      return program ? program.program_name : "N/A";
    },
    toggleAdd() {
      this.isAdd = true;
      this.isTable = true;
    },
    toggleEdit(user) {
      this.selectedUser = user; // ✅ fixed
      this.showEditModal = true;
    },
    toggleDelete(user) {
      this.recordToDelete = user;
      this.showDeleteModal = true;
    },
    async confirmDelete() {
      if (!this.recordToDelete || isNaN(this.recordToDelete.id)) {
        toast.error("Invalid user ID.");
        return;
      }

      const userId = this.recordToDelete.id;
      this.isDeleting = true;

      try {
        await axios.delete(
          process.env.VUE_APP_API_BASE_URL + `/auth/remove/${userId}`
        );
        this.recordToDelete = null;
        this.showDeleteModal = false;

        const audio = new Audio(require("@/assets/delete.mp3"));
        audio.play();

        const store = useFetchDataStore();
        await store.fetchUsers();

        toast.success("Record deleted successfully");
      } catch (error) {
        console.error("Delete failed:", error);
        toast.error("Failed to delete record.");
      } finally {
        this.isDeleting = false;
      }
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
    closeView() {
      this.isAdd = false;
    },
    closeModal() {
      this.showEditModal = false;
      this.selectedUser = null;
    },
  },
  mounted() {
    this.loadUsers();
  },
};
</script>
