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
          class="text-defaultGreen text-sm flex items-center gap-2 mt-2"
        >
          <span
            class="animate-spin border-2 border-green-600 border-t-transparent rounded-full w-4 h-4"
          ></span>
          Uploading...
        </div>

        <!-- Action Buttons -->
        <div class="tracking-wide flex justify-end gap-2 mt-4">
          <button
            class="bg-gray-200 p-2 px-3 rounded-lg text-gray-700 hover:bg-white border hover:border-gray-800 hover:text-gray-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
            @click="$emit('close')"
          >
            Cancel
          </button>
          <button
            class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
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
            BSIT: "Bachelor of Science in Information Technology",
            BSIS: "Bachelor of Science in Information Systems",
            BSAF: "Bachelor of Science in Agro-Forestry",
            BSFAS: "Bachelor of Science in Fisheries and Aquatic Sciences",
            BSFT: "Bachelor of Science in Food Technology",
            BSMB: "Bachelor of Science in Marine Biology",
            BPA: "Bachelor of Public Administration",
            BSDRM: "Bachelor of Science in Disaster Resiliency and Management",
            BSENTREP: "Bachelor of Science in Entrepreneurship",
            BSSW: "Bachelor of Science in Social Work",
            BSTM: "Bachelor of Science in Tourism Management",
            BSEDMATH: "Bachelor of Secondary Education Major in Math",
            BSEDSCI: "Bachelor of Secondary Education Major in Science",
            BSEDENG: "Bachelor of Secondary Education Major in English",
            BACOMM: "Bachelor of Arts in Communication",
            BTLEd: "Bachelor of Technology and Livelihood Education",
            BPE: "Bachelor of Physical Education",
          };

          this.parsedData = json.map((row) => {
            const [start, end] = row["School Year"]
              .split("-")
              .map((y) => Number(y.trim()));

            return {
              curriculum_start_year: start,
              curriculum_end_year: end,
              institute_code: row.Institute.trim(),
              institute_name: instituteMap[row.Institute.trim()] || "",
              program_code: row.Program.trim(), // Already a code in your data
              program_name:
                programMap[row.Program.trim()] || row.Program.trim(),
              course_level: Number(row["Year Level"]),
              course_semester: Number(row.Semester),
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
        toast.warning("Please upload a valid file first!");
        return;
      }

      this.uploading = true;

      try {
        const fetchDataStore = useFetchDataStore();

        // 🔹 Ensure courses are loaded
        if (!fetchDataStore.courses.length) {
          await fetchDataStore.fetchCourses();
        }

        const existingCourses = fetchDataStore.courses;

        // 🔹 Normalize helper
        const normalize = (val) =>
          String(val || "")
            .replace(/\s+/g, "")
            .toUpperCase()
            .trim();

        const existingSet = new Set(
          existingCourses
            .map((course) => {
              if (!course.curriculum || !course.curriculum.program) return null;

              const start = course.curriculum?.curriculum_start_year;
              const end = course.curriculum?.curriculum_end_year;

              return `${normalize(course.course_code)}-${
                course.curriculum.program.program_code
              }-${
                course.curriculum.program.institute?.institute_code
              }-${start}-${end}-${course.course_level}-${
                course.course_semester
              }`;
            })
            .filter(Boolean), // removes null
        );
        // 🔹 Deduplicate institutes
        const uniqueInstitutes = [
          ...new Map(
            this.parsedData.map((row) => [row.institute_code, row]),
          ).values(),
        ];

        const instituteMap = new Map();

        for (const inst of uniqueInstitutes) {
          const res = await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/institute/add-institute",
            {
              institute_code: inst.institute_code,
              institute_name: inst.institute_name,
            },
          );

          instituteMap.set(inst.institute_code, res.data.institute_id);
        }

        // 🔹 Deduplicate programs
        const uniquePrograms = [
          ...new Map(
            this.parsedData.map((row) => [
              `${row.institute_code}-${row.program_code}`,
              row,
            ]),
          ).values(),
        ];

        const programMap = new Map();
        const curriculumMap = new Map();

        for (const prog of uniquePrograms) {
          const programRes = await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/programs/add-programs",
            {
              program_code: prog.program_code,
              program_name: prog.program_name,
              institute_id: instituteMap.get(prog.institute_code),
            },
          );

          const program = programRes.data;

          programMap.set(
            `${prog.institute_code}-${prog.program_code}`,
            program.program_id,
          );

          const curriculumRes = await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/curriculums/add-curriculums",
            {
              curriculum_start_year: prog.curriculum_start_year,
              curriculum_end_year: prog.curriculum_end_year,
              institute_id: instituteMap.get(prog.institute_code),
              program_id: program.program_id,
            },
          );

          const curriculum = curriculumRes.data;

          curriculumMap.set(
            `${prog.institute_code}-${prog.program_code}`,
            curriculum.curriculum_id,
          );
        }

        // 🔹 Prepare course payload
        const coursesPayload = this.parsedData.map((row) => {
          const curriculum_id = curriculumMap.get(
            `${row.institute_code}-${row.program_code}`,
          );

          const key = `${normalize(row.course_code)}-${row.program_code}-${
            row.institute_code
          }-${row.curriculum_start_year}-${row.curriculum_end_year}-${
            row.course_level
          }-${row.course_semester}`;

          return {
            key,
            payload: {
              course_level: row.course_level,
              course_semester: row.course_semester,
              course_code: row.course_code,
              course_title: row.course_title,
              course_lec: row.course_lec,
              course_lab: row.course_lab,
              institute_id: instituteMap.get(row.institute_code),
              program_id: programMap.get(
                `${row.institute_code}-${row.program_code}`,
              ),
              curriculum_id: curriculum_id,
            },
          };
        });

        // 🔹 Filter duplicates
        const newCourses = coursesPayload
          .filter((course) => !existingSet.has(course.key))
          .map((course) => course.payload);

        // 🔹 If everything exists
        if (!newCourses.length) {
          toast.warning("All uploaded courses already exist in the database.");
          this.uploading = false;
          return;
        }

        // 🔹 Upload only new courses
        await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/courses/add-courses",
          newCourses,
        );

        toast.success(`${newCourses.length} new courses uploaded successfully`);

        // 🔹 Refresh store
        await fetchDataStore.fetchCourses();

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error(error);
        toast.error("Upload failed.");
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
