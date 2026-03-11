<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages / User Accounts
      </div>

      <div class="flex gap-2">
        <div
          @click="toggleImportExpertise"
          class="flex items-center gap-2 px-3 py-2 border text-purple-600 border-purple-600 rounded-xl hover:bg-purple-700 hover:text-white hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-purple-500 bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          </div>
          <span class="font-medium text-sm">Import Expertise</span>
        </div>

        <div
          @click="toggleImport"
          class="flex items-center gap-2 px-3 py-2 border bg-blue-700 text-white border-blue-700 rounded-xl hover:bg-white hover:text-blue-700 hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-blue-500 bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon :name="'uploads'" class="w-4 h-4" />
          </div>
          <span class="font-medium text-sm">Import Users</span>
        </div>

        <div
          @click="toggleAdd"
          class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon :name="'add-account1.1'" class="w-4 h-4" />
          </div>
          <span class="font-medium text-sm">Add Accounts</span>
        </div>
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
              <th class="px-4 py-3 text-left font-normal w-[15%]">Name</th>
              <th class="px-4 py-3 text-left font-normal w-[25%]">Email</th>
              <th class="px-4 py-3 text-left font-normal">Institute</th>
              <th class="px-4 py-3 text-left font-normal">Program</th>
              <th class="px-4 py-3 text-left font-normal">Position</th>

              <th
                class="px-4 py-3 text-center rounded-tr-lg font-normal w-[20%]"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="user in paginatedData"
              :key="user.id"
              class="hover:bg-green-50 transition-all border-t"
            >
              <td class="px-4 py-3 text-left">
                {{ user.first_name }} {{ user.last_name }}
              </td>
              <td class="px-4 py-3 text-left">{{ user.email }}</td>
              <td class="px-4 py-3 text-left">
                {{ user.institute?.institute_code }}
              </td>
              <td class="px-4 py-3 text-left">
                {{ user.program?.program_code }}
              </td>
              <td class="px-4 py-3 text-left">{{ user.role }}</td>

              <td class="px-4 py-3">
                <div class="flex gap-2 flex-wrap justify-center items-center">
                  <button
                    class="w-[90px] h-8 border border-purple-300 hover:bg-purple-200 text-purple-700 rounded-lg flex items-center justify-center gap-1"
                    @click="toggleViewExpertise(user)"
                    title="View Expertise"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-4 w-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                      />
                    </svg>
                    View
                  </button>

                  <button
                    class="w-[90px] h-8 border border-green-300 hover:bg-green-200 text-defaultGreen rounded-lg flex items-center justify-center gap-1"
                    @click="toggleEdit(user)"
                  >
                    <icon name="edit" /> Edit
                  </button>

                  <button
                    class="px-3 py-1 h-8 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                    @click="toggleDelete(user)"
                  >
                    <icon name="delete" /> Delete
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
                'bg-defaultGreen text-white': currentPage === page,
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

  <!-- Modals -->
  <addUsers v-if="isAdd" @close="closeView" @refresh="loadUsers" />
  <addUsers
    v-if="showEditModal && selectedUser"
    :userData="selectedUser"
    @close="closeModal"
    @refresh="loadUsers"
  />
  <importUsers
    v-if="showImportModal"
    @close="closeImportModal"
    @refresh="loadUsers"
  />
  <importExpertise
    v-if="showImportExpertiseModal"
    @close="closeImportExpertiseModal"
    @refresh="loadUsers"
  />
  <viewUserExpertise
    v-if="showViewExpertiseModal && selectedUserExpertise"
    :userData="selectedUserExpertise"
    @close="closeViewExpertiseModal"
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
import importUsers from "../modals/import-users.vue";
import importExpertise from "../modals/import-expertise.vue";
import viewUserExpertise from "../modals/view-user-expertise.vue";

import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TableUsers",
  components: {
    icon,
    addUsers,
    importUsers,
    importExpertise,
    viewUserExpertise,
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAdd: false,
      isTable: true,
      showDeleteModal: false,
      showImportModal: false,
      showImportExpertiseModal: false,
      showViewExpertiseModal: false,
      recordToDelete: null,
      selectedUser: null, // ✅ fixed
      selectedUserExpertise: null,
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
    async loadUsers() {
      const store = useFetchDataStore();
      await store.fetchUsers();
      await store.fetchPrograms();
    },
    toggleAdd() {
      this.isAdd = true;
      this.isTable = true;
    },
    toggleImport() {
      this.showImportModal = true;
    },
    toggleImportExpertise() {
      this.showImportExpertiseModal = true;
    },
    toggleViewExpertise(user) {
      this.selectedUserExpertise = user;
      this.showViewExpertiseModal = true;
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
          process.env.VUE_APP_API_BASE_URL + `/auth/remove/${userId}`,
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
    closeImportModal() {
      this.showImportModal = false;
    },
    closeImportExpertiseModal() {
      this.showImportExpertiseModal = false;
    },
    closeViewExpertiseModal() {
      this.showViewExpertiseModal = false;
      this.selectedUserExpertise = null;
    },
  },
  mounted() {
    this.loadUsers();
  },
};
</script>
