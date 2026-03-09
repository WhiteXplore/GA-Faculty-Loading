<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages / Faculty List
      </div>
    </div>

    <!-- Table Container -->
    <div class="mt-4 overflow-x-auto border p-3 rounded-xl bg-white">
      <div
        class="flex justify-between items-center flex-wrap gap-3 text-gray-700 bg-white"
      >
        <!-- Items per page -->
        <div class="flex items-center gap-2">
          <div class="relative">
            <select
              v-model="itemsPerPage"
              class="appearance-none rounded-full border border-green-600 bg-white px-3 py-1.5 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
              @change="changePage(1)"
            >
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
            </select>
            <div
              class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-green-600"
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
            placeholder="Search faculty..."
            class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
            @input="changePage(1)"
          />
          <div
            class="absolute inset-y-0 left-3 flex items-center text-green-600 pointer-events-none"
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

      <!-- Faculty Table -->
      <div class="w-full mt-3 rounded-xl overflow-hidden">
        <div
          class="overflow-y-auto transition-all duration-300"
          :class="tableHeightClass"
        >
          <table class="min-w-full table-auto border text-sm text-gray-700">
            <thead
              class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
            >
              <tr>
                <th class="w-10 px-4 py-3 text-left rounded-tl-lg font-normal">
                  ID
                </th>
                <th class="px-4 py-3 text-left font-normal">Faculty Name</th>
                <th class="px-4 py-3 text-left font-normal">Institute</th>
                <th class="px-4 py-3 text-left font-normal">Program</th>
                <th class="px-4 py-3 text-left font-normal">Role</th>
                <th class="px-4 py-3 text-left rounded-tr-lg font-normal">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(user, index) in paginatedData"
                :key="user.id"
                class="bg-white hover:bg-green-50 transition border rounded-md shadow-sm"
              >
                <td class="px-4 py-3">{{ startIndex + index }}</td>
                <td class="px-4 py-3">
                  {{ user.first_name }} {{ user.last_name }}
                </td>
                <td class="px-4 py-3">
                  {{ user.institute?.institute_name || "N/A" }}
                </td>
                <td class="px-4 py-3">
                  {{ user.program?.program_name || "N/A" }}
                </td>
                <td class="px-4 py-3 text-center">{{ user.role }}</td>
                <td class="px-4 py-3">
                  <div class="flex gap-2">
                    <!-- View button -->
                    <button
                      class="px-3 py-1 h-8 border border-blue-300 hover:bg-blue-200 text-blue-800 rounded-lg flex items-center gap-1"
                      @click="toggleView(user)"
                    >
                      <icon name="eye" /> View
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="paginatedData.length === 0">
                <td colspan="6" class="text-center py-8 text-gray-400">
                  No faculty found
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
          {{ filteredData.length }} faculty
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

    <!-- View Modal -->
    <div
      v-if="showViewModal"
      class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
    >
      <div
        class="bg-white w-full max-w-lg rounded-2xl shadow-2xl p-6 relative animate-slideUp"
      >
        <!-- Header -->
        <div class="flex justify-between items-center border-b pb-3 mb-4">
          <h2
            class="text-xl font-semibold text-gray-900 flex items-center gap-2"
          >
            <svg
              class="w-6 h-6 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 11c0 1.657-1.343 3-3 3S6 12.657 6 11s1.343-3 3-3 3 1.343 3 3zm0 0v10m0-10c0 1.657 1.343 3 3 3s3-1.343 3-3-1.343-3-3-3-3 1.343-3 3z"
              />
            </svg>
            Faculty Expertise
          </h2>
          <button
            @click="showViewModal = false"
            class="text-gray-400 hover:text-gray-600 transition"
          >
            ✕
          </button>
        </div>

        <!-- Content -->
        <div class="space-y-4" v-if="selectedFaculty">
          <!-- Faculty Info -->
          <div class="grid gap-2 text-sm">
            <p class="flex space-x-6">
              <span class="font-semibold text-gray-700">Name:</span>
              <span class="text-gray-900">
                {{ selectedFaculty.first_name }} {{ selectedFaculty.last_name }}
              </span>
            </p>
            <p class="flex space-x-2">
              <span class="font-semibold text-gray-700">Institute:</span>
              <span class="text-gray-900">
                {{ selectedFaculty.institute?.institute_name || "N/A" }}
              </span>
            </p>
            <p class="flex space-x-2">
              <span class="font-semibold text-gray-700">Program:</span>
              <span class="text-gray-900">
                {{ selectedFaculty.program?.program_name || "N/A" }}
              </span>
            </p>
          </div>

          <!-- Expertise Section -->
          <div class="pt-3 border-t">
            <h3 class="font-semibold text-gray-800 mb-2">Expertise</h3>
            <ul
              class="list-disc list-inside ml-2 space-y-1 text-gray-700 text-sm"
            >
              <li
                v-for="(other, i) in selectedFaculty.expertise || []"
                :key="i"
              >
                {{ other.course?.course_code }} -
                {{ other.course?.course_description }}
              </li>
              <li
                v-if="
                  !selectedFaculty.expertise ||
                  selectedFaculty.expertise.length === 0
                "
                class="text-gray-500 italic"
              >
                No expertise added
              </li>
            </ul>
          </div>

          <!-- Other Expertise Section -->
          <div class="pt-3 border-t">
            <h3 class="font-semibold text-gray-800 mb-2">Other Expertise</h3>
            <ul
              class="list-disc list-inside ml-2 space-y-1 text-gray-700 text-sm"
            >
              <li
                v-for="(other, i) in selectedFaculty.other_expertise || []"
                :key="i"
              >
                {{ other.course?.course_code }} -
                {{ other.course?.course_description }}
              </li>
              <li
                v-if="
                  !selectedFaculty.other_expertise ||
                  selectedFaculty.other_expertise.length === 0
                "
                class="text-gray-500 italic"
              >
                None other expertise added
              </li>
            </ul>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex justify-end mt-6">
          <button
            @click="showViewModal = false"
            class="px-5 py-2 rounded-lg bg-[#147452] text-white font-medium hover:bg-green-700 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TableFaculty",
  components: { icon },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isTable: true,
      showDeleteModal: false,
      recordToDelete: null,
      selectedFaculty: null,
      showEditModal: false,
      showViewModal: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rawusers"]),
    filteredData() {
      const query = this.searchQuery.toLowerCase();

      // Filter only Program Chairperson and Faculty
      return this.rawusers
        .filter((u) => u.role === "Program Chairperson" || u.role === "Faculty")
        .filter((u) =>
          [
            `${u.first_name} ${u.last_name}`,
            u.institute?.institute_name || "",
            u.program?.program_name || "",
            u.role || "",
          ]
            .join(" ")
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
      return Array.from({ length: this.totalPages }, (_, i) => i + 1);
    },
    tableHeightClass() {
      return this.itemsPerPage > 10 ? "max-h-[500px]" : "max-h-[400px]";
    },
  },
  methods: {
    async loadUsers() {
      const store = useFetchDataStore();
      await store.fetchRawUsers();
    },
    toggleEdit(user) {
      this.selectedFaculty = user;
      this.showEditModal = true;
    },
    toggleDelete(user) {
      this.recordToDelete = user;
      this.showDeleteModal = true;
    },
    toggleView(user) {
      this.selectedFaculty = user;
      this.showViewModal = true;
    },
    async confirmDelete() {
      if (!this.recordToDelete || !Number.isInteger(this.recordToDelete.id)) {
        toast.error("Invalid user ID.");
        return;
      }
      const userId = this.recordToDelete.id;
      try {
        await axios.delete(`http://localhost:8000/users/delete/${userId}`);
        this.recordToDelete = null;
        this.showDeleteModal = false;
        new Audio(require("@/assets/delete.mp3")).play();
        await this.loadUsers();
        toast.success("Faculty deleted successfully");
      } catch (error) {
        console.error("Delete failed:", error);
        toast.error("Failed to delete faculty.");
      }
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
  },
  mounted() {
    this.loadUsers();
  },
};
</script>
