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
          <h1 class="font-semibold text-lg text-gray-800">Upload Courses</h1>
        </div>
        <p class="text-sm text-gray-500 mt-1">
          Upload an Excel or CSV file containing the course list.
        </p>

        <!-- Drag & Drop / Click Zone -->
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
              <span class="text-green-600">Upload a file</span> or drag and
              drop<br />
              Excel / CSV (.xlsx, .xls, .csv) up to 10MB
            </p>
            <p v-else class="text-green-600">File uploaded: {{ file.name }}</p>

            <input
              type="file"
              class="hidden"
              ref="fileInput"
              @change="handleFileUpload"
              accept=".csv, .xlsx, .xls"
            />
          </div>
        </div>

        <!-- Accepted Files Info -->
        <div class="mt-3 text-[13px] flex justify-between text-left">
          <div>
            <p class="text-gray-600">Accepted Files: .xlsx, .xls, .csv</p>
            <p class="text-green-700">example.xlsx</p>
          </div>
        </div>

        <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

        <!-- Uploading Status -->
        <div
          v-if="uploading"
          class="text-green-600 text-sm flex items-center gap-2 mt-2"
        >
          <span
            class="animate-spin border-2 border-green-600 border-t-transparent rounded-full w-4 h-4"
          ></span>
          Uploading...
        </div>

        <!-- Action Buttons -->
        <div class="tracking-wide flex justify-end gap-2 mt-4">
          <button
            class="bg-red-600 p-2 px-3 rounded-md text-white hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md"
            @click="$emit('close')"
          >
            Cancel
          </button>
          <button
            class="bg-green-600 p-2 px-3 rounded-md text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
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

export default {
  name: "UploadCoursesPage",
  data() {
    return {
      file: null,
      dragging: false,
      uploading: false,
      parsedData: null,
    };
  },
  methods: {
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

          // Example Transformations
          const instituteMap = {
            IC: "Institute of Computing",
            ITED: "Institute of Teacher Education",
            ILEGG:
              "Institute of Leadership, Entrepreneurship and Good Governance",
            IAAS: "Institute of Applied and Aquatic Sciences",
          };

          const programMap = {
            "Bachelor of Science in Information Technology": "BSIT",
            "Bachelor of Science in Information Systems": "BSIS",
            "Bachelor of Science in Agro-Forestry": "BSAF",
            "Bachelor of Science in Fisheries and Aquatic Sciences": "BSFAS",
            "Bachelor of Science in Food Technology": "BFT",
            "Bachelor of Science in Marine Biology": "BSMB",
            "Bachelor of Public Administration": "BPA",
            "Bachelor of Science in Disaster Resiliency and Management":
              "BSDRM",
            "Bachelor of Science in Entrepreneurship": "BSE",
            "Bachelor of Science in Social Work": "BSW",
            "Bachelor of Science in Tourism Management": "BSTM",
            "Bachelor of Arts in Communication": "BSAC",
            "Bachelor of Secondary Education": "BSE",
            "Bachelor of Technology and Livelihood Education": "BTLE",
            "Bachelor of Physical Education": "BPE",
          };

          const semesterMap = { First: 1, Second: 2 };

          this.parsedData = json.map((row) => {
            const [start, end] = row["School Year"]
              .split("-")
              .map((y) => Number(y.trim()));

            return {
              curriculum_start_year: start,
              curriculum_end_year: end,
              institute_code: row.Institute.trim(),
              institute_name: instituteMap[row.Institute.trim()] || "",
              program_code: programMap[row.Program.trim()] || "",
              program_name: row.Program.trim(),
              course_level: Number(row["Year Level"]),
              course_semester: semesterMap[row.Semester.trim()] || 0,
              course_code: row["Course Code"].trim(),
              course_title: row["Course Title"].trim(),
              course_lec: Number(row["Lecture Units"]),
              course_lab: Number(row["Laboratory Units"]),
            };
          });

          console.log("Transformed Data:", this.parsedData);
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
        // 1️⃣ Create only one institute (first row)
        const firstInstituteRow = this.parsedData[0];
        const instituteRes = await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/institute/add-institute",
          {
            institute_code: firstInstituteRow.institute_code,
            institute_name: firstInstituteRow.institute_name,
          }
        );
        const institute = instituteRes.data; // shared institute_id

        // 2️⃣ Deduplicate programs by program_code
        const uniquePrograms = [
          ...new Map(
            this.parsedData.map((row) => [row.program_code, row])
          ).values(),
        ];

        const programMap = new Map(); // program_code => program_id
        const curriculumMap = new Map(); // program_code => curriculum_id

        // 3️⃣ Create programs and their curriculums
        for (const prog of uniquePrograms) {
          // Create program
          const programRes = await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/programs/add-programs",
            {
              program_code: prog.program_code,
              program_name: prog.program_name,
              institute_id: institute.institute_id,
            }
          );
          const program = programRes.data;
          programMap.set(prog.program_code, program.program_id);

          // Create curriculum for this program
          const curriculumRes = await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/curriculums/add-curriculums",
            {
              curriculum_start_year: prog.curriculum_start_year,
              curriculum_end_year: prog.curriculum_end_year,
              institute_id: institute.institute_id,
              program_id: program.program_id,
            }
          );
          const curriculum = curriculumRes.data;
          curriculumMap.set(prog.program_code, curriculum.curriculum_id);
        }

        // 4️⃣ Map courses to the correct program & curriculum
        const coursesPayload = this.parsedData.map((row) => ({
          course_level: row.course_level,
          course_semester: row.course_semester,
          course_code: row.course_code,
          course_title: row.course_title,
          course_lec: row.course_lec,
          course_lab: row.course_lab,
          institute_id: institute.institute_id,
          program_id: programMap.get(row.program_code),
          curriculum_id: curriculumMap.get(row.program_code),
        }));

        // 5️⃣ Upload courses
        await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/courses/add-courses",
          coursesPayload
        );

        this.$emit("refresh");
        toast.success("Upload successful!");
        this.$emit("close");
      } catch (error) {
        console.error(error);
        alert("Upload failed.");
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
