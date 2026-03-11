<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        ref="curriculumnForm"
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon name="add-students" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit Curriculum" : "Add Curriculum" }}
            </h1>
          </div>
          <icon
            name="circle-close3"
            class="cursor-pointer"
            @click="$emit('close')"
          />
        </div>

        <!-- Body -->
        <div class="p-5 w-[28vw] space-y-4">
          <!-- Program -->
          <div class="flex flex-col space-y-2 relative">
            <label class="font-bold">Program:</label>
            <input
              v-model="searchProgramQuery"
              type="text"
              placeholder="Search program..."
              class="px-3 py-3 border border-gray-600 rounded-md"
              @focus="showProgramDropdown = true"
              :disabled="isEdit"
              required
            />

            <div
              v-if="showProgramDropdown && filteredPrograms.length && !isEdit"
              class="absolute top-[60px] w-full bg-white border rounded-md max-h-40 overflow-y-auto z-10"
              @mouseleave="showProgramDropdown = false"
            >
              <div
                v-for="program in filteredPrograms"
                :key="program.program_id"
                class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                @mousedown="selectProgram(program)"
              >
                {{ program.program_name }}
              </div>
            </div>
          </div>

          <!-- Curriculum Name -->
          <div class="flex flex-col space-y-2">
            <label class="font-bold">Curriculum Name:</label>
            <input
              :value="formattedCurriculumName"
              type="text"
              disabled
              class="w-full border px-3 py-3 border-gray-600 rounded-md bg-gray-100 cursor-not-allowed"
            />
          </div>

          <!-- Effective Year -->
          <div class="flex flex-col space-y-2">
            <label class="font-bold">Effective Year:</label>
            <input
              v-model="form.curriculum_end_year"
              type="number"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md"
              placeholder="e.g. 2025"
            />
          </div>

          <!-- Divider -->
          <div class="h-[1px] bg-gray-200 my-4"></div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2">
            <button
              type="button"
              class="bg-gray-200 p-2 px-3 rounded-lg text-gray-700 hover:bg-white border hover:border-gray-800 hover:text-gray-800 hover:shadow-md transition-all duration-300 hover:scale-105"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transition-all duration-300 hover:scale-105"
            >
              {{ isEdit ? "Save Changes" : "Submit" }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "AddEditCurriculumPage",
  components: { icon },

  props: {
    curriculumData: {
      type: Object,
      default: null,
    },
  },

  data() {
    return {
      form: {
        program_id: "",
        curriculum_start_year: "",
        curriculum_end_year: "",
      },
      searchProgramQuery: "",
      showProgramDropdown: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["programs"]),

    isEdit() {
      return !!this.curriculumData;
    },

    filteredPrograms() {
      if (!this.searchProgramQuery) return this.programs;
      return this.programs.filter((p) =>
        p.program_name
          .toLowerCase()
          .includes(this.searchProgramQuery.toLowerCase()),
      );
    },

    formattedCurriculumName() {
      if (!this.form.program_id || !this.form.curriculum_end_year) return "";
      const program = this.programs.find(
        (p) => p.program_id === this.form.program_id,
      );
      return program
        ? `${this.form.curriculum_end_year} - ${program.program_name}`
        : "";
    },
  },

  watch: {
    curriculumData: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.form.program_id = newVal.program_id;
          this.form.curriculum_start_year = newVal.curriculum_start_year;
          this.form.curriculum_end_year = newVal.curriculum_end_year;

          const program = this.programs.find(
            (p) => p.program_id === newVal.program_id,
          );
          if (program) {
            this.searchProgramQuery = program.program_name;
          }
        }
      },
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchPrograms"]),

    selectProgram(program) {
      this.form.program_id = program.program_id;
      this.searchProgramQuery = program.program_name;
      this.showProgramDropdown = false;
    },

    async submitData() {
      const formEl = this.$refs.curriculumnForm;
      if (!formEl.checkValidity()) {
        formEl.reportValidity();
        return;
      }

      try {
        if (this.isEdit) {
          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/curriculums/update-curriculum/${this.curriculumData.curriculum_id}`,
            this.form,
          );
          toast.success("Curriculum updated successfully!");
        } else {
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/curriculums/add-curriculums`,
            this.form,
          );
          toast.success("Curriculum added successfully!");
        }

        new Audio(require("@/assets/add.mp3")).play();
        this.$emit("refresh");
        this.$emit("close");
      } catch (err) {
        toast.error("Failed to save curriculum");
      }
    },
  },

  mounted() {
    this.fetchPrograms();
  },
};
</script>
