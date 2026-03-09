<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 w-screen"
  >
    <div
      class="flex justify-center items-center w-full max-w-md bg-white p-4 rounded-xl shadow-lg"
    >
      <div class="flex flex-col w-full">
        <!-- Header -->
        <div class="flex justify-start">
          <h1 class="font-semibold text-lg text-gray-800">Upload Rooms</h1>
        </div>
        <p class="text-sm text-gray-500 mt-1">
          Upload an Excel or CSV file containing the room list.
        </p>

        <!-- Drag & Drop Zone -->
        <div
          class="flex justify-center items-center cursor-pointer border-2 border-dashed border-gray-300 rounded-md p-8 w-full max-w-xl mx-auto mt-3"
          :class="{ 'bg-gray-100': dragging }"
          @dragover.prevent="dragging = true"
          @dragleave.prevent="dragging = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
        >
          <div class="text-center">
            <p v-if="!file" class="text-gray-600">
              <span class="text-defaultGreen">Upload a file</span> or drag and
              drop<br />
              Excel / CSV (.xlsx, .xls, .csv) up to 10MB
            </p>
            <p v-else class="text-defaultGreen">
              File uploaded: {{ file.name }}
            </p>

            <input
              type="file"
              class="hidden"
              ref="fileInput"
              @change="handleFileUpload"
              accept=".csv, .xlsx, .xls"
            />
          </div>
        </div>

        <!-- File Info -->
        <div class="mt-3 text-[13px] flex justify-between text-left">
          <div>
            <p class="text-gray-600">Accepted Files: .xlsx, .xls, .csv</p>
          </div>
        </div>

        <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

        <!-- Uploading -->
        <div
          v-if="uploading"
          class="text-defaultGreen text-sm flex items-center gap-2 mt-2"
        >
          <span
            class="animate-spin border-2 border-green-600 border-t-transparent rounded-full w-4 h-4"
          ></span>
          Uploading...
        </div>

        <!-- Actions -->
        <div class="tracking-wide flex justify-end gap-2 mt-4">
          <button
            class="bg-gray-200 p-2 px-3 rounded-lg text-gray-700 hover:bg-white border hover:border-gray-800 hover:text-gray-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
            @click="$emit('close')"
          >
            Cancel
          </button>
          <button
            class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transform transition-all duration-300 hover:scale-105 cursor-pointer"
            @click="submitUpload"
            :disabled="!file || uploading"
          >
            {{ uploading ? "Processing..." : "Upload" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as XLSX from "xlsx";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";

export default {
  name: "UploadRoomsPage",
  data() {
    return {
      file: null,
      dragging: false,
      uploading: false,
      parsedData: null,
      institutes: [],
    };
  },
  async mounted() {
    await this.loadInstitutes();
  },
  methods: {
    async loadInstitutes() {
      const store = useFetchDataStore();
      await store.fetchInstitutes();
      this.institutes = store.institutes;
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    handleDrop(e) {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files.length) this.handleFileUpload({ target: { files } });
      this.dragging = false;
    },

    handleFileUpload(event) {
      const selected = event.target.files[0];
      if (!selected) return;

      this.file = selected;

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: "array" });
          const worksheet = workbook.Sheets[workbook.SheetNames[0]];
          const json = XLSX.utils.sheet_to_json(worksheet, { defval: "" });

          if (!json.length) throw new Error("Empty file");

          // Map Excel data with type coercion
          this.parsedData = json
            .map((row) => {
              const instituteCode = row["Institute"] || "";
              const institute = this.institutes.find(
                (i) => i.institute_code === instituteCode,
              );

              return {
                institute_id: institute ? Number(institute.institute_id) : null,
                building_name: String(row["Building Name"] || "").trim(),
                level: String(row["Level / Floor"] || "").trim(),
                room_name: String(row["Room No / Name"] || "").trim(),
                room_capacity: parseInt(row["Room Size / Capacity"], 10) || 0,
                room_type: String(row["Lec / Lab"] || "").trim(),
              };
            })
            // Filter invalid rows
            .filter(
              (r) =>
                r.building_name &&
                r.level &&
                r.room_name &&
                r.room_capacity > 0 &&
                r.room_type,
            );

          console.log("ROOM DATA:", this.parsedData);
        } catch (err) {
          console.error("Error parsing file:", err);
          alert("Invalid or corrupted file.");
        }
      };

      reader.readAsArrayBuffer(selected);
    },

    async submitUpload() {
      if (!this.parsedData || !this.parsedData.length) {
        alert("Please upload a valid file first!");
        return;
      }

      this.uploading = true;

      try {
        // ✅ Send as bulk array to NestJS upload endpoint
        await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/rooms/add-rooms",
          this.parsedData,
        );

        toast.success("Rooms uploaded successfully!");
        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error(error);
        // Show backend validation errors if available
        if (error.response?.data?.message) {
          alert("Upload failed:\n" + error.response.data.message.join("\n"));
        } else {
          alert("Upload failed. Check console for details.");
        }
      } finally {
        this.uploading = false;
      }
    },
  },
};
</script>

<style scoped>
input[type="file"]:focus + div {
  outline: 2px dashed #22c55e;
  outline-offset: 2px;
}
</style>
