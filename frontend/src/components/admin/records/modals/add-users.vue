<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="usersForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEditMode ? "Edit User" : "Add User" }}
            </h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- Form Content -->
        <div class="p-5 w-[30vw] space-y-6">
          <!-- Step 1: Personal Information -->
          <div v-if="currentStep === 1" class="space-y-3">
            <h2 class="text-md font-bold text-gray-800 border-b pb-1">
              Personal Information
            </h2>

            <div>
              <label class="font-bold">First Name:</label>
              <input
                v-model="form.first_name"
                type="text"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                placeholder="Enter first name"
              />
            </div>

            <div>
              <label class="font-bold">Last Name:</label>
              <input
                v-model="form.last_name"
                type="text"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                placeholder="Enter last name"
              />
            </div>

            <div>
              <label class="font-bold">Position:</label>
              <input
                v-model="form.position"
                type="text"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                placeholder="Enter position"
              />
            </div>

            <div>
              <label class="font-bold">Role:</label>
              <select
                v-model="form.role"
                required
                class="w-full border px-3 py-3.5 border-gray-600 rounded-md text-md text-gray-800"
              >
                <option disabled value="">Select role</option>
                <option value="Admin">Admin</option>
                <option value="Program Chairperson">Program Chairperson</option>
                <option value="Faculty">Faculty</option>
              </select>
            </div>

            <!-- Institute -->
            <div class="flex flex-col space-y-2 w-full relative">
              <label class="font-bold">Institute :</label>
              <input
                v-model="searchInstituteQuery"
                type="text"
                placeholder="Search institute..."
                class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
                @focus="showInstituteDropdown = true"
              />
              <div
                v-if="showInstituteDropdown && filteredInstitutes.length"
                class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
                @mouseleave="showInstituteDropdown = false"
              >
                <div
                  v-for="institute in filteredInstitutes"
                  :key="institute.institute_id"
                  class="px-3 py-3 hover:bg-gray-100 cursor-pointer"
                  @mousedown="selectinstitute(institute)"
                >
                  {{ institute.institute_name }}
                </div>
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
                  class="px-3 py-3 hover:bg-gray-100 cursor-pointer"
                  @mousedown="selectprogram(program)"
                >
                  {{ program.program_name }}
                </div>
              </div>
            </div>

            <!-- Next Button -->
            <div class="flex justify-end pt-2">
              <button
                class="bg-defaultGreen p-2 px-4 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
                type="button"
                @click="goToStep2"
              >
                Next
              </button>
            </div>
          </div>

          <!-- Step 2: User Credentials -->
          <div v-if="currentStep === 2" class="space-y-3">
            <h2 class="text-md font-bold text-gray-800 border-b pb-1">
              User Credentials
            </h2>

            <div>
              <label class="font-bold">Email:</label>
              <input
                v-model="form.email"
                type="email"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                placeholder="Enter email"
              />
            </div>

            <div v-if="!isEditMode">
              <label class="font-bold">Password:</label>
              <input
                v-model="form.password"
                type="password"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                placeholder="Enter password"
              />
            </div>

            <!-- Buttons -->
            <div class="tracking-wide flex justify-between gap-2 pt-4">
              <button
                class="bg-gray-400 p-2 px-4 rounded-lg text-white hover:bg-white border hover:border-gray-600 hover:text-gray-700 hover:shadow-md"
                type="button"
                @click="currentStep = 1"
              >
                Back
              </button>
              <button
                class="bg-defaultGreen p-2 px-4 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
                type="submit"
              >
                {{ isEditMode ? "Save Changes" : "Submit" }}
              </button>
            </div>
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
  name: "UsersModal",
  components: { icon },
  props: {
    userData: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      currentStep: 1,
      form: {
        id: null,
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        position: "",
        institute_id: "",
        program_id: "",
        role: "",
      },
      searchProgramQuery: "",
      showProgramDropdown: false,
      searchInstituteQuery: "",
      showInstituteDropdown: false,
    };
  },
  computed: {
    isEditMode() {
      return !!this.userData;
    },
    ...mapState(useFetchDataStore, ["programs", "institutes"]),
    filteredPrograms() {
      const query = this.searchProgramQuery?.toLowerCase() || "";
      return this.programs
        .filter(
          (program) =>
            program.program_name.toLowerCase().includes(query) &&
            program.institute_id === this.form.institute_id
        )
        .sort((a, b) => a.program_name.localeCompare(b.program_name));
    },
    filteredInstitutes() {
      const query = this.searchInstituteQuery?.toLowerCase() || "";
      return [...this.institutes]
        .filter((institute) =>
          institute.institute_name.toLowerCase().includes(query)
        )
        .sort((a, b) => a.institute_name.localeCompare(b.institute_name));
    },
  },
  methods: {
    ...mapActions(useFetchDataStore, ["fetchPrograms", "fetchInstitutes"]),
    selectprogram(program) {
      this.form.program_id = program.program_id;
      this.searchProgramQuery = program.program_name;
      this.showProgramDropdown = false;
    },
    selectinstitute(institute) {
      this.form.institute_id = institute.institute_id;
      this.searchInstituteQuery = institute.institute_name;
      this.showInstituteDropdown = false;
      this.searchProgramQuery = "";
      this.form.program_id = null;
    },
    goToStep2() {
      const {
        first_name,
        last_name,
        position,
        role,
        institute_id,
        program_id,
      } = this.form;
      if (
        !first_name ||
        !last_name ||
        !position ||
        !role ||
        !institute_id ||
        !program_id
      ) {
        toast.error("Please complete all personal information fields.");
        return;
      }
      this.currentStep = 2;
    },
    async submitData() {
      const form = this.$refs.usersForm;
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      try {
        if (this.isEditMode) {
          // UPDATE
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL + `/auth/update/${this.form.id}`,
            this.form,
            { withCredentials: true }
          );
          toast.success("User updated successfully!");
        } else {
          // ADD
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/auth/register",
            this.form,
            {
              withCredentials: true,
            }
          );
          toast.success("User registered successfully!");
          const audio = new Audio(require("@/assets/add.mp3"));
          audio.play();
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        toast.error(error?.response?.data?.message || "Failed to save user");
      }
    },
  },
  mounted() {
    this.fetchPrograms();
    this.fetchInstitutes();

    // Pre-fill form if editing
    if (this.isEditMode) {
      this.form = { ...this.form, ...this.userData };
      this.searchInstituteQuery = this.userData.institute_name || "";
      this.searchProgramQuery = this.userData.program_name || "";
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
