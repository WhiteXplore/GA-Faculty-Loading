<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <div class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5">
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-purple-600 text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
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
            <h1 class="font-bold tracking-wide text-lg">
              Import User Expertise
            </h1>
          </div>
          <button
            @click="$emit('close')"
            class="text-white hover:text-gray-200 cursor-pointer"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
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

        <!-- Form Content -->
        <div class="p-5 w-[35vw] space-y-4">
          <!-- Instructions -->
          <div class="bg-purple-50 border-l-4 border-purple-500 p-4 rounded">
            <h3 class="font-bold text-purple-800 mb-2">Import Instructions:</h3>
            <ul class="text-purple-700 text-sm space-y-1">
              <li>• File must be in XLSX format (.xlsx)</li>
              <li>• Required columns: Instructors Name, Course Code</li>
              <li>• Instructor name format: "Last Name, First Name"</li>
              <li>• Course codes must match existing courses in the system</li>
            </ul>
          </div>

          <!-- Download Template Button -->
          <div class="flex justify-center">
            <button
              type="button"
              @click="downloadTemplate"
              class="flex items-center gap-2 px-4 py-2 border border-purple-600 text-purple-600 rounded-lg hover:bg-purple-700 hover:text-white transition duration-200"
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
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              Download Template
            </button>
          </div>

          <!-- File Upload Area -->
          <div class="space-y-2">
            <label class="font-bold text-gray-800">Upload XLSX File:</label>
            <div
              @dragover.prevent="dragOver = true"
              @dragleave.prevent="dragOver = false"
              @drop.prevent="handleFileDrop"
              :class="[
                'border-2 border-dashed rounded-lg p-6 text-center transition-all',
                dragOver
                  ? 'border-purple-500 bg-purple-50'
                  : 'border-gray-300 bg-gray-50',
              ]"
            >
              <input
                ref="fileInput"
                type="file"
                accept=".xlsx"
                @change="handleFileChange"
                class="hidden"
              />

              <div v-if="!selectedFile" class="space-y-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-12 w-12 mx-auto text-gray-400"
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
                <p class="text-gray-600">
                  Drag & drop your XLSX file here, or
                  <button
                    type="button"
                    @click="$refs.fileInput.click()"
                    class="text-purple-600 hover:text-purple-700 font-semibold underline"
                  >
                    browse
                  </button>
                </p>
              </div>

              <div v-else class="space-y-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-12 w-12 mx-auto text-purple-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                <p class="text-gray-800 font-semibold">
                  {{ selectedFile.name }}
                </p>
                <p class="text-gray-500 text-sm">
                  {{ formatFileSize(selectedFile.size) }}
                </p>
                <button
                  type="button"
                  @click="clearFile"
                  class="text-red-600 hover:text-red-700 text-sm font-semibold"
                >
                  Remove file
                </button>
              </div>
            </div>
          </div>

          <!-- Progress Bar -->
          <div v-if="uploading" class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Uploading and processing...</span>
              <span class="text-gray-800 font-semibold"
                >{{ uploadProgress }}%</span
              >
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div
                class="bg-purple-600 h-2.5 rounded-full transition-all duration-300"
                :style="{ width: uploadProgress + '%' }"
              ></div>
            </div>
          </div>

          <!-- Import Results -->
          <div v-if="importResults" class="space-y-3">
            <div
              class="bg-green-50 border-l-4 border-green-500 p-4 rounded"
              v-if="importResults.success > 0"
            >
              <p class="font-semibold text-green-800">
                ✓ Successfully imported {{ importResults.success }} expertise
                records
              </p>
            </div>

            <div
              class="bg-red-50 border-l-4 border-red-500 p-4 rounded"
              v-if="importResults.failed > 0"
            >
              <p class="font-semibold text-red-800 mb-2">
                ✗ Failed to import {{ importResults.failed }} expertise records
              </p>
              <div class="max-h-40 overflow-y-auto space-y-2">
                <div
                  v-for="(error, index) in importResults.errors"
                  :key="index"
                  class="text-sm text-red-700 bg-red-100 p-2 rounded"
                >
                  <p>
                    <strong>Row {{ error.row }}:</strong> {{ error.error }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-end gap-3 pt-4">
            <button
              type="button"
              @click="$emit('close')"
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition duration-200"
            >
              Cancel
            </button>
            <button
              type="button"
              @click="handleImport"
              :disabled="!selectedFile || uploading"
              :class="[
                'px-4 py-2 rounded-lg transition duration-200',
                selectedFile && !uploading
                  ? 'bg-purple-600 text-white hover:bg-purple-700'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed',
              ]"
            >
              {{ uploading ? "Importing..." : "Import Expertise" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
import * as XLSX from "xlsx";

export default {
  name: "ImportExpertise",
  data() {
    return {
      selectedFile: null,
      uploading: false,
      uploadProgress: 0,
      dragOver: false,
      importResults: null,
    };
  },
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file && file.name.endsWith(".xlsx")) {
        this.selectedFile = file;
        this.importResults = null;
      } else {
        toast.error("Please select a valid XLSX file");
      }
    },
    handleFileDrop(event) {
      this.dragOver = false;
      const file = event.dataTransfer.files[0];
      if (file && file.name.endsWith(".xlsx")) {
        this.selectedFile = file;
        this.importResults = null;
      } else {
        toast.error("Please select a valid XLSX file");
      }
    },
    clearFile() {
      this.selectedFile = null;
      this.importResults = null;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = "";
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
    },
    downloadTemplate() {
      // Create sample data based on the screenshot
      const templateData = [
        {
          "Instructors Name": "Acdal, April M.",
          "Course Code": "RR325",
        },
        {
          "Instructors Name": "Acdal, April M.",
          "Course Code": "ER327",
        },
        {
          "Instructors Name": "Anobong Jr., Anselmo G.",
          "Course Code": "GEELECT1",
        },
        {
          "Instructors Name": "Balio, Ariel, Jr. C.",
          "Course Code": "THE223",
        },
        {
          "Instructors Name": "Bangasin, Alneza M.",
          "Course Code": "LIT121",
        },
      ];

      // Create workbook and worksheet
      const ws = XLSX.utils.json_to_sheet(templateData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Expertise");

      // Set column widths
      ws["!cols"] = [{ wch: 30 }, { wch: 15 }];

      // Download file
      XLSX.writeFile(wb, "user_expertise_import_template.xlsx");
      toast.success("Template downloaded successfully");
    },
    async handleImport() {
      if (!this.selectedFile) {
        toast.error("Please select a file to import");
        return;
      }

      this.uploading = true;
      this.uploadProgress = 0;
      this.importResults = null;

      try {
        const formData = new FormData();
        formData.append("file", this.selectedFile);

        // Simulate progress
        const progressInterval = setInterval(() => {
          if (this.uploadProgress < 90) {
            this.uploadProgress += 10;
          }
        }, 200);

        const response = await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/users/import-expertise",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          },
        );

        clearInterval(progressInterval);
        this.uploadProgress = 100;

        this.importResults = {
          success: response.data.success,
          failed: response.data.failed,
          errors: response.data.errors || [],
        };

        if (response.data.success > 0) {
          toast.success(
            `Successfully imported ${response.data.success} expertise records!`,
          );
          this.$emit("refresh");
        }

        if (response.data.failed > 0) {
          toast.warning(
            `${response.data.failed} expertise records failed to import. Check details below.`,
          );
        }
      } catch (error) {
        console.error("Import failed:", error);
        toast.error(
          error.response?.data?.message ||
            "Failed to import expertise. Please try again.",
        );
      } finally {
        this.uploading = false;
      }
    },
  },
};
</script>

<style scoped>
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}
</style>
