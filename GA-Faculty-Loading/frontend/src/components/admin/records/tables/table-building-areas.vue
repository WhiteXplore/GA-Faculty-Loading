<template>
  <div v-if="isTable">
    <!-- HEADER -->
    <div class="flex justify-between items-center px-1 text-sm">
      <div class="text-[13px] text-text font-regular">
        Pages / Buildings Areas
      </div>

      <div class="flex gap-2">
        <!-- Upload -->
        <div
          @click="isUploadModal = true"
          class="flex items-center gap-2 px-3 py-2 border bg-blue-700 text-white border-blue-700 rounded-xl hover:bg-white hover:text-blue-700 hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-blue-500 bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon name="uploads" />
          </div>

          <span class="font-medium text-sm"> Upload Building Areas </span>
        </div>

        <!-- Add -->
        <div
          @click="toggleAdd"
          class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon name="circle-add" />
          </div>

          <span class="font-medium text-sm"> Add Building Areas </span>
        </div>
      </div>
    </div>

    <!-- TABLE CONTAINER -->
    <div class="mt-2 overflow-x-auto border p-3 rounded-xl bg-white">
      <!-- CONTROLS -->
      <div
        class="flex justify-between items-center flex-wrap gap-3 text-gray-700 bg-white"
      >
        <!-- PER PAGE -->
        <div class="flex items-center gap-2">
          <select
            v-model="itemsPerPage"
            @change="changePage(1)"
            class="rounded-full border border-green-600 bg-white px-3 py-1 text-sm font-semibold"
          >
            <option value="10">10</option>
            <option value="15">15</option>
            <option value="20">20</option>
          </select>

          <span class="text-sm font-medium text-gray-600"> Per page </span>
        </div>

        <!-- SEARCH -->
        <div class="relative w-full sm:w-64 md:w-72 lg:w-80">
          <input
            v-model="searchQuery"
            @input="changePage(1)"
            type="text"
            placeholder="Search..."
            class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full"
          />

          <div
            class="absolute inset-y-0 left-3 flex items-center text-defaultGreen"
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

      <!-- TABLE -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[69vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead class="bg-defaultGreen text-white sticky top-0">
              <tr>
                <th class="px-4 py-3 text-left font-normal w-[40%]">
                  College Branch
                </th>
                <th class="px-4 py-3 text-left font-normal w-[40%]">
                  Area Name
                </th>

                <th class="px-4 py-3 text-left font-normal w-[30%]">
                  Time Travel
                </th>

                <th class="px-4 py-3 text-center font-normal w-[30%]">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="area in paginatedData"
                :key="area.building_area_id"
                class="hover:bg-green-50 border-t"
              >
                <td class="px-4 py-3">
                  {{ area.collegeBranch?.college_branch_name }}
                </td>
                <td class="px-4 py-3">
                  {{ area.area_name }}
                </td>

                <td class="px-4 py-3">
                  {{ area.time_travel ?? "-" }}
                </td>

                <td class="px-4 py-3 text-center">
                  <div class="flex justify-center gap-2">
                    <button
                      class="w-[90px] h-8 border border-green-300 hover:bg-green-200 text-defaultGreen rounded-lg flex items-center justify-center gap-1 text-sm"
                      @click="toggleEdit(area)"
                    >
                      <icon name="edit" />
                      Edit
                    </button>

                    <button
                      class="px-3 py-1 h-8 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                      @click="toggleDelete(area)"
                    >
                      <icon name="delete" />
                      Delete
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="paginatedData.length === 0">
                <td colspan="3" class="text-center py-8 text-gray-400">
                  No records found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- PAGINATION -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-gray-700 text-sm">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredData.length }} entries
        </div>

        <div class="flex items-center gap-1 text-sm">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 rounded-l-md disabled:opacity-50"
          >
            &lt;
          </button>

          <button
            v-for="page in pageNumbers"
            :key="page"
            @click="changePage(page)"
            :class="[
              'px-3 py-1 rounded-md',
              currentPage === page
                ? 'bg-defaultGreen text-white'
                : 'bg-gray-200',
            ]"
          >
            {{ page }}
          </button>

          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 bg-gray-300 rounded-r-md disabled:opacity-50"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>

    <!-- ADD MODAL -->
    <addBuilding v-if="isAdd" @close="isAdd = false" @refresh="loadBuildings" />

    <!-- EDIT MODAL -->
    <addBuilding
      v-if="showEditModal"
      :buildingData="selectedBuilding"
      @close="closeModal"
      @refresh="loadBuildings"
    />
  </div>
  <div
    v-if="showDeleteModal"
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div
      class="rounded-xl shadow-lg w-[320px] md:w-[420px] bg-white py-6 px-4 flex flex-col items-center"
    >
      <div
        class="rounded-full w-20 h-20 flex justify-center items-center bg-red-300 animate-pulse"
      >
        <icon name="question" class="w-10 h-10 text-white" />
      </div>

      <h1 class="text-[16px] font-semibold mt-4">Delete Confirmation</h1>

      <p class="mt-2 text-[13px] text-center px-8">
        Are you sure you want to delete
        <b>{{ areaToDelete?.area_name }}</b> ? This action cannot be undone.
      </p>

      <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

      <div class="tracking-wide flex gap-2 mt-4">
        <button
          class="bg-red-400 p-2 px-3 text-[13px] rounded-md text-white hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md"
          @click="showDeleteModal = false"
        >
          No, Cancel
        </button>

        <button
          class="bg-green-400 p-2 px-3 text-[13px] rounded-md text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
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
import addBuilding from "../modals/add-building-areas.vue";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";
import { toast } from "vue3-toastify";

export default {
  name: "TableBuildingAreas",

  components: {
    icon,
    addBuilding,
  },

  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",

      isAdd: false,
      isUploadModal: false,
      isTable: true,

      selectedBuilding: null,
      showEditModal: false,

      showDeleteModal: false,
      areaToDelete: null,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["building_areas"]),

    filteredData() {
      const query = (this.searchQuery || "").toLowerCase();

      return this.building_areas.filter((item) =>
        [item.area_name, item.time_travel]
          .join(" ")
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
  },

  methods: {
    async loadBuildings() {
      const store = useFetchDataStore();
      await store.fetchBuildingAreas(); // ✅ FIXED
    },

    toggleAdd() {
      this.isAdd = true;
    },

    toggleEdit(item) {
      this.selectedBuilding = item;
      this.showEditModal = true;
    },

    toggleDelete(item) {
      this.areaToDelete = item;
      this.showDeleteModal = true;
    },

    async confirmDelete() {
      try {
        await axios.delete(
          process.env.VUE_APP_API_BASE_URL +
            `/building-areas/${this.areaToDelete.building_area_id}`,
        );

        toast.success("Building area deleted successfully");

        this.showDeleteModal = false;
        this.areaToDelete = null;

        this.loadBuildings();
      } catch (error) {
        toast.error("Failed to delete building area");
      }
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },

    closeModal() {
      this.showEditModal = false;
      this.selectedBuilding = null;
    },

    formatTravelTime(minutes) {
      if (!minutes) return "-";

      const hours = Math.floor(minutes / 60);
      const mins = minutes % 60;

      if (hours === 0) return `${mins} Minutes`;
      if (mins === 0) return `${hours} Hour${hours > 1 ? "s" : ""}`;

      return `${hours} Hour ${mins} Minutes`;
    },
  },

  mounted() {
    this.loadBuildings();
  },
};
</script>
