<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages /
        <span class="font-semibold text-green-900">
          {{
            user && user.role === "Program Chairperson"
              ? "Faculty Under My Program"
              : "Faculty List"
          }}
        </span>
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
              class="appearance-none rounded-full border border-green-600 bg-white px-3 py-1 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
              @change="changePage(1)"
            >
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
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[65vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead
              class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
            >
              <tr>
                <th class="px-4 py-3 text-left font-normal">Faculty Name</th>
                <th class="px-4 py-3 text-left font-normal">Institute</th>
                <th class="px-4 py-3 text-left font-normal w-[30%]">Program</th>
                <th class="px-4 py-3 text-left font-normal w-[15%]">Role</th>
                <th class="px-4 py-3 text-center rounded-tr-lg font-normal">
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
                <td class="px-4 py-3">
                  {{ user.first_name }} {{ user.last_name }}
                </td>
                <td class="px-4 py-3">
                  {{ user.institute?.institute_name || "N/A" }}
                </td>
                <td class="px-4 py-3">
                  {{ user.program?.program_name || "N/A" }}
                </td>
                <td class="px-4 py-3 text-left">{{ user.role }}</td>
                <td class="px-4 py-3 items-center justify-center flex">
                  <div class="flex gap-2">
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
        <h2 class="text-xl font-semibold text-gray-900 flex items-center gap-2">
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
        <div class="grid gap-2 text-xs">
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

        <div class="pt-3 border-t">
          <h3 class="font-semibold text-gray-800 mb-2">Expertise</h3>
          <ul
            class="list-disc list-inside ml-2 space-y-1 text-gray-700 text-sm"
          >
            <li v-for="(other, i) in selectedFaculty.expertise || []" :key="i">
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

      <div class="flex justify-end mt-6">
        <button
          @click="showViewModal = false"
          class="px-5 py-3 rounded-lg bg-[#147452] text-white font-medium hover:bg-green-700 transition"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
// import { toast } from "vue3-toastify";
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
      user: null, // ✅ added for current logged-in user
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rawusers"]),

    filteredData() {
      const query = this.searchQuery.toLowerCase();
      const currentUser = this.user;

      if (!this.rawusers || !currentUser) return [];

      let list = [];

      // Admin → All faculty and PC
      if (currentUser.role === "Admin") {
        list = this.rawusers.filter(
          (u) => u.role === "Program Chairperson" || u.role === "Faculty"
        );
      }
      // Program Chairperson → Faculty only in same institute + program
      else if (currentUser.role === "Program Chairperson") {
        list = this.rawusers.filter(
          (u) =>
            u.role === "Faculty" &&
            u.institute?.institute_id === currentUser.institute_id &&
            u.program?.program_id === currentUser.program_id
        );
      }

      // Search filter
      return list.filter((u) =>
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
      await store.fetchRawUsers();
    },
    toggleView(user) {
      this.selectedFaculty = user;
      this.showViewModal = true;
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
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
  },

  async mounted() {
    await this.fetchUser();
    await this.loadUsers();
  },
};
</script>
