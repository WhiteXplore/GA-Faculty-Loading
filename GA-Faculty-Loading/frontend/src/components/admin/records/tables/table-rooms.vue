<template>
  <div v-if="isTable" class=" ">
    <div class="flex justify-between items-center px-1 text-sm">
      <!-- LEFT (Pages Title) -->
      <div class="text-[13px] text-text font-regular">
        Pages / Rooms Availability
      </div>

      <!-- RIGHT (Buttons) -->
      <div class="flex gap-2">
        <!-- Upload Room -->
        <div
          @click="isUploadModal = true"
          class="flex items-center gap-2 px-3 py-2 border bg-blue-700 text-white border-blue-700 rounded-xl hover:bg-white hover:text-blue-700 hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-blue-500 bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon name="uploads" />
          </div>

          <span class="font-medium text-sm">Upload Room</span>
        </div>

        <!-- Add Room -->
        <div
          @click="toggleAdd"
          class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon name="circle-add" />
          </div>

          <span class="font-medium text-sm">Add Room</span>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="mt-2 overflow-x-auto border p-3 rounded-xl bg-white">
      <!-- Top Controls -->
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
            <!-- Custom arrow -->
            <div
              class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-defaultGreen transition-colors"
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
          <!-- Search icon -->
          <div
            class="absolute inset-y-0 left-3 flex items-center text-defaultGreen pointer-events-none transition-colors"
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
                <th class="px-4 py-3 text-left font-normal w-[8%]">
                  Room Name
                </th>

                <th class="px-4 py-3 text-center font-normal w-[10%]">
                  Room Type
                </th>
                <th class="px-4 py-3 text-center font-normal w-[7%]">
                  Room Capacity
                </th>
                <th class="px-4 py-3 text-center font-normal w-[7%]">
                  Institute
                </th>
                <th class="px-4 py-3 text-left font-normal w-[15%]">
                  Building Name
                </th>

                <th
                  class="px-4 py-3 text-center rounded-tr-lg font-normal w-[1%]"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="rooms_data in paginatedData"
                :key="rooms_data.rooms_id"
                class="hover:bg-green-50 transition-all border-t"
              >
                <td class="px-4 py-3 text-left">
                  {{ rooms_data.room_name }}
                </td>

                <td class="px-4 py-3 text-center">
                  {{ rooms_data.room_type }}
                </td>
                <td class="px-4 py-3 text-center">
                  {{ rooms_data.room_capacity }}
                </td>
                <td class="px-4 py-3 text-center">
                  {{ rooms_data.institute?.institute_code || "-" }}
                </td>
                <td class="px-4 py-3 text-left">
                  {{ rooms_data.building?.building_name }}
                </td>

                <td class="px-4 py-3 flex justify-center">
                  <div class="flex gap-2 justify-center">
                    <button
                      class="w-[90px] h-8 border border-green-300 hover:bg-green-200 text-defaultGreen rounded-lg flex items-center justify-center gap-1 text-sm"
                      @click="toggleEdit(rooms_data)"
                    >
                      <icon name="edit" /> Edit
                    </button>

                    <button
                      class="w-[90px] h-8 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center justify-center gap-1 text-sm"
                      @click="toggleDelete(rooms_data)"
                    >
                      <icon name="delete" /> Delete
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="paginatedData.length === 0">
                <td colspan="6" class="text-left py-6 text-gray-400">
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
          <span v-for="page in pageNumbers" :key="'page-' + page">
            <button
              @click="changePage(page)"
              :class="{
                ' bg-defaultGreen text-white': currentPage === page,
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

  <addRooms v-if="isAdd" @close="closeView" @refresh="loadRooms" />
  <addRooms
    v-if="showEditModal && selectedRoom"
    :roomData="selectedRoom"
    @close="closeModal"
    @refresh="loadRooms"
  />
  <uploadRooms
    v-if="isUploadModal"
    @close="isUploadModal = false"
    @refresh="loadRooms"
  />

  <!-- Delete Confirmation Modal -->

  <!-- DELETE CONFIRMATION MODAL -->
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
        <b>{{ recordToDelete?.room_name }}</b> ? This action cannot be undone.
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
import addRooms from "../modals/add-rooms.vue";
import uploadRooms from "../modals/upload-rooms.vue";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TableRooms",
  components: {
    icon,
    addRooms,
    uploadRooms,
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAdd: false,
      isEdit: false,
      isTable: true,
      isUploadData: false,
      showDeleteModal: false,
      recordToDelete: null,
      selectedRoom: null,
      showEditModal: false,
      isUploadModal: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rooms"]),

    filteredData() {
      const query = this.searchQuery.toLowerCase();
      return this.rooms.filter((item) =>
        [
          item.room_name,
          item.room_type,
          item.room_capacity,
          item.institute?.institute_name,
        ]
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
    async loadRooms() {
      const store = useFetchDataStore();
      await store.fetchRooms();
    },
    toggleUploadData() {
      this.isUploadData = true;
      this.isTable = true;
    },
    toggleAdd() {
      this.isAdd = true;
      this.isTable = true;
    },
    toggleEdit(item) {
      this.selectedRoom = item;
      this.showEditModal = true;
    },
    toggleDelete(item) {
      this.recordToDelete = item;
      this.showDeleteModal = true;
    },
    confirmDelete() {
      if (!this.recordToDelete || isNaN(this.recordToDelete.room_id)) {
        toast.error("Invalid room ID.");
        return;
      }

      const roomId = this.recordToDelete.room_id;

      axios
        .delete(process.env.VUE_APP_API_BASE_URL + `/rooms/delete-id/${roomId}`)
        .then(() => {
          this.recordToDelete = null;
          this.showDeleteModal = false;

          // Play sound after successful delete
          const audio = new Audio(require("@/assets/delete.mp3"));
          audio.play();

          this.loadRooms(); // refresh the list from backend
          toast.success("Record deleted successfully");
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
      this.isUploadData = false;
    },
    closeModal() {
      this.showEditModal = false;
      this.selectedRoom = null;
    },
    handleBackToTable() {
      this.isEdit = false;
      this.isAdd = false;
      this.isUploadData = false;
      this.isTable = true;
    },
  },
  mounted() {
    this.loadRooms();
  },
};
</script>
