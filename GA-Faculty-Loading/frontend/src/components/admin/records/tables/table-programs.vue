<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4">Pages / Programs</div>

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
        <span class="font-medium text-sm">Add Program</span>
      </div>
    </div>

    <!-- Controls -->
    <div class="mt-4 overflow-x-auto border p-3 rounded-xl bg-white">
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

        <!-- Filters -->
        <div class="flex items-center gap-3 flex-wrap">
          <!-- Institute Filter -->
          <div class="relative">
            <select
              v-model="selectedInstitute"
              class="appearance-none rounded-full border border-green-600 bg-white px-4 py-2 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
              @change="changePage(1)"
            >
              <option value="">All Institutes</option>
              <option
                v-for="(inst, idx) in uniqueInstitutes"
                :key="idx"
                :value="inst"
              >
                {{ inst }}
              </option>
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
      </div>

      <!-- Table -->
      <div class="w-full mt-1 rounded-xl overflow-hidden">
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
                <th class="px-4 py-3 text-left rounded-tl-lg">#</th>
                <th class="px-4 py-2 text-left">Institute</th>
                <th class="px-4 py-2 text-left">Program Code</th>
                <th class="px-4 py-2 text-left">Program Name</th>
                <th class="px-4 py-2 text-left rounded-tr-lg">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(prog, index) in paginatedData"
                :key="prog.program_id"
                class="bg-white hover:bg-green-50 transition border rounded-md shadow-sm"
              >
                <td class="px-4 py-2">{{ startIndex + index }}</td>
                <td class="px-4 py-2">
                  {{ prog.institute?.institute_name || "N/A" }}
                </td>
                <td class="px-4 py-2">{{ prog.program_code }}</td>
                <td class="px-4 py-2">{{ prog.program_name }}</td>
                <td class="px-4 py-2">
                  <div class="flex gap-2">
                    <button
                      class="px-3 py-1 border border-blue-300 hover:bg-blue-200 text-blue-800 rounded-lg flex items-center gap-1"
                      @click="toggleAddYearSection(prog)"
                      title="Add Year/Section"
                    >
                      <icon name="add-students" /> Add Year/Section
                    </button>
                    <button
                      class="px-3 py-1 border border-green-300 hover:bg-green-200 text-green-800 rounded-lg flex items-center gap-1"
                      @click="toggleEdit(prog)"
                    >
                      <icon name="edit" /> Edit
                    </button>
                    <button
                      class="px-3 py-1 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                      @click="toggleDelete(prog)"
                    >
                      <icon name="delete" /> Delete
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="paginatedData.length === 0">
                <td colspan="5" class="text-center py-8 text-gray-400">
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
          <button
            v-for="page in pageNumbers"
            :key="'page-' + page"
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

  <!-- Add / Edit Modals -->
  <addProgram v-if="isAddProgram" @close="closeView" @refresh="loadPrograms" />
  <addProgram
    v-if="showEditModal && selectedProgram"
    :programData="selectedProgram"
    @close="closeModal"
    @refresh="loadPrograms"
  />
  <addYearSection
    v-if="showYearSectionModal && selectedProgram"
    :programData="selectedProgram"
    @close="closeYearSectionModal"
    @refresh="loadPrograms"
  />

  <!-- Delete Confirmation -->
  <div
    v-if="showDeleteModal"
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  ></div>
  <div
    v-if="showDeleteModal"
    class="rounded-xl shadow-lg w-[300px] md:w-[400px] bg-white py-6 px-4 flex flex-col items-center fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50"
  >
    <div
      class="rounded-full w-16 h-16 flex justify-center items-center bg-red-300 animate-pulse"
    >
      <icon name="question" class="w-8 h-8 text-white" />
    </div>
    <h1 class="text-[16px] font-semibold mt-4">Delete Confirmation</h1>
    <p class="mt-2 text-[13px] text-center px-8">
      Are you sure you want to delete this record? This action cannot be undone.
    </p>
    <div class="w-full h-[1px] bg-gray-200 mt-4"></div>
    <div class="flex gap-2 mt-4">
      <button
        class="bg-red-400 px-3 py-2 text-white rounded-md hover:bg-white hover:border hover:border-red-800 hover:text-red-800"
        @click="showDeleteModal = false"
      >
        No, Cancel
      </button>
      <button
        class="bg-green-400 px-3 py-2 text-white rounded-md hover:bg-white hover:border hover:border-green-800 hover:text-green-800"
        @click="confirmDelete"
      >
        Yes, Delete
      </button>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import addProgram from "../modals/add-program.vue";
import addYearSection from "../../../program-chairperson/program-record/modals/add-year-section.vue";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TablePrograms",
  components: { icon, addProgram, addYearSection },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      selectedInstitute: "",
      isAddProgram: false,
      isTable: true,
      showDeleteModal: false,
      recordToDelete: null,
      selectedProgram: null,
      showEditModal: false,
      showYearSectionModal: false,
      user: null,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["programs"]),

    uniqueInstitutes() {
      const names = this.programs.map((p) => p.institute?.institute_name);
      return [...new Set(names.filter(Boolean))];
    },

    filteredData() {
      let result = this.programs || [];

      const currentUser = this.user;

      if (currentUser?.role === "Program Chairperson") {
        result = result.filter(
          (p) =>
            String(p.institute?.institute_id) ===
              String(currentUser.institute_id) &&
            String(p.program_id) === String(currentUser.program_id),
        );
      }

      if (this.selectedInstitute) {
        result = result.filter(
          (p) => p.institute?.institute_name === this.selectedInstitute,
        );
      }

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(
          (p) =>
            p.program_name?.toLowerCase().includes(query) ||
            p.program_code?.toLowerCase().includes(query) ||
            p.institute?.institute_name?.toLowerCase().includes(query),
        );
      }

      return result;
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
      return this.filteredData.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    endIndex() {
      const end = this.currentPage * this.itemsPerPage;
      return Math.min(end, this.filteredData.length);
    },
  },
  methods: {
    async loadPrograms() {
      const store = useFetchDataStore();
      await store.fetchPrograms();
    },
    async fetchUser() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          },
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

    toggleAdd() {
      this.isAddProgram = true;
      this.isTable = true;
    },
    toggleEdit(item) {
      this.selectedProgram = item;
      this.showEditModal = true;
    },
    toggleAddYearSection(item) {
      this.selectedProgram = item;
      this.showYearSectionModal = true;
    },
    toggleDelete(item) {
      this.recordToDelete = item;
      this.showDeleteModal = true;
    },
    confirmDelete() {
      if (!this.recordToDelete || isNaN(this.recordToDelete.program_id)) {
        toast.error("Invalid program ID.");
        return;
      }
      axios
        .delete(
          process.env.VUE_APP_API_BASE_URL +
            `/programs/delete-id/${this.recordToDelete.program_id}`,
        )
        .then(() => {
          this.showDeleteModal = false;
          this.recordToDelete = null;
          this.loadPrograms();
          toast.success("Record deleted successfully");
        })
        .catch((err) => {
          console.error("Delete failed:", err);
          toast.error("Failed to delete record.");
        });
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
    closeView() {
      this.isAddProgram = false;
    },
    closeModal() {
      this.showEditModal = false;
      this.selectedProgram = null;
    },
    closeYearSectionModal() {
      this.showYearSectionModal = false;
      this.selectedProgram = null;
    },
  },
  async mounted() {
    await this.fetchUser();
    await this.loadPrograms();
  },
};
</script>
