<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center">
    <!-- Overlay -->
    <div
      class="absolute inset-0 bg-gray-800 bg-opacity-40"
      @click="$emit('close')"
    ></div>

    <!-- Modal Content -->
    <div
      class="relative bg-white rounded-xl w-[400px] md:w-[500px] p-6 flex flex-col gap-4 shadow-lg"
    >
      <h2 class="text-lg font-semibold text-gray-800">Upload Courses</h2>
      <p class="text-sm text-gray-500">
        Upload an Excel or CSV file containing the course list. Make sure the
        format matches the required template.
      </p>

      <!-- File Input -->
      <label
        class="border border-green-600 rounded-lg p-4 text-sm cursor-pointer text-center hover:bg-green-50 transition"
      >
        <input
          type="file"
          @change="handleFileUpload"
          accept=".csv, .xlsx, .xls"
          class="hidden"
        />
        <div v-if="!fileName">Click or drag file here</div>
        <div v-else>
          Selected file: <span class="font-medium">{{ fileName }}</span>
        </div>
      </label>

      <!-- Upload Status -->
      <div
        v-if="uploading"
        class="text-green-600 text-sm flex items-center gap-2"
      >
        <span
          class="animate-spin border-2 border-green-600 border-t-transparent rounded-full w-4 h-4"
        ></span>
        Uploading...
      </div>

      <!-- Actions -->
      <div class="flex justify-end gap-2 mt-4">
        <button
          @click="$emit('close')"
          class="px-3 py-1 bg-gray-200 rounded-lg text-gray-700 hover:bg-gray-300"
        >
          Cancel
        </button>
        <button
          @click="submitUpload"
          :disabled="!file || uploading"
          class="px-3 py-1 bg-green-600 rounded-lg text-white hover:bg-green-700 disabled:opacity-50"
        >
          {{ uploading ? "Processing..." : "Upload" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import * as XLSX from "xlsx";
import axios from "axios";

export default {
  name: "UploadCoursesPage",
  data() {
    return {
      file: null,
      fileName: "",
      uploading: false,
      parsedData: null,
    };
  },
  methods: {
    handleFileUpload(event) {
      const selected = event.target.files[0];
      if (!selected) return;

      this.file = selected;
      this.fileName = selected.name;

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: "array" });
          const sheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[sheetName];
          const json = XLSX.utils.sheet_to_json(worksheet, { defval: "" });

          if (!json.length) throw new Error("Empty file or invalid format.");

          this.parsedData = json;
          console.log("📄 Parsed Excel to JSON:", json);
        } catch (err) {
          console.error("❌ Error parsing file:", err);
          alert("Invalid or corrupted file format.");
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
        const first = this.parsedData[0];

        // Validate required fields
        if (
          !first.institute_code ||
          !first.institute_name ||
          !first.program_code ||
          !first.program_name
        ) {
          throw new Error("Missing required fields in the uploaded file.");
        }

        // 1️⃣ Add Institute
        const institutePayload = {
          institute_code: first.institute_code.trim(),
          institute_name: first.institute_name.trim(),
        };
        const instituteRes = await axios.post(
          "http://localhost:8000/institute/add-institute",
          institutePayload
        );
        const institute = instituteRes.data;
        console.log("✅ Institute added:", institute);

        // 2️⃣ Add Program
        const programPayload = {
          program_code: first.program_code.trim(),
          program_name: first.program_name.trim(),
          institute_id: institute.institute_id, // ✅ your naming format
        };
        const programRes = await axios.post(
          "http://localhost:8000/programs/add-programs",
          programPayload
        );
        const program = programRes.data;
        console.log("✅ Program added:", program);

        // 3️⃣ Add Curriculum
        const curriculumPayload = {
          curriculum_start_year: Number(first.curriculum_start_year),
          curriculum_end_year: Number(first.curriculum_end_year),
          institute_id: institute.institute_id,
          program_id: program.program_id,
        };
        const curriculumRes = await axios.post(
          "http://localhost:8000/curriculums/add-curriculums",
          curriculumPayload
        );
        const curriculum = curriculumRes.data; // returns curriculum_id

        console.log("✅ Curriculum added:", curriculum);

        // 4️⃣ Add Courses
        const coursesPayload = this.parsedData.map((row) => ({
          course_code: row.course_code?.trim(),
          course_title: row.course_title?.trim(),
          course_level: Number(row.course_level) || 0,
          course_semester: Number(row.course_semester) || 0,
          course_lec: Number(row.course_lec) || 0,
          course_lab: Number(row.course_lab) || 0,
          institute_id: institute.institute_id,
          program_id: program.program_id,
          curriculum_id: curriculum.curriculum_id,
        }));

        const coursesRes = await axios.post(
          "http://localhost:8000/courses/add-courses",
          coursesPayload
        );

        const courses = coursesRes.data;
        console.log("✅ Courses added:", courses);

        // Final structure
        const finalPayload = {
          message: "Courses uploaded successfully and linked to curriculum",
          institute,
          program,
          curriculum,
          courses,
        };

        console.log("🚀 Final JSON:", finalPayload);

        alert("✅ Upload process completed successfully!");
        this.$emit("close");
      } catch (error) {
        console.error("❌ Upload failed:", error);
        alert("Upload failed. Please check the console for details.");
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
