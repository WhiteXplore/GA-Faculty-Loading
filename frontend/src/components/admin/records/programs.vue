<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Programs</h1>
      <button
        @click="showUploadModal = true"
        class="bg-green-600 hover:bg-defaultGreen text-white px-4 py-2 rounded-md text-sm flex items-center gap-2 transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
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
        Upload Excel
      </button>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tablePrograms :key="tableKey" />
    </div>

    <!-- Upload Excel Modal -->
    <div
      v-if="showUploadModal"
      class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
      @click.self="closeModal"
    >
      <div
        class="bg-white rounded-lg shadow-xl max-w-md w-full p-6 animate-scaleUp"
      >
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-800">
            Upload Programs Excel File
          </h2>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <!-- Upload Instructions -->
        <div class="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <h3 class="font-semibold text-sm text-blue-800 mb-2">
            Excel Format Required:
          </h3>
          <ul class="text-xs text-blue-700 space-y-1">
            <li>• Column 1: Institute</li>
            <li>• Column 2: Program (Code)</li>
            <li>• Column 3: Program Name</li>
          </ul>
          <p class="text-xs text-blue-600 mt-2">
            Note: Duplicate programs will be skipped automatically.
          </p>
        </div>

        <!-- File Upload Area -->
        <div class="mb-4">
          <label
            for="file-upload"
            class="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
            :class="
              selectedFile ? 'border-green-500 bg-green-50' : 'border-gray-300'
            "
          >
            <div class="flex flex-col items-center justify-center pt-5 pb-6">
              <svg
                class="w-10 h-10 mb-3"
                :class="selectedFile ? 'text-green-500' : 'text-gray-400'"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
              <p
                class="mb-2 text-sm"
                :class="
                  selectedFile
                    ? 'text-defaultGreen font-semibold'
                    : 'text-gray-500'
                "
              >
                <span v-if="!selectedFile">Click to upload Excel file</span>
                <span v-else>{{ selectedFile.name }}</span>
              </p>
              <p class="text-xs text-gray-500">XLSX or XLS (MAX. 10MB)</p>
            </div>
            <input
              id="file-upload"
              type="file"
              class="hidden"
              accept=".xlsx,.xls"
              @change="handleFileSelect"
            />
          </label>
        </div>

        <!-- Upload Progress -->
        <div v-if="uploading" class="mb-4">
          <div class="flex items-center justify-center space-x-2">
            <div
              class="animate-spin rounded-full h-5 w-5 border-b-2 border-green-600"
            ></div>
            <span class="text-sm text-gray-600">Uploading...</span>
          </div>
        </div>

        <!-- Error Message -->
        <div
          v-if="errorMessage"
          class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md"
        >
          <p class="text-sm text-red-600">{{ errorMessage }}</p>
        </div>

        <!-- Success Message -->
        <div
          v-if="successMessage"
          class="mb-4 p-3 bg-green-50 border border-green-200 rounded-md"
        >
          <p class="text-sm text-defaultGreen">{{ successMessage }}</p>
          <p v-if="uploadResult" class="text-xs text-defaultGreen mt-1">
            Imported {{ uploadResult.imported }} of
            {{ uploadResult.total }} programs
            <span v-if="uploadResult.skipped > 0" class="text-yellow-600">
              ({{ uploadResult.skipped }} skipped - already exist)
            </span>
          </p>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-end space-x-3">
          <button
            @click="closeModal"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="uploadFile"
            :disabled="!selectedFile || uploading"
            class="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-defaultGreen disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            {{ uploading ? "Uploading..." : "Upload" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import tablePrograms from "./tables/table-programs.vue";
import axios from "axios";

export default {
  name: "ProgramsPage",
  components: {
    tablePrograms,
  },
  data() {
    return {
      showUploadModal: false,
      selectedFile: null,
      uploading: false,
      errorMessage: "",
      successMessage: "",
      uploadResult: null,
      tableKey: 0,
    };
  },
  methods: {
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        // Validate file size (10MB max)
        const maxSize = 10 * 1024 * 1024; // 10MB in bytes
        if (file.size > maxSize) {
          this.errorMessage = "File size must be less than 10MB";
          this.selectedFile = null;
          event.target.value = "";
          return;
        }

        // Validate file type
        const allowedTypes = [
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          "application/vnd.ms-excel",
        ];
        if (!allowedTypes.includes(file.type)) {
          this.errorMessage =
            "Please select a valid Excel file (.xlsx or .xls)";
          this.selectedFile = null;
          event.target.value = "";
          return;
        }

        this.selectedFile = file;
        this.errorMessage = "";
        this.successMessage = "";
      }
    },

    async uploadFile() {
      if (!this.selectedFile) {
        this.errorMessage = "Please select a file first";
        return;
      }

      this.uploading = true;
      this.errorMessage = "";
      this.successMessage = "";

      try {
        const formData = new FormData();
        formData.append("file", this.selectedFile);

        const response = await axios.post(
          "http://localhost:8000/programs/upload-excel",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          },
        );

        this.successMessage = response.data.message;
        this.uploadResult = response.data;

        // Refresh the table
        this.tableKey++;

        // Close modal after 2 seconds
        setTimeout(() => {
          this.closeModal();
        }, 2000);
      } catch (error) {
        console.error("Upload error:", error);
        this.errorMessage =
          error.response?.data?.message ||
          "Failed to upload file. Please try again.";
      } finally {
        this.uploading = false;
      }
    },

    closeModal() {
      this.showUploadModal = false;
      this.selectedFile = null;
      this.uploading = false;
      this.errorMessage = "";
      this.successMessage = "";
      this.uploadResult = null;
      // Reset file input
      const fileInput = document.getElementById("file-upload");
      if (fileInput) fileInput.value = "";
    },
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
