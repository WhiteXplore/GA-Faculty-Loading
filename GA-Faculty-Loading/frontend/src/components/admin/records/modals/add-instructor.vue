<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="instructorForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">Add Instructor</h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- Body -->
        <div class="w-full h-auto p-5">
          <!-- Personal Information -->
          <div v-if="currentStep === 1">
            <h1 class="text-left text-lg font-bold">Personal Information</h1>
            <div class="w-[25vw] text-left gap-3 flex flex-col mt-2">
              <div class="w-full space-y-2">
                <label for="instructor_fname">First Name:</label>
                <input
                  v-model="form.instructor_fname"
                  type="text"
                  id="instructor_fname"
                  required
                  class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                  placeholder="Enter first name"
                />
              </div>
              <div class="w-full space-y-2">
                <label for="instructor_mname">Middle Name:</label>
                <input
                  v-model="form.instructor_mname"
                  type="text"
                  id="instructor_mname"
                  required
                  class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                  placeholder="Enter middle name"
                />
              </div>
              <div class="w-full space-y-2">
                <label for="instructor_lname">Last Name:</label>
                <input
                  v-model="form.instructor_lname"
                  type="text"
                  id="instructor_lname"
                  required
                  class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                  placeholder="Enter last name"
                />
              </div>
              <div class="w-full space-y-2">
                <label for="instructor_gender">Gender:</label>
                <select
                  v-model="form.instructor_gender"
                  id="instructor_gender"
                  required
                  class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
                >
                  <option value="" disabled>Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Education Information -->
          <div v-if="currentStep === 2">
            <h1 class="text-left text-lg font-bold">Education Information</h1>
            <div class="w-[25vw] text-left gap-3 flex flex-col mt-2">
              <div class="w-full space-y-2">
                <label for="institute_id">Institute:</label>
                <select
                  v-model="form.institute_id"
                  id="institute_id"
                  class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
                >
                  <option value="" disabled>Select Institute</option>
                  <option
                    v-for="institute in institutes"
                    :key="institute.institute_id"
                    :value="institute.institute_id"
                  >
                    {{ institute.institute_name }}
                  </option>
                </select>
              </div>

              <div class="w-full space-y-2">
                <label for="program_id">Program:</label>
                <select
                  v-model="form.program_id"
                  id="program_id"
                  class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
                >
                  <option value="" disabled>Select Program</option>
                  <option
                    v-for="program in filteredPrograms"
                    :key="program.program_id"
                    :value="program.program_id"
                  >
                    {{ program.program_name }}
                  </option>
                </select>
              </div>
              <!-- Instructor Expertise Multi-Select -->
              <div class="flex flex-col space-y-2 w-[25vw] relative">
                <label>Instructor Expertise :</label>
                <input
                  :value="form.instructor_expertise.join(', ')"
                  @input="searchExpertiseQuery = $event.target.value"
                  @focus="showExpertiseDropdown = true"
                  type="text"
                  placeholder="Select expertise..."
                  class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
                />

                <div
                  v-if="showExpertiseDropdown && filteredExpertise.length"
                  class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
                  @mouseleave="showExpertiseDropdown = false"
                >
                  <div
                    v-for="expertise in filteredExpertise"
                    :key="expertise"
                    class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                    @mousedown="selectExpertise(expertise)"
                  >
                    {{ expertise }}
                  </div>
                </div>

                <!-- Display selected expertise -->
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="expertise in form.instructor_expertise"
                    :key="expertise"
                    class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs cursor-pointer"
                    @click="removeExpertise(expertise)"
                  >
                    {{ expertise }} ✕
                  </span>
                </div>
              </div>

              <div class="w-full space-y-2">
                <label for="instructor_jobtype">Job Type:</label>
                <select
                  v-model="form.instructor_jobtype"
                  id="instructor_jobtype"
                  required
                  class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
                >
                  <option value="" disabled>Select Job Type:</option>
                  <option value="Regular">Regular</option>
                  <option value="Weekend">Weekend</option>
                  <option value="Overload">Overload</option>
                  <option value="Regular-Overload">Regular/Overload</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Navigation Buttons -->
          <div class="tracking-wide flex justify-between mt-4">
            <button
              v-if="currentStep > 1"
              type="button"
              class="bg-gray-600 p-2 px-3 rounded-md text-white hover:bg-gray-800"
              @click="prevStep"
            >
              Back
            </button>
            <button
              v-if="currentStep < 2"
              type="button"
              class="bg-defaultGreen p-2 px-3 rounded-md text-white hover:"
              @click="nextStep"
            >
              Next
            </button>
          </div>

          <!-- Divider -->
          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <!-- Submit/Cancel -->
          <div class="tracking-wide flex justify-end gap-2 mt-4">
            <button
              type="button"
              class="bg-red-600 p-2 px-3 rounded-md text-white hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="bg-defaultGreen p-2 px-3 rounded-md text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
            >
              Submit
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
  name: "AddFacultyLoad",
  components: { icon },
  data() {
    return {
      currentStep: 1,
      form: {
        instructor_fname: "",
        instructor_mname: "",
        instructor_lname: "",
        instructor_gender: "",
        instructor_jobtype: "",
        program_id: "",
        institute_id: "",
        instructor_expertise: [],
      },
      searchExpertiseQuery: "",
      showExpertiseDropdown: false,
      availableExpertise: [
        "Programming",
        "Data Science",
        "Mathematics",
        "Physics",
        "Chemistry",
        "Biology",
        "Communication",
        "History",
        "IT Fundamentals",
        "Software Development",
        "Psychology",
        "Physical Education",
        "Health",
        "Writing Skills",
        "Technology",
        "Culture",
      ],
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["programs", "institutes"]),
    filteredPrograms() {
      if (!this.form.institute_id) return [];
      return this.programs.filter(
        (p) => p.institute_id === this.form.institute_id
      );
    },
    filteredExpertise() {
      const query = this.searchExpertiseQuery.toLowerCase();
      return this.availableExpertise.filter(
        (exp) =>
          exp.toLowerCase().includes(query) &&
          !this.form.instructor_expertise.includes(exp)
      );
    },
  },
  watch: {
    "form.institute_id"() {
      this.form.program_id = "";
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchPrograms", "fetchInstitutes"]),
    nextStep() {
      this.currentStep++;
    },
    prevStep() {
      this.currentStep--;
    },
    selectExpertise(expertise) {
      if (!this.form.instructor_expertise.includes(expertise)) {
        this.form.instructor_expertise.push(expertise);
      }
      this.searchExpertiseQuery = "";
      this.showExpertiseDropdown = false;
    },
    removeExpertise(expertise) {
      this.form.instructor_expertise = this.form.instructor_expertise.filter(
        (e) => e !== expertise
      );
    },
    async submitData() {
      console.log("submit triggered", this.form);

      const form = this.$refs.instructorForm;
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      try {
        const response = await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/instructors/add-instructor",
          this.form
        );
        console.log(response);
        toast.success("Instructor added successfully!");

        const audio = new Audio(require("@/assets/add.mp3"));
        audio.play();

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error("Error submitting form:", error.response?.data || error);
        toast.error("Failed to add instructor.");
      }
    },
  },
  mounted() {
    this.fetchPrograms();
    this.fetchInstitutes();
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
