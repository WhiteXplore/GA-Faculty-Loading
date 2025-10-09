<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-md">Add Year/Section</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Program Card -->
      <div
        v-if="userProgram"
        class="border p-4 rounded-xl bg-white shadow-sm hover:shadow-md transition-all"
      >
        <div class="flex justify-between items-center">
          <div>
            <h2 class="text-lg font-bold text-gray-800">
              {{ userProgram.program_name }}
            </h2>
            <p class="text-sm text-gray-600">
              Code: {{ userProgram.program_code }}
            </p>
            <p class="text-sm text-gray-600" v-if="userProgram.institute">
              Institute: {{ userProgram.institute.institute_name }}
            </p>
          </div>
          <div>
            <button
              @click="openYearSectionModal"
              class="flex items-center gap-2 px-4 py-3 bg-defaultGreen text-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300"
            >
              <icon name="add-students" class="w-5 h-5" />
              <span class="font-medium">Add Year/Section</span>
            </button>
          </div>
        </div>

        <!-- Instructions -->
        <div class="mt-4 bg-blue-50 p-3 rounded-md">
          <h3 class="font-bold text-sm text-blue-800 mb-2">Instructions:</h3>
          <ul class="text-xs text-blue-700 space-y-1 list-disc list-inside">
            <li>Click "Add Year/Section" to configure class sections</li>
            <li>Select the school year for the sections</li>
            <li>Set the number of sections for each year level (1st-4th)</li>
            <li>Define the class size for each section</li>
            <li>Sections will be automatically named (A, B, C, etc.)</li>
          </ul>
        </div>
      </div>

      <!-- Loading State -->
      <div
        v-else-if="loading"
        class="border p-8 rounded-xl bg-white shadow-sm text-center"
      >
        <p class="text-gray-500">Loading program information...</p>
      </div>

      <!-- No Program Found -->
      <div
        v-else
        class="border p-8 rounded-xl bg-white shadow-sm text-center"
      >
        <icon name="question" class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-500">No program found for your account.</p>
        <p class="text-sm text-gray-400 mt-2">
          Please contact the administrator.
        </p>
      </div>
    </div>
  </div>

  <!-- Add Year/Section Modal -->
  <addYearSection
    v-if="showYearSectionModal && userProgram"
    :programData="userProgram"
    @close="closeYearSectionModal"
    @refresh="loadUserProgram"
  />
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import addYearSection from "./modals/add-year-section.vue";
import axios from "axios";

export default {
  name: "AddYearSectionPage",
  components: { icon, addYearSection },
  data() {
    return {
      showYearSectionModal: false,
      userProgram: null,
      user: null,
      loading: true,
    };
  },
  methods: {
    async fetchUser() {
      try {
        const response = await axios.get("http://localhost:8000/auth/me", {
          withCredentials: true,
        });
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
    async loadUserProgram() {
      try {
        this.loading = true;
        const response = await axios.get(
          "http://localhost:8000/programs/get-programs"
        );
        const programs = response.data;

        // Filter to get user's program
        if (this.user) {
          if (this.user.role === "Program Chairperson") {
            this.userProgram = programs.find(
              (p) =>
                String(p.institute?.institute_id) ===
                  String(this.user.institute_id) &&
                String(p.program_id) === String(this.user.program_id)
            );
          } else if (this.user.role === "Admin") {
            // For admin, could show all programs or let them select
            // For now, show a message that they should use Programs page
            toast.info(
              "Admins should use the Programs page to add year/sections"
            );
            this.$router.push("/programs");
          }
        }
      } catch (error) {
        console.error("Failed to load program:", error);
        toast.error("Failed to load program information");
      } finally {
        this.loading = false;
      }
    },
    openYearSectionModal() {
      this.showYearSectionModal = true;
    },
    closeYearSectionModal() {
      this.showYearSectionModal = false;
    },
  },
  async mounted() {
    await this.fetchUser();
    await this.loadUserProgram();
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>

