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
            <h1
              class="font-bold tracking-wide text-lg"
              v-if="user.role === 'Admin'"
            >
              {{ isEditMode ? "Edit User" : "Add User" }}
            </h1>
            <h1
              class="font-bold tracking-wide text-lg"
              v-else-if="user.role === 'Faculty'"
            >
              {{ isEditMode ? "Edit My Details" : "Add My Details" }}
            </h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- Form Content -->
        <div class="px-5 py-3 w-[30vw] space-y-6">
          <!-- Step 1: Personal Information -->
          <div v-if="currentStep === 1" class="space-y-3">
            <h2 class="text-lg font-bold text-gray-800 border-b pb-1">
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
          <div v-if="currentStep === 2" class="space-y-3">
            <h2 class="text-lg font-bold text-gray-800 border-b pb-1">
              Professional / employment Information
            </h2>

            <div>
              <label class="font-bold">Role:</label>
              <select
                v-model="form.role"
                required
                class="w-full border px-2 py-3.5 border-gray-600 rounded-md text-md text-gray-800"
              >
                <option disabled value="">Select role</option>
                <option value="Admin">Admin</option>
                <option value="Program Chairperson">Program Chairperson</option>
                <option value="Faculty">Faculty</option>
              </select>
            </div>

            <div>
              <label class="font-bold">Designation:</label>
              <input
                v-model="form.designation"
                type="text"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                placeholder="Enter designation"
              />
            </div>
            <div>
              <label class="font-bold">Type of employment:</label>
              <select
                v-model="form.employment_type"
                required
                class="w-full border px-2 py-3.5 border-gray-600 rounded-md text-md text-gray-800"
              >
                <option disabled value="">Select type</option>
                <option value="full time">Full Time</option>
                <option value="part time">Part Time</option>
              </select>
            </div>

            <div>
              <label class="font-bold">Unit Load:</label>
              <input
                v-model="form.unit_load"
                type="number"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                placeholder="Enter unit load"
              />
            </div>

            <!-- School Year -->
            <div class="flex flex-col space-y-2 w-full relative">
              <label class="font-bold">School Year :</label>
              <input
                v-model="searchSchoolYearQuery"
                type="text"
                placeholder="Search school year..."
                class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
                @focus="showSchoolYearDropdown = true"
              />
              <div
                v-if="showSchoolYearDropdown && filteredInstitutes.length"
                class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
                @mouseleave="showSchoolYearDropdown = false"
              >
                <div
                  v-for="schoolyear in filteredSchoolYears"
                  :key="schoolyear.school_year_id"
                  class="px-3 py-3 hover:bg-gray-100 cursor-pointer"
                  @mousedown="selectSchoolYear(schoolyear)"
                >
                  {{ schoolyear.school_year_name }}
                </div>
              </div>
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
            <div class="flex justify-between pt-2">
              <button
                class="bg-gray-400 p-2 px-4 rounded-lg text-white hover:bg-white border hover:border-gray-600 hover:text-gray-700 hover:shadow-md"
                type="button"
                @click="currentStep = 1"
              >
                Back
              </button>
              <button
                class="bg-defaultGreen p-2 px-4 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
                type="button"
                @click="goToStep3"
              >
                Next
              </button>
            </div>
          </div>
          <!-- Step 2: User Credentials -->
          <div v-if="currentStep === 3" class="space-y-3">
            <h2 class="text-lg font-bold text-gray-800 border-b pb-1">
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

            <!-- ✅ Always show password field -->
            <div>
              <label class="font-bold">
                {{ isEditMode ? "New Password (optional):" : "Password:" }}
              </label>
              <input
                v-model="form.password"
                type="password"
                :required="!isEditMode"
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                :placeholder="
                  isEditMode
                    ? 'Leave blank to keep current password'
                    : 'Enter password'
                "
              />
            </div>

            <!-- Buttons -->
            <div class="tracking-wide flex justify-between gap-2 pt-4">
              <button
                class="bg-gray-400 p-2 px-4 rounded-lg text-white hover:bg-white border hover:border-gray-600 hover:text-gray-700 hover:shadow-md"
                type="button"
                @click="currentStep = 2"
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
      user: {},
      form: {
        id: null,
        email: "",
        password: "",
        first_name: "",
        last_name: "",

        school_year_id: "",
        institute_id: "",
        program_id: "",
        role: "",

        employment_type: "",
        unit_load: "",
        designation: "",
      },
      searchProgramQuery: "",
      showProgramDropdown: false,
      searchInstituteQuery: "",
      showInstituteDropdown: false,
      searchSchoolYearQuery: "",
      showSchoolYearDropdown: false,
    };
  },
  computed: {
    isEditMode() {
      return !!this.userData;
    },
    ...mapState(useFetchDataStore, ["programs", "institutes", "activeYears"]),
    filteredPrograms() {
      const query = this.searchProgramQuery?.toLowerCase() || "";
      return this.programs
        .filter(
          (program) =>
            program.program_name.toLowerCase().includes(query) &&
            program.institute_id === this.form.institute_id,
        )
        .sort((a, b) => a.program_name.localeCompare(b.program_name));
    },
    filteredInstitutes() {
      const query = this.searchInstituteQuery?.toLowerCase() || "";
      return [...this.institutes]
        .filter((institute) =>
          institute.institute_name.toLowerCase().includes(query),
        )
        .sort((a, b) => a.institute_name.localeCompare(b.institute_name));
    },

    filteredSchoolYears() {
      const query = this.searchSchoolYearQuery?.toLowerCase() || "";
      return [...this.activeYears]
        .filter((schoolyear) =>
          schoolyear.school_year_name.toLowerCase().includes(query),
        )
        .sort((a, b) => a.school_year_name.localeCompare(b.school_year_name));
    },
  },
  methods: {
    ...mapActions(useFetchDataStore, [
      "fetchPrograms",
      "fetchInstitutes",
      "fetchActiveYears",
    ]),
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
    selectSchoolYear(schoolyear) {
      this.form.school_year_id = schoolyear.school_year_id; // Save the ID
      this.searchSchoolYearQuery = schoolyear.school_year_name; // Show name in input
      this.showSchoolYearDropdown = false;
    },
    goToStep2() {
      const { first_name, last_name } = this.form;
      if (!first_name || !last_name) {
        toast.error("Please complete all personal information fields.");
        return;
      }
      this.currentStep = 2;
    },
    goToStep3() {
      const { role, institute_id, program_id, employment_type, unit_load } =
        this.form;
      if (
        !role ||
        !institute_id ||
        !program_id ||
        !employment_type ||
        !unit_load
      ) {
        toast.error("Please complete all personal information fields.");
        return;
      }
      this.currentStep = 3;
    },

    async submitData() {
      const form = this.$refs.usersForm;

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      try {
        if (this.isEditMode) {
          const userId = this.form.id || this.form.sub;

          // ✅ If password is empty, remove it before sending
          const updateData = { ...this.form };
          if (!updateData.password) {
            delete updateData.password;
          }

          await axios.patch(
            process.env.VUE_APP_API_BASE_URL + `/auth/update/${userId}`,
            updateData,
            { withCredentials: true },
          );
          toast.success("User updated successfully!");
          this.$emit("updated");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/auth/register",
            this.form,
            {
              withCredentials: true,
            },
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
          this.user.expertise = this.user.expertise || [];
          this.user.other_expertise = this.user.other_expertise || [];
          console.log("Authenticated User:", this.user);
        } else {
          this.$router.push("/");
          location.reload();
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },
  },
  mounted() {
    this.fetchUser();
    this.fetchPrograms();
    this.fetchInstitutes();
    this.fetchActiveYears();
    if (this.isEditMode) {
      // Start fresh so institute_id and program_id don't get overwritten
      this.form = {
        id: this.userData.id || this.userData.sub || null,
        email: this.userData.email || "",
        password: "",
        first_name: this.userData.first_name || "",
        last_name: this.userData.last_name || "",
        role: this.userData.role || "",
        employment_type: this.userData.employment_type || "",
        unit_load: this.userData.unit_load || "",
        designation: this.userData.designation || "",
        institute_id: "",
        program_id: "",
      };

      // ✅ Handle institute properly
      if (this.userData.institute) {
        this.form.institute_id = this.userData.institute.institute_id;
        this.searchInstituteQuery = this.userData.institute.institute_name;
      } else if (this.userData.institute_id) {
        this.form.institute_id = this.userData.institute_id;
        const institute = this.institutes.find(
          (inst) => inst.institute_id === this.userData.institute_id,
        );
        if (institute) this.searchInstituteQuery = institute.institute_name;
      }

      // ✅ Handle program properly
      if (this.userData.program) {
        this.form.program_id = this.userData.program.program_id;
        this.searchProgramQuery = this.userData.program.program_name;
      } else if (this.userData.program_id) {
        this.form.program_id = this.userData.program_id;
        const program = this.programs.find(
          (prog) => prog.program_id === this.userData.program_id,
        );
        if (program) this.searchProgramQuery = program.program_name;
      }

      // Handle school year properly
      if (this.isEditMode && this.userData.school_year) {
        this.form.school_year_id = this.userData.school_year.school_year_id;
        this.searchSchoolYearQuery = this.userData.school_year.school_year_name;
      } else if (this.isEditMode && this.userData.school_year_id) {
        this.form.school_year_id = this.userData.school_year_id;
        const year = this.activeYears.find(
          (y) => y.school_year_id === this.userData.school_year_id,
        );
        if (year) this.searchSchoolYearQuery = year.school_year_name;
      }
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
