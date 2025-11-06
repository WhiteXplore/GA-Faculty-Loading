<template>
  <div class="space-y-6 text-[13px]">
    <!-- HEADER -->
    <div class="text-sm flex justify-between">
      <div class="text-[13px] text-text mt-4">Pages / Year & Section</div>

      <div class="flex items-center gap-2">
        <div
          @click="refreshTable"
          class="flex items-center gap-2 px-3 py-2 bg-blue-800 text-white rounded-xl shadow-sm hover:shadow-md border border-blue-800 hover:bg-white hover:text-blue-800 transition-all duration-300 cursor-pointer"
        >
          <div
            class="flex items-center justify-center w-5 h-5 bg-white rounded-full group-hover:bg-white transition-colors duration-300"
          >
            <icon
              :name="'refresh'"
              class="w-5 h-5 text-blue-800 transition-colors duration-300 group-hover:text-blue-600"
            />
          </div>
          <span class="font-medium text-sm">Refresh</span>
        </div>
        <button
          @click="openYearSectionModal"
          class="flex items-center gap-2 px-4 py-2 text-green-600 bg-white border border-green-500 rounded-xl shadow-sm hover:bg-green-600 hover:text-white transition-all duration-300"
        >
          <div
            class="flex items-center justify-center w-5 h-5 bg-green-100 rounded-full"
          >
            <icon name="circle-add" class="w-4 h-4" />
          </div>
          <span class="font-medium">Add Year/Section</span>
        </button>
      </div>
    </div>

    <!-- MAIN CONTENT -->
    <div v-if="user" class="space-y-6">
      <!-- Program Info (Program Chairperson only) -->
      <div
        v-if="user.role === 'Program Chairperson' && userProgram"
        class="bg-white border border-green-100 p-5 rounded-2xl"
      >
        <h2 class="text-lg font-bold text-gray-800">
          {{ userProgram.program_name }}
        </h2>
        <p class="text-sm text-gray-600" v-if="userProgram.institute">
          Institute: {{ userProgram.institute.institute_name }}
        </p>
        <!-- SECTIONS TABLE -->
        <div v-if="filteredAndSearchedClasses.length > 0">
          <!-- Table -->
          <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
            <table
              class="min-w-full text-sm text-gray-700 border-collapse table-auto"
            >
              <thead
                class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
              >
                <tr>
                  <th
                    v-if="user.role === 'Admin'"
                    class="px-4 py-3 text-left w-[20%]"
                  >
                    Program
                  </th>
                  <th class="px-4 py-3 text-left w-[15%]">Program</th>
                  <th class="px-4 py-3 text-left w-[15%]">Section Name</th>
                  <th class="px-4 py-3 text-center w-[18%]">Class Size</th>
                  <th class="px-4 py-3 text-center w-[18%]">School Year</th>
                  <th class="px-4 py-3 text-center w-[20%]">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="cls in paginatedClasses"
                  :key="cls.class_id"
                  class="hover:bg-green-50 transition-all border-t"
                >
                  <td v-if="user.role === 'Admin'" class="px-4 py-3 text-left">
                    {{ cls.program?.program_name }}
                  </td>
                  <td class="px-4 py-3 text-left">
                    {{ cls.program?.program_code }}
                  </td>
                  <td class="px-4 py-3 font-medium text-left">
                    {{ cls.set_name }}
                  </td>
                  <td class="px-4 py-3 text-center">{{ cls.class_size }}</td>
                  <td class="px-4 py-3 text-center">
                    {{ cls.schoolYear?.school_year_name }}
                  </td>
                  <td class="px-4 py-3 flex justify-center gap-2">
                    <!-- Delete Button -->
                    <button
                      @click="promptDelete(cls.class_id)"
                      class="px-3 py-1 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                    >
                      <icon name="delete" /> Delete
                    </button>
                  </td>
                </tr>

                <tr v-if="paginatedClasses.length === 0">
                  <td
                    :colspan="user.role === 'Admin' ? 6 : 5"
                    class="text-center py-6 text-gray-400"
                  >
                    No matching sections found
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="flex justify-between items-center mt-4 text-gray-700">
            <div>
              Showing {{ startIndex }} to {{ endIndex }} of
              {{ filteredAndSearchedClasses.length }} entries
            </div>
            <div class="flex items-center">
              <button
                @click="changePage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400 disabled:opacity-50"
              >
                &lt;
              </button>
              <button
                v-for="page in pageNumbers"
                :key="'page-' + page"
                @click="changePage(page)"
                :class="{
                  'bg-defaultGreen text-white': currentPage === page,
                  'bg-gray-200 text-gray-700': currentPage !== page,
                }"
                class="px-3 py-1 mx-1 rounded-md hover:bg-green-300"
              >
                {{ page }}
              </button>
              <button
                @click="changePage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400 disabled:opacity-50"
              >
                &gt;
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="bg-white border p-8 rounded-xl text-center">
        <p class="text-gray-600">
          No sections created for {{ activeSchoolYearName }} yet.
        </p>
      </div>
    </div>

    <!-- LOADING OR EMPTY STATES -->
    <div v-else-if="loading" class="bg-white border p-8 rounded-xl text-center">
      <p class="text-gray-500 animate-pulse">Loading program information...</p>
    </div>

    <div v-else class="bg-white border p-8 rounded-xl text-center">
      <p class="text-gray-600 font-medium">
        No program found for your account.
      </p>
      <p class="text-sm text-gray-400 mt-1">
        Please contact the administrator.
      </p>
    </div>
  </div>

  <!-- MODAL -->
  <!-- 🔹 Fixed modal rendering -->
  <addYearSection
    v-if="showYearSectionModal"
    :programData="userProgram || {}"
    @close="closeYearSectionModal"
    @refresh="loadUserProgram"
  />

  <div v-if="showDeleteModal" class="fixed inset-0 z-50">
    <div class="absolute inset-0 bg-gray-800 bg-opacity-40"></div>
    <div
      class="rounded-xl border w-[300px] md:w-[400px] bg-white py-6 px-4 flex flex-col items-center absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
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
        Are you sure you want to delete this record? This action cannot be
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
import { toast } from "vue3-toastify";
import addYearSection from "@/components/admin/records/modals/add-year-section.vue";
import axios from "axios";
import { mapState } from "pinia";
import { useFetchDataStore } from "@/store/fetch-data-store";

export default {
  name: "YearSectionManagement",
  components: { icon, addYearSection },
  data() {
    return {
      showYearSectionModal: false,
      userProgram: null,
      user: null,
      classes: [],
      programs: [],
      searchQuery: "",
      currentPage: 1,
      itemsPerPage: 10,
      showDeleteModal: false,
      deleteTargetId: null,
      loading: true,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["activeYear", "year"]),

    activeSchoolYearId() {
      return this.activeYear?.school_year_id || null;
    },

    activeSchoolYearName() {
      return this.activeYear?.school_year_name || "Current School Year";
    },

    filteredClasses() {
      if (!this.activeSchoolYearId) return [];

      if (this.user?.role === "Admin") {
        return this.classes.filter(
          (cls) =>
            String(cls.school_year_id) === String(this.activeSchoolYearId)
        );
      }

      if (this.userProgram) {
        return this.classes.filter(
          (cls) =>
            String(cls.program_id) === String(this.userProgram.program_id) &&
            String(cls.school_year_id) === String(this.activeSchoolYearId)
        );
      }

      return [];
    },

    filteredAndSearchedClasses() {
      return this.filteredClasses.filter((cls) =>
        cls.set_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },

    totalPages() {
      return Math.ceil(
        this.filteredAndSearchedClasses.length / this.itemsPerPage
      );
    },

    startIndex() {
      return this.filteredAndSearchedClasses.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(
        this.startIndex + this.itemsPerPage - 1,
        this.filteredAndSearchedClasses.length
      );
    },

    paginatedClasses() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredAndSearchedClasses.slice(
        start,
        start + this.itemsPerPage
      );
    },

    pageNumbers() {
      return Array.from({ length: this.totalPages }, (_, i) => i + 1);
    },
  },
  methods: {
    async refreshTable() {
      const store = useFetchDataStore();
      this.loading = true;

      try {
        await this.fetchUser();
        await store.fetchActiveYears();
        await this.loadClasses();
        await this.loadPrograms();
        await this.loadUserProgram();
        this.currentPage = 1;
        toast.success("Table refreshed successfully");
      } catch (error) {
        console.error("Error refreshing table:", error);
        toast.error("Failed to refresh table");
      } finally {
        this.loading = false;
      }
    },

    async fetchUser() {
      const { data } = await axios.get("http://localhost:8000/auth/me", {
        withCredentials: true,
      });
      this.user = data;
    },

    async loadPrograms() {
      const { data } = await axios.get(
        "http://localhost:8000/programs/get-programs"
      );
      this.programs = data;
    },

    async loadUserProgram() {
      if (this.user?.role === "Program Chairperson") {
        this.userProgram = this.programs.find(
          (p) => String(p.program_id) === String(this.user.program_id)
        );
      }
    },

    async loadClasses() {
      const { data } = await axios.get(
        "http://localhost:8000/class/get-classes"
      );
      this.classes = data;
    },

    promptDelete(classId) {
      this.deleteTargetId = classId;
      this.showDeleteModal = true;
    },

    async confirmDelete() {
      if (!this.deleteTargetId) return;

      try {
        await axios.delete(
          `http://localhost:8000/class/delete-id/${this.deleteTargetId}`,
          { withCredentials: true }
        );
        await this.loadClasses();
        toast.success("Record deleted successfully");
        this.showDeleteModal = false;
        this.deleteTargetId = null;
      } catch (error) {
        console.error("Error deleting class:", error);
        toast.error("Failed to delete class");
      }
    },

    openYearSectionModal() {
      this.showYearSectionModal = true;
    },

    closeYearSectionModal() {
      this.showYearSectionModal = false;
      this.loadClasses();
    },

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) this.currentPage = page;
    },
  },

  watch: {
    activeYear: {
      async handler() {
        this.currentPage = 1;
        await this.loadClasses();
      },
      immediate: true,
    },
  },

  async mounted() {
    await this.fetchUser();
    const store = useFetchDataStore();
    await store.fetchActiveYears();
    await this.loadClasses();
    await this.loadPrograms();
    await this.loadUserProgram();
    this.loading = false;
  },
};
</script>
