<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between items-center">
      <!-- Breadcrumbs -->
      <div class="flex items-center gap-1 text-[13px] text-gray-600 mt-4">
        <span
          v-if="viewLevel !== 'institute' && user?.role === 'Admin'"
          class="cursor-pointer hover:text-green-600"
          @click="backToInstitutes"
        >
          Institute
        </span>
        <span v-if="viewLevel !== 'institute' && user?.role === 'Admin'"
          >/</span
        >

        <span
          v-if="viewLevel === 'program' || viewLevel === 'assignClass'"
          class="cursor-pointer hover:text-green-600"
          @click="backToPrograms"
        >
          Programs under {{ selectedInstitute?.institute_name }}
        </span>
        <span v-if="viewLevel === 'assignClass'">/</span>

        <span
          v-if="viewLevel === 'assignClass'"
          class="text-green-700 font-medium underline"
        >
          Assign Classes for {{ selectedProgram?.program_name }}
        </span>
      </div>

      <!-- Add button -->
      <div
        v-if="user?.role === 'Admin' || user?.role === 'Program Chairperson'"
        @click="toggleAdd"
        class="flex items-center gap-2 px-3 py-2 bg-white text-green-600 rounded-xl shadow-sm hover:shadow-md border border-green-500 hover:bg-defaultGreen hover:text-white transition-all duration-300 cursor-pointer"
      >
        <div
          class="flex items-center justify-center w-5 h-5 bg-green-100 rounded-full transition-colors duration-300"
        >
          <icon :name="'circle-add'" class="w-4 h-4 text-green-600" />
        </div>
        <span class="font-medium text-sm">Assign Class</span>
      </div>
    </div>

    <!-- Table Container -->
    <div class="mt-4 overflow-x-auto border p-3 rounded-xl bg-white">
      <!-- Top Controls -->
      <div
        class="flex justify-between items-center flex-wrap gap-3 sm:gap-4 text-gray-700 bg-white"
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
              class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-green-600 transition-colors"
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
            placeholder="Search..."
            class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
            @input="changePage(1)"
          />
          <div
            class="absolute inset-y-0 left-3 flex items-center text-green-600 pointer-events-none transition-colors"
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

      <!-- ================= INSTITUTES TABLE (Admin Only) ================= -->
      <div v-if="user?.role === 'Admin' && viewLevel === 'institute'">
        <div class="w-full mt-3 rounded-xl border overflow-hidden bg-white">
          <table class="min-w-full text-sm text-gray-700">
            <thead>
              <tr class="bg-defaultGreen text-white text-left">
                <th class="px-4 py-3 font-semibold">Institute Code</th>
                <th class="px-4 py-3 font-semibold">Institute Name</th>
                <th class="px-4 py-3 font-semibold text-center">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr
                v-for="inst in paginatedData"
                :key="inst.institute_id"
                class="hover:bg-gray-50 transition"
              >
                <td class="px-4 py-3">{{ inst.institute_code }}</td>
                <td class="px-4 py-3">{{ inst.institute_name }}</td>
                <td class="px-4 py-3">
                  <div class="flex justify-center">
                    <button
                      @click="viewPrograms(inst)"
                      class="px-3 py-1 h-8 border border-green-300 hover:bg-green-200 text-green-800 rounded-lg flex items-center gap-1"
                    >
                      <icon name="eye-open" /> View
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ================= PROGRAMS TABLE ================= -->
      <div v-else-if="viewLevel === 'program'">
        <div class="w-full mt-3 rounded-xl border overflow-hidden bg-white">
          <table class="min-w-full text-sm text-gray-700">
            <thead>
              <tr class="bg-defaultGreen text-white text-left">
                <th class="px-4 py-3 font-semibold">Program Code</th>
                <th class="px-4 py-3 font-semibold">Program Name</th>
                <th class="px-4 py-3 font-semibold text-center">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr
                v-for="prog in paginatedData"
                :key="prog.program_id"
                class="hover:bg-gray-50 transition"
              >
                <td class="px-4 py-3">{{ prog.program_code }}</td>
                <td class="px-4 py-3">{{ prog.program_name }}</td>
                <td class="px-4 py-3 text-center">
                  <button
                    @click="viewAssignClasses(prog)"
                    class="px-3 py-1 h-8 border border-green-300 hover:bg-green-200 text-green-800 rounded-lg flex items-center gap-1"
                  >
                    <icon name="eye-open" /> View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ================= ASSIGN CLASSES TABLE ================= -->
      <div v-else-if="viewLevel === 'assignClass'">
        <div class="w-full mt-3 rounded-xl border overflow-hidden bg-white">
          <table class="min-w-full text-sm text-gray-700">
            <thead>
              <tr class="bg-defaultGreen text-white text-left">
                <th class="px-4 py-3 font-semibold">#</th>
                <th class="px-4 py-3 font-semibold">Program</th>
                <th class="px-4 py-3 font-semibold">Course</th>
                <th class="px-4 py-3 font-semibold">Level</th>
                <th class="px-4 py-3 font-semibold">Set</th>
                <th class="px-4 py-3 font-semibold text-center">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr
                v-for="(cls, index) in paginatedData"
                :key="cls.assign_class_id"
                class="hover:bg-gray-50 transition"
              >
                <td class="px-4 py-3 text-gray-600 font-medium">
                  {{ startIndex + index }}
                </td>
                <td class="px-4 py-3">{{ cls.program?.program_code }}</td>
                <td class="px-4 py-3">{{ cls.course?.course_code }}</td>
                <td class="px-4 py-3">
                  {{ yearLabel(cls.course?.course_level) }}
                </td>
                <td class="px-4 py-3">{{ cls.set }}</td>
                <td class="px-4 py-3 text-center flex gap-2 justify-center">
                  <button
                    v-if="
                      user?.role === 'Admin' ||
                      user?.role === 'Program Chairperson'
                    "
                    @click="toggleEdit(cls)"
                    class="px-3 py-1 h-8 border border-green-300 hover:bg-green-200 text-green-800 rounded-lg flex items-center gap-1"
                  >
                    <icon name="edit" /> Edit
                  </button>
                  <button
                    v-if="
                      user?.role === 'Admin' ||
                      user?.role === 'Program Chairperson'
                    "
                    @click="toggleDelete(cls)"
                    class="px-3 py-1 h-8 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                  >
                    <icon name="delete" /> Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ================= PAGINATION ================= -->
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
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400 disabled:opacity-50"
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
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400 disabled:opacity-50"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ============ MODALS ============ -->
  <AddAssignClassModal
    v-if="isAdd"
    @close="closeView"
    @refresh="loadAssignClass"
  />
  <AddAssignClassModal
    v-if="showEditModal && selectedAssignClass"
    :assignClassData="selectedAssignClass"
    @close="closeModal"
    @refresh="loadAssignClass"
  />

  <!-- Delete Modal -->
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
import AddAssignClassModal from "../modals/add-assign-class.vue";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TableAssignClasses",
  components: { icon, AddAssignClassModal },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAdd: false,
      isTable: true,
      showDeleteModal: false,
      recordToDelete: null,
      selectedAssignClass: null,
      showEditModal: false,
      user: null,
      localAssignClass: [],
      viewLevel: "institute",
      selectedInstitute: null,
      selectedProgram: null,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["assignClass"]),
    filteredData() {
      const query = this.searchQuery.toLowerCase().trim();

      // ============= Institute View =============
      if (this.viewLevel === "institute") {
        const grouped = {};
        this.localAssignClass.forEach((item) => {
          const inst = item.program?.institute;
          if (inst) {
            if (!grouped[inst.institute_id]) {
              grouped[inst.institute_id] = { ...inst, programs: [] };
            }
            if (
              !grouped[inst.institute_id].programs.find(
                (p) => p.program_id === item.program.program_id
              )
            ) {
              grouped[inst.institute_id].programs.push(item.program);
            }
          }
        });
        let result = Object.values(grouped);

        if (query) {
          result = result.filter(
            (inst) =>
              inst.institute_code.toLowerCase().includes(query) ||
              inst.institute_name.toLowerCase().includes(query)
          );
        }
        return result;
      }

      // ============= Program View =============
      if (this.viewLevel === "program") {
        const grouped = {};
        this.localAssignClass
          .filter(
            (item) =>
              item.program?.institute_id ===
              this.selectedInstitute?.institute_id
          )
          .forEach((item) => {
            const prog = item.program;
            if (prog) {
              if (!grouped[prog.program_id]) {
                grouped[prog.program_id] = { ...prog, assignClasses: [] };
              }
              grouped[prog.program_id].assignClasses.push(item);
            }
          });
        let result = Object.values(grouped);

        if (query) {
          result = result.filter(
            (prog) =>
              prog.program_code.toLowerCase().includes(query) ||
              prog.program_name.toLowerCase().includes(query)
          );
        }
        return result;
      }

      // ============= Assign Classes View =============
      if (this.viewLevel === "assignClass") {
        let result = this.localAssignClass.filter(
          (item) =>
            item.program?.program_id === this.selectedProgram?.program_id
        );

        if (query) {
          result = result.filter((item) => {
            const searchable = [
              item.program?.program_code,
              item.program?.program_name,
              item.course?.course_code,
              item.course?.course_name,
              this.yearLabel(item.course?.course_level),
              item.set,
            ]
              .filter(Boolean)
              .join(" ")
              .toLowerCase();
            return searchable.includes(query);
          });
        }
        return result;
      }

      return [];
    },

    groupedByInstitute() {
      const grouped = {};
      this.localAssignClass.forEach((item) => {
        const inst = item.program?.institute;
        if (inst) {
          if (!grouped[inst.institute_id]) {
            grouped[inst.institute_id] = { ...inst, programs: [] };
          }
          if (
            !grouped[inst.institute_id].programs.find(
              (p) => p.program_id === item.program.program_id
            )
          ) {
            grouped[inst.institute_id].programs.push(item.program);
          }
        }
      });
      return Object.values(grouped);
    },
    groupedByProgram() {
      if (!this.selectedInstitute) return [];
      const grouped = {};
      this.localAssignClass
        .filter(
          (item) =>
            item.program?.institute_id === this.selectedInstitute.institute_id
        )
        .forEach((item) => {
          const prog = item.program;
          if (prog) {
            if (!grouped[prog.program_id]) {
              grouped[prog.program_id] = { ...prog, assignClasses: [] };
            }
            grouped[prog.program_id].assignClasses.push(item);
          }
        });
      return Object.values(grouped);
    },
    assignClassesByProgram() {
      if (!this.selectedProgram) return [];
      return this.localAssignClass.filter(
        (item) => item.program?.program_id === this.selectedProgram.program_id
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
  },
  methods: {
    viewPrograms(institute) {
      this.selectedInstitute = institute;
      this.viewLevel = "program";
    },
    viewAssignClasses(program) {
      this.selectedProgram = program;
      this.viewLevel = "assignClass";
    },
    backToInstitutes() {
      this.viewLevel = "institute";
      this.selectedInstitute = null;
    },
    backToPrograms() {
      this.viewLevel = "program";
      this.selectedProgram = null;
    },
    yearLabel(value) {
      const map = {
        1: "First Year",
        2: "Second Year",
        3: "Third Year",
        4: "Fourth Year",
      };
      return map[value] || value;
    },
    async fetchUser() {
      try {
        const response = await axios.get("http://localhost:8000/auth/me", {
          withCredentials: true,
        });
        if (response.data) {
          this.user = response.data;
          await this.loadAssignClassByRole();
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },
    async loadAssignClassByRole() {
      const store = useFetchDataStore();
      await store.fetchAssignClass();

      if (!this.user) return;

      if (this.user.role === "Admin") {
        this.localAssignClass = store.assignClass;
        this.viewLevel = "institute";
      } else if (this.user.role === "Program Chairperson") {
        // Filter assign classes to only this chairperson's institute
        this.localAssignClass = store.assignClass.filter(
          (cls) => cls.program?.institute_id === this.user.institute_id
        );

        // Automatically select the institute and go to program view
        const institute = this.localAssignClass[0]?.program?.institute;
        if (institute) {
          this.selectedInstitute = institute;
          this.viewLevel = "program";
        }
      } else {
        this.localAssignClass = [];
      }

      // Reset pagination
      this.currentPage = 1;
    },
    async loadAssignClass() {
      await this.loadAssignClassByRole();
    },
    toggleAdd() {
      this.isAdd = true;
    },
    toggleEdit(item) {
      this.selectedAssignClass = item;
      this.showEditModal = true;
    },
    toggleDelete(item) {
      this.recordToDelete = item;
      this.showDeleteModal = true;
    },
    confirmDelete() {
      if (!this.recordToDelete || isNaN(this.recordToDelete.assign_class_id)) {
        toast.error("Invalid assign class ID.");
        return;
      }
      const assignClassId = this.recordToDelete.assign_class_id;
      axios
        .delete(`http://localhost:8000/assign-class/delete-id/${assignClassId}`)
        .then(() => {
          this.recordToDelete = null;
          this.showDeleteModal = false;
          const audio = new Audio(require("@/assets/delete.mp3"));
          audio.play();
          this.loadAssignClass();
          toast.success("Class deleted successfully");
        })
        .catch((error) => {
          console.error("Delete failed:", error);
          toast.error("Failed to delete record.");
        });
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
    closeView() {
      this.isAdd = false;
    },
    closeModal() {
      this.showEditModal = false;
      this.selectedAssignClass = null;
    },
  },
  mounted() {
    this.fetchUser();
  },
};
</script>
