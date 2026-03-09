<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="assignClassForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEditMode ? "Edit Class" : "Add Class" }}
            </h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- Body -->
        <div class="p-5 w-[30vw]">
          <div class="w-full text-left gap-3 flex flex-col space-y-1">
            <!-- Program Institute Filter -->
            <div v-if="user?.role === 'Admin'" class="w-full space-y-2">
              <label class="font-bold">Filter by Institute :</label>
              <select
                v-model="selectedInstitute"
                class="px-3 py-3.5 border w-full border-gray-600 rounded-md text-md text-gray-800"
              >
                <option value="">All Institutes</option>
                <option
                  v-for="inst in institutes"
                  :key="inst.institute_id"
                  :value="inst.institute_id"
                >
                  {{ inst.institute_name }}
                </option>
              </select>
            </div>

            <!-- Course Filters -->
            <div class="w-full flex gap-2">
              <div class="w-1/2 space-y-2">
                <label class="font-bold">Filter by Semester :</label>
                <select
                  v-model="selectedSemester"
                  class="px-3 py-3.5 border w-full border-gray-600 rounded-md text-md text-gray-800"
                >
                  <option value="">All</option>
                  <option v-for="sem in semesters" :key="sem" :value="sem">
                    {{ semesterLabel(sem) }}
                  </option>
                </select>
              </div>

              <div class="w-1/2 space-y-2">
                <label class="font-bold">Filter by Level :</label>
                <select
                  v-model="selectedLevel"
                  class="px-3 py-3.5 border w-full border-gray-600 rounded-md text-md text-gray-800"
                >
                  <option value="">All</option>
                  <option v-for="lvl in levels" :key="lvl" :value="lvl">
                    {{ lvl }}
                  </option>
                </select>
              </div>
            </div>
            <!-- Program -->
            <div class="flex flex-col space-y-2 w-full relative">
              <label class="font-bold">Program :</label>
              <input
                v-model="searchProgramQuery"
                type="text"
                placeholder="Search program..."
                class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
                @focus="showProgramDropdown = true"
              />
              <div
                v-if="showProgramDropdown && filteredPrograms.length"
                class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
                @mouseleave="showProgramDropdown = false"
              >
                <div
                  v-for="program in filteredPrograms"
                  :key="program.program_id"
                  class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                  @mousedown="selectProgram(program)"
                >
                  {{ program.program_name }} - {{ program.program_code }}
                </div>
              </div>
            </div>

            <!-- Course -->
            <div class="flex flex-col space-y-2 w-full relative mt-2">
              <label class="font-bold">Course :</label>
              <input
                v-model="searchCourseQuery"
                type="text"
                placeholder="Search course..."
                class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
                @focus="showCourseDropdown = true"
              />

              <div
                v-if="showCourseDropdown"
                class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-48 overflow-y-auto z-10"
                @mouseleave="showCourseDropdown = false"
              >
                <div
                  v-for="course in filteredCourses"
                  :key="course.course_id"
                  class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                  @mousedown="selectCourse(course)"
                >
                  <div class="font-semibold text-gray-800">
                    {{ course.course_code }} - {{ course.course_name }}
                  </div>
                  <div class="text-xs text-gray-500">
                    Level: {{ course.course_level }} •
                    {{ semesterLabel(course.course_semester) }}
                  </div>
                </div>

                <div
                  v-if="!filteredCourses.length"
                  class="px-3 py-2 text-gray-500 text-sm italic"
                >
                  No courses found
                </div>
              </div>
            </div>
            <!-- Set -->
            <div class="w-full space-y-2">
              <label class="font-bold">Set :</label>
              <div class="relative">
                <select
                  v-model="form.set"
                  required
                  class="w-full px-4 py-3.5 border border-gray-300 rounded-md text-sm text-gray-800 bg-white shadow-sm focus:ring-2 focus:ring-green-500 focus:border-green-500 transition ease-in-out duration-200 appearance-none"
                >
                  <option disabled value="">Select a set</option>
                  <option
                    v-for="set in sets"
                    :key="set"
                    :value="set"
                    class="py-2"
                  >
                    {{ set }}
                  </option>
                </select>
                <!-- Custom dropdown arrow -->
                <div
                  class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-gray-500"
                >
                  <svg
                    class="h-5 w-5"
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
            </div>
          </div>

          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <!-- Buttons -->
          <div class="tracking-wide flex justify-end gap-2 mt-4">
            <button
              class="bg-gray-200 p-2 px-3 rounded-lg text-gray-700 hover:bg-white border hover:border-gray-800 hover:text-gray-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
              @click="$emit('close')"
              type="button"
            >
              Cancel
            </button>
            <button
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
              type="submit"
            >
              {{ isEditMode ? "Save Changes" : "Submit" }}
            </button>
          </div>
        </div>
      </form>
    </div>

    <!-- Conflict Modal -->
    <div
      v-if="showConflictModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-60"
    >
      <div
        class="bg-white rounded-2xl shadow-2xl w-[420px] p-6 animate-slideUp border border-gray-100"
      >
        <!-- Icon + Title -->
        <div class="flex items-center gap-3 mb-4">
          <div class="bg-red-100 text-red-600 p-3 rounded-full">
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
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L4.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>
          <h2 class="text-lg font-semibold text-gray-900">Conflict Detected</h2>
        </div>

        <!-- Body -->
        <p
          class="text-sm text-gray-700 leading-relaxed mb-6 bg-red-50 rounded-lg p-4"
        >
          A class with the same <span class="font-semibold">Program</span>,
          <span class="font-semibold">Course</span>, and
          <span class="font-semibold">Set</span> already exists. Please choose
          another set or update the details.
        </p>

        <!-- Buttons -->
        <div class="flex justify-end gap-3">
          <button
            @click="showConflictModal = false"
            class="px-4 py-2 rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-100 transition"
          >
            Close
          </button>
          <button
            @click="showConflictModal = false"
            class="px-4 py-2 rounded-lg bg-red-600 text-white font-medium hover:bg-red-700 transition"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import axios from "axios";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "AssignClassFormModal",
  props: {
    assignClassData: {
      type: Object,
      default: null,
    },
  },
  components: { icon },

  data() {
    return {
      user: null,
      form: {
        program_id: "",
        course_id: "",
        set: "",
        year: "", // curriculum year
        semester: "", // course semester
      },
      searchProgramQuery: "",
      showProgramDropdown: false,
      searchCourseQuery: "",
      showCourseDropdown: false,
      sets: Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i)),

      // Filters
      selectedInstitute: "",
      selectedSemester: "",
      selectedLevel: "",
      // Conflict modal
      showConflictModal: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["programs", "courses"]),

    isEditMode() {
      return !!this.assignClassData;
    },

    institutes() {
      const seen = new Set();
      let allInstitutes = (this.programs || [])
        .map((p) => p.institute)
        .filter(Boolean);

      if (this.user?.role === "Admin") {
        return allInstitutes.filter((inst) => {
          if (seen.has(inst.institute_id)) return false;
          seen.add(inst.institute_id);
          return true;
        });
      }

      if (this.user?.role === "Program Chairperson") {
        return allInstitutes.filter(
          (inst) =>
            inst.institute_id === this.user.institute_id &&
            !seen.has(inst.institute_id) &&
            seen.add(inst.institute_id),
        );
      }

      return [];
    },

    semesters() {
      const set = new Set(this.courses?.map((c) => c.course_semester));
      return [...set].filter(Boolean);
    },

    levels() {
      const set = new Set(this.courses?.map((c) => c.course_level));
      return [...set].filter(Boolean);
    },

    filteredPrograms() {
      let list = this.programs || [];

      if (this.selectedInstitute) {
        list = list.filter((p) => p.institute_id === this.selectedInstitute);
      }

      if (this.searchProgramQuery) {
        list = list.filter((p) =>
          p.program_name
            .toLowerCase()
            .includes(this.searchProgramQuery.toLowerCase()),
        );
      }

      return list;
    },

    filteredCourses() {
      let list = this.courses || [];

      if (this.selectedInstitute) {
        list = list.filter(
          (c) => c.curriculum?.program?.institute_id === this.selectedInstitute,
        );
      }

      if (this.form.program_id) {
        list = list.filter(
          (c) => c.curriculum?.program_id === this.form.program_id,
        );
      }

      if (this.selectedSemester) {
        list = list.filter((c) => c.course_semester === this.selectedSemester);
      }

      if (this.selectedLevel) {
        list = list.filter((c) => c.course_level === this.selectedLevel);
      }

      if (this.searchCourseQuery) {
        const query = this.searchCourseQuery.toLowerCase();
        list = list.filter(
          (c) =>
            c.course_code.toLowerCase().includes(query) ||
            c.course_description.toLowerCase().includes(query),
        );
      }

      return list;
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchPrograms", "fetchCourses"]),

    semesterLabel(value) {
      const map = {
        1: "First Semester",
        2: "Second Semester",
        3: "Summer",
      };
      return map[value] || value;
    },

    selectProgram(program) {
      this.form.program_id = program.program_id;
      this.searchProgramQuery = program.program_name;
      this.showProgramDropdown = false;
      this.selectedInstitute = program.institute_id;
    },

    selectCourse(course) {
      this.form.course_id = course.course_id;
      this.searchCourseQuery = course.course_code;
      this.showCourseDropdown = false;
      this.selectedSemester = course.course_semester;
      this.selectedLevel = course.course_level;

      // Auto-populate year and semester
      this.form.year = course.curriculum?.curriculum_effective;
      this.form.semester = course.course_semester;
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

    async submitData() {
      const formEl = this.$refs.assignClassForm;
      if (!formEl.checkValidity()) {
        formEl.reportValidity();
        return;
      }

      try {
        const { data: existing } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/assign-class/get-assign-class",
        );

        const conflict = existing.find(
          (cls) =>
            cls.program_id === this.form.program_id &&
            cls.course_id === this.form.course_id &&
            cls.set === this.form.set &&
            (!this.isEditMode ||
              cls.assign_class_id !== this.assignClassData.assign_class_id),
        );

        if (conflict) {
          this.showConflictModal = true;
          return;
        }

        if (this.isEditMode) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/assign-class/update-id/${this.assignClassData.assign_class_id}`,
            this.form,
          );
          toast.success("Class updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/assign-class/add-assign-class",
            this.form,
          );
          toast.success("Class added successfully!");
        }

        const audio = new Audio(require("@/assets/add.mp3"));
        audio.play();

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        toast.error(
          this.isEditMode ? "Failed to update class" : "Failed to add class",
        );
      }
    },
  },

  async mounted() {
    await this.fetchUser(); // fetch user first
    await this.fetchPrograms();
    await this.fetchCourses();

    if (this.user?.role === "Program Chairperson") {
      this.selectedInstitute = this.user.institute_id; // auto-filter programs
    }

    if (this.isEditMode) {
      this.form = {
        program_id: this.assignClassData.program_id,
        course_id: this.assignClassData.course_id,
        set: this.assignClassData.set,
      };
      this.searchProgramQuery =
        this.assignClassData.program?.program_name || "";
      this.searchCourseQuery = this.assignClassData.course?.course_code || "";

      // For edit mode, keep previous selections
      this.selectedInstitute =
        this.user?.role === "Admin"
          ? this.assignClassData.program?.institute_id || ""
          : this.user.institute_id;
      this.selectedSemester =
        this.assignClassData.course?.course_semester || "";
      this.selectedLevel = this.assignClassData.course?.course_level || "";
    }
  },
};
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    transform: translateY(40px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.animate-slideUp {
  animation: fadeInUp 0.3s ease-out;
}
</style>
