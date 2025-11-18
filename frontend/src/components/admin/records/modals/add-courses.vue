<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="coursesForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit " : "Add " }} Course
            </h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- Body -->
        <div class="p-5 w-[35vw] space-y-5">
          <!-- Curriculum -->
          <div class="flex flex-col space-y-2 w-full relative">
            <label class="font-bold">Curriculum :</label>
            <input
              v-model="searchCurriculumQuery"
              type="text"
              placeholder="Search curriculum..."
              class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
              @focus="showCurriculumDropdown = true"
            />
            <div
              v-if="showCurriculumDropdown && filteredCurriculum.length"
              class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
              @mouseleave="showCurriculumDropdown = false"
            >
              <div
                v-for="curriculum in filteredCurriculum"
                :key="curriculum.curriculum_id"
                class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                @mousedown="selectcurriculum(curriculum)"
              >
                {{ curriculum.curriculum_name }}
              </div>
            </div>
          </div>

          <!-- Course Code -->
          <div class="w-full space-y-2">
            <label for="course_code" class="font-bold">Course Code:</label>
            <input
              v-model="form.course_code"
              type="text"
              id="course_code"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="Enter course code"
            />
          </div>

          <!-- Description -->
          <div class="w-full space-y-2">
            <label for="course_description" class="font-bold"
              >Course Description:</label
            >
            <textarea
              v-model="form.course_description"
              id="course_description"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="Enter course description"
            />
          </div>

          <!-- Year + Semester -->
          <div class="w-full flex gap-3">
            <div class="w-full space-y-2">
              <label class="font-bold">Year Level:</label>
              <select
                v-model="form.course_level"
                required
                class="w-full border px-2 py-3 border-gray-600 rounded-md"
              >
                <option disabled value="">Select Level</option>
                <option value="1">First</option>
                <option value="2">Second</option>
                <option value="3">Third</option>
                <option value="4">Fourth</option>
              </select>
            </div>
            <div class="w-full space-y-2">
              <label class="font-bold">Semester:</label>
              <select
                v-model="form.course_semester"
                required
                class="w-full border px-2 py-3 border-gray-600 rounded-md"
              >
                <option disabled value="">Select Semester</option>
                <option value="1">First</option>
                <option value="2">Second</option>
              </select>
            </div>
          </div>

          <!-- Lec/Lab -->
          <div class="w-full flex gap-3">
            <div class="w-full space-y-2">
              <label class="font-bold">Lecture (Hours):</label>
              <input
                v-model="form.course_lec"
                type="number"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md"
              />
            </div>
            <div class="w-full space-y-2">
              <label class="font-bold">Laboratory (Hours):</label>
              <input
                v-model="form.course_lab"
                type="number"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md"
              />
            </div>
          </div>

          <div class="flex flex-col space-y-2 relative">
            <label class="font-bold">Requisites :</label>

            <!-- Show Add button if input is hidden -->
            <button
              v-if="!showRequisiteInput"
              type="button"
              class="bg-defaultGreen text-white px-3 py-3 tracking-wider rounded-md text-sm hover:bg-green-700"
              @click="showRequisiteInput = true"
            >
              Add Requisite
            </button>

            <!-- Show input when button clicked -->
            <div v-if="showRequisiteInput" class="flex flex-col gap-2">
              <div class="flex gap-2">
                <input
                  :value="form.course_requisite.join(', ')"
                  @input="searchRequisiteQuery = $event.target.value"
                  @focus="showRequisiteDropdown = true"
                  type="text"
                  placeholder="Search course prerequisite..."
                  class="px-3 py-3 border w-full border-gray-600 rounded-md"
                />
                <!-- Cancel button -->
                <button
                  type="button"
                  @click="cancelRequisites"
                  class="text-red-600 px-2 py-1 border border-red-600 rounded-md hover:bg-red-600 hover:text-white"
                >
                  Cancel
                </button>
              </div>

              <!-- Dropdown -->
              <div
                v-if="showRequisiteDropdown && filteredCourse.length"
                class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
                @mouseleave="showRequisiteDropdown = false"
              >
                <div
                  v-for="course in filteredCourse"
                  :key="course.course_id"
                  class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                  @mousedown="selectcourse(course)"
                >
                  {{ course.course_code }} - {{ course.course_description }}
                </div>
              </div>
            </div>

            <!-- Display selected requisites -->
            <div class="flex flex-wrap gap-2 mt-2">
              <span
                v-for="code in form.course_requisite"
                :key="code"
                class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs cursor-pointer"
                @click="removeRequisite(code)"
              >
                {{ code }} ✕
              </span>
            </div>
          </div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2 mt-4">
            <button
              class="bg-red-600 p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-red-800 hover:text-red-800"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800"
              type="submit"
            >
              {{ isEdit ? "Update" : "Submit" }}
            </button>
          </div>
        </div>
      </form>
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
  name: "CourseFormModal",
  components: { icon },
  props: {
    courseData: { type: Object, default: null },
  },
  data() {
    return {
      form: {
        curriculum_id: "",
        course_code: "",
        course_description: "",
        course_semester: "",
        course_lab: "",
        course_lec: "",
        course_level: "",
        course_requisite: [],
      },
      showRequisiteInput: false,
      searchCurriculumQuery: "",
      showCurriculumDropdown: false,
      searchRequisiteQuery: "",
      showRequisiteDropdown: false,
      searchTagQuery: "",
      showTagDropdown: false,
      availableTags: [
        "Computing",
        "IT Fundamentals",
        "Programming",
        "Software Development",
        "Filipino",
        "Communication",
        "Science",
        "Technology",
        "History",
        "Culture",
        "Psychology",
        "Personal Development",
        "Physical Education",
        "Health",
        "Writing Skills",
      ],
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["curriculums", "courses"]),
    isEdit() {
      return !!this.courseData;
    },
    filteredCurriculum() {
      if (!this.searchCurriculumQuery) return this.curriculums;
      const q = this.searchCurriculumQuery.toLowerCase();
      return this.curriculums.filter((c) =>
        c.curriculum_name?.toLowerCase().includes(q)
      );
    },
    filteredCourse() {
      const q = this.searchRequisiteQuery.toLowerCase();
      return this.courses.filter(
        (course) =>
          (course.course_code?.toLowerCase().includes(q) ||
            course.course_description?.toLowerCase().includes(q)) &&
          this.form.curriculum_id === course.curriculum_id &&
          !this.form.course_requisite.includes(course.course_code) // skip selected
      );
    },
  },
  methods: {
    ...mapActions(useFetchDataStore, ["fetchCurriculums", "fetchCourses"]),
    cancelRequisites() {
      this.showRequisiteInput = false;
      this.form.course_requisite = []; // clear all selected
      this.searchRequisiteQuery = ""; // clear input
    },
    selectcurriculum(curr) {
      this.form.curriculum_id = curr.curriculum_id;
      this.searchCurriculumQuery = curr.curriculum_name;
      this.showCurriculumDropdown = false;
    },
    selectcourse(course) {
      if (!this.form.course_requisite.includes(course.course_code)) {
        this.form.course_requisite.push(course.course_code);
      }
      this.showRequisiteDropdown = false;
    },
    removeRequisite(code) {
      this.form.course_requisite = this.form.course_requisite.filter(
        (c) => c !== code
      );
    },

    async submitData() {
      try {
        const payload = {
          ...this.form,
          course_requisite: this.form.course_requisite.join(","),
        };

        if (this.isEdit) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/courses/update-course/${this.courseData.course_id}`,
            payload
          );
          toast.success("Course updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/courses/add-courses",
            payload
          );
          toast.success("Course added successfully!");
        }

        this.$emit("refresh");
        this.$emit("close");

        // Play audio, but handle errors separately
        try {
          const audio = new Audio(
            require(`@/assets/${this.isEdit ? "update.mp3" : "add.mp3"}`)
          );
          await audio.play();
        } catch (audioErr) {
          console.warn("Audio failed to play:", audioErr);
        }
      } catch (err) {
        console.error(err);
        toast.error(
          this.isEdit ? "Failed to update course." : "Failed to add course."
        );
      }
    },
  },
  mounted() {
    this.fetchCurriculums();
    this.fetchCourses();

    // if editing, fill the form
    if (this.isEdit) {
      this.form = {
        ...this.courseData,
        course_requisite: this.courseData.course_requisite
          ? this.courseData.course_requisite.split(",")
          : [],
      };
      this.searchCurriculumQuery =
        this.courseData.curriculum?.curriculum_name || "";
    }
  },
};
</script>
