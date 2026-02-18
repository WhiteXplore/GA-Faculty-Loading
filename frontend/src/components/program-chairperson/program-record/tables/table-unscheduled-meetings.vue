<template>
  <div>
    <!-- Controls -->
    <div class="overflow-x-auto border p-3 bg-white">
      <div class="flex justify-between items-center flex-wrap gap-3">
        <!-- Per Page -->
        <div class="flex items-center gap-2">
          <select
            v-model.number="itemsPerPage"
            @change="changePage(1)"
            class="rounded-full border border-green-600 px-3 py-1 text-sm"
          >
            <option :value="10">10</option>
            <option :value="15">15</option>
            <option :value="20">20</option>
          </select>
          <span class="text-sm">Per page</span>
        </div>

        <!-- Search -->
        <input
          v-model="searchQuery"
          @input="changePage(1)"
          type="text"
          placeholder="Search course, program, SY..."
          class="rounded-full border border-green-600 px-4 py-2 text-sm w-[280px]"
        />
      </div>

      <!-- Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <table class="min-w-full text-sm text-gray-700">
          <thead class="bg-defaultGreen text-white">
            <tr>
              <th class="px-4 py-3 text-left">Course</th>
              <th class="px-4 py-3 text-center">Program</th>
              <th class="px-4 py-3 text-center">Type</th>
              <th class="px-4 py-3 text-center">School Year</th>
              <th class="px-4 py-3 text-center">Semester</th>
              <th class="px-4 py-3 text-center">Reason</th>
              <th class="px-4 py-3 text-center">Created</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="item in paginatedData"
              :key="item.id"
              class="border-t hover:bg-green-50"
            >
              <td class="px-4 py-3 font-semibold">
                {{ item.course_code }}
              </td>

              <td class="px-4 py-3 text-center">
                {{ item.program_name }}
              </td>

              <td class="px-4 py-3 text-center">
                {{ item.type }}
              </td>

              <td class="px-4 py-3 text-center">
                {{ item.school_year }}
              </td>

              <td class="px-4 py-3 text-center">
                {{ semesterLabel(item.semester) }}
              </td>

              <td class="px-4 py-3 text-xs text-red-600 max-w-xs">
                {{ item.reason }}
              </td>

              <td class="px-4 py-3 text-center text-xs text-gray-500">
                {{ formatDate(item.created_at) }}
              </td>
            </tr>

            <tr v-if="paginatedData.length === 0">
              <td colspan="7" class="text-center py-8 text-gray-400">
                No unscheduled meetings found
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
          <!-- Prev -->
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400"
          >
            &lt;
          </button>

          <!-- Page Numbers -->
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

          <!-- Next -->
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
import axios from "axios";

export default {
  name: "UnscheduledMeetingTable",

  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      user: {},
    };
  },

  computed: {
    store() {
      return useFetchDataStore();
    },

    filteredData() {
      const query = this.searchQuery.toLowerCase();

      return this.store.unscheduled_meetings
        .filter((item) => item.program_id === this.user.program_id)
        .filter((item) => {
          return (
            item.course_code?.toLowerCase().includes(query) ||
            item.program_name?.toLowerCase().includes(query) ||
            item.school_year?.toLowerCase().includes(query)
          );
        });
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredData.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;
    },

    pageNumbers() {
      const total = this.totalPages;

      if (total <= 3) {
        return Array.from({ length: total }, (_, i) => i + 1);
      }

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
  },

  methods: {
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },

    semesterLabel(sem) {
      return sem === "1" ? "1st Semester" : sem === "2" ? "2nd Semester" : sem;
    },

    formatDate(date) {
      return new Date(date).toLocaleString();
    },

    async fetchUser() {
      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/auth/me`,
          { withCredentials: true },
        );
        this.user = res.data || {};
      } catch {
        this.user = {};
      }
    },
  },

  async mounted() {
    await this.fetchUser();
    await this.store.fetchUnscheduledMeetings();
  },
};
</script>
