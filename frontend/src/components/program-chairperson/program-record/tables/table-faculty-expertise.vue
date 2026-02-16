<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mt-8">
      <div class="text-[13px] text-gray-700">
        Pages / Faculty Expertise Overview
        <span class="text-gray-400 mx-1">/</span>
        <span class="font-semibold text-defaultGreen">{{ activeTab }}</span>
      </div>
    </div>

    <!-- Main Content -->
    <!-- Tabs -->
    <div class="flex gap-2 mt-6">
      <button
        v-for="tab in tabs"
        :key="tab"
        @click="activeTab = tab"
        :class="[
          'px-4 py-2 rounded-t-lg font-normal text-sm transition-all',
          activeTab === tab
            ? 'bg-defaultGreen text-white shadow-md'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
        ]"
      >
        {{ tab }}
      </button>
    </div>
    <div class="overflow-x-auto border p-3 rounded-tr-xl bg-white">
      <!-- Controls -->
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
            placeholder="Search faculty ..."
            class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full sm:w-[280px] transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
            @input="changePage(1)"
          />
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

      <!-- Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[69vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead
              class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
            >
              <tr>
                <th class="px-4 py-3 text-left w-[3%] rounded-tl-lg">No.</th>
                <th class="px-4 py-3 text-left w-[20%]">
                  {{
                    activeTab !== "Not Selected Expertise"
                      ? "Faculty Name"
                      : "Course Code"
                  }}
                </th>
                <th class="px-4 py-3 text-left w-[40%]">Course Description</th>
                <th class="px-4 py-3 text-left w-[25%]">Program</th>
              </tr>
            </thead>

            <tbody>
              <!-- Expertise / Other Expertise -->
              <template v-if="activeTab !== 'Not Selected Expertise'">
                <tr
                  v-for="(user, index) in paginatedUsers"
                  :key="`${user.id}-${user.course_id}-${user.type}`"
                  class="hover:bg-green-50 transition-all border-t"
                >
                  <td class="px-4 py-4 text-gray-600 text-left">
                    {{ startIndex + index }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.first_name }} {{ user.last_name }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.course_code }} - {{ user.course_title }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.program?.program_name || "-" }}
                  </td>
                </tr>
              </template>

              <!-- Not Selected Expertise -->
              <template v-else>
                <tr
                  v-for="(user, index) in paginatedUsers"
                  :key="`not-selected-${user.course_id}-${index}`"
                  class="hover:bg-green-50 transition-all border-t"
                >
                  <td class="px-4 py-4 text-gray-600 text-left">
                    {{ startIndex + index }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.course_code }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.course_title }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.curriculum?.program?.program_code || "-" }}
                  </td>
                </tr>
              </template>

              <!-- No Records -->
              <tr v-if="paginatedUsers.length === 0">
                <td colspan="4" class="text-center py-8 text-gray-400">
                  No records found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-gray-700 text-sm">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredUsers.length }} entries
        </div>
        <div class="flex items-center gap-1 text-sm">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400"
          >
            &lt;
          </button>
          <button
            v-for="page in pageNumbers"
            :key="page"
            @click="changePage(page)"
            :class="{
              'bg-defaultGreen text-white': currentPage === page,
              'bg-gray-200 text-gray-700': currentPage !== page,
            }"
            class="px-3 py-1 rounded-md hover:bg-green-300"
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
</template>

<script>
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "FacultyExpertiseOverview",

  data() {
    return {
      searchQuery: "",
      itemsPerPage: 10,
      currentPage: 1,
      user: null,
      activeTab: "Expertise",
      tabs: ["Expertise", "Other Expertise", "Not Selected Expertise"],
      allCourses: [],
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["rawusers"]),

    filteredUsers() {
      let users = this.rawusers || [];
      const query = this.searchQuery.toLowerCase();

      // Filter only Faculty & Program Chairperson
      users = users.filter(
        (u) => u.role === "Faculty" || u.role === "Program Chairperson",
      );

      // Limit by logged-in user's institute/program
      if (this.user) {
        if (this.user.role === "Program Chairperson") {
          users = users.filter(
            (u) => u.institute?.institute_id === this.user.institute_id,
          );
        } else {
          users = users.filter(
            (u) =>
              u.institute?.institute_id === this.user.institute_id &&
              u.program?.program_id === this.user.program_id,
          );
        }
      }

      let expanded = [];

      // 🔹 Expertise Tab
      if (this.activeTab === "Expertise") {
        users.forEach((u) => {
          u.expertise.forEach((e) => {
            expanded.push({
              ...u,
              type: "Expertise",
              course_id: e.course.course_id,
              course_code: e.course.course_code,
              course_title: e.course.course_title,
            });
          });
        });
      }

      // 🔹 Other Expertise Tab
      if (this.activeTab === "Other Expertise") {
        users.forEach((u) => {
          u.other_expertise.forEach((e) => {
            expanded.push({
              ...u,
              type: "Other Expertise",
              course_id: e.course.course_id,
              course_code: e.course.course_code,
              course_title: e.course.course_title,
            });
          });
        });
      }

      // 🔹 Not Selected Expertise Tab
      if (this.activeTab === "Not Selected Expertise") {
        const selected = new Set();

        users.forEach((u) => {
          u.expertise.forEach((e) => selected.add(e.course.course_id));
          u.other_expertise.forEach((e) => selected.add(e.course.course_id));
        });

        // Filter only courses belonging to the same institute and program as the logged-in user
        expanded = this.allCourses
          .filter((c) => {
            const programMatch =
              this.user?.program_id &&
              c.curriculum?.program?.program_id === this.user.program_id;

            const instituteMatch =
              this.user?.institute_id &&
              c.curriculum?.program?.institute?.institute_id ===
                this.user.institute_id;

            // Only show courses under the same institute and program, and not yet selected
            return !selected.has(c.course_id) && programMatch && instituteMatch;
          })
          .map((c) => ({
            ...c,
            type: "Not Selected Expertise",
          }));
      }

      // 🔍 Search filter
      if (query) {
        expanded = expanded.filter((u) => {
          if (this.activeTab === "Not Selected Expertise") {
            return (
              u.course_code.toLowerCase().includes(query) ||
              u.course_title.toLowerCase().includes(query)
            );
          } else {
            return (
              u.first_name.toLowerCase().includes(query) ||
              u.last_name.toLowerCase().includes(query) ||
              u.program?.program_name?.toLowerCase().includes(query) ||
              u.course_code.toLowerCase().includes(query)
            );
          }
        });
      }

      return expanded;
    },

    paginatedUsers() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredUsers.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredUsers.length / this.itemsPerPage) || 1;
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
      return this.filteredUsers.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      const end = this.currentPage * this.itemsPerPage;
      return Math.min(end, this.filteredUsers.length);
    },
  },

  methods: {
    async fetchUser() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          },
        );
        this.user = res.data;
      } catch (err) {
        console.error("Failed to fetch user:", err);
      }
    },

    async loadRawUsers() {
      const store = useFetchDataStore();
      await store.fetchRawUsers();
    },

    async fetchAllCourses() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/courses/get-courses",
        );
        this.allCourses = res.data;
      } catch (err) {
        console.error("Error fetching courses:", err);
      }
    },

    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
  },

  async mounted() {
    await this.fetchUser();
    await this.loadRawUsers();
    await this.fetchAllCourses();
  },
};
</script>
