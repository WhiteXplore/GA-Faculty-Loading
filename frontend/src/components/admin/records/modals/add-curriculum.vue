<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="curriculumnForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ mode === "add" ? "Add Curriculum" : "Edit Curriculum" }}
            </h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- Form Body -->
        <div class="p-5 w-[28vw] space-y-3">
          <!-- Program -->
          <div class="flex flex-col space-y-2 w-full relative">
            <label class="font-bold">Program :</label>
            <input
              v-model="searchProgramQuery"
              type="text"
              placeholder="Search program..."
              class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
              @focus="showProgramDropdown = true"
              :disabled="mode === 'edit'"
            />
            <div
              v-if="showProgramDropdown && filteredPrograms.length"
              class="absolute top-[60px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
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
          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="curriculum_name" class="font-bold"
              >Curriculum Name:</label
            >
            <input
              v-model="form.curriculum_name"
              type="text"
              id="curriculum_name"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="Enter curriculum"
            />
          </div>

          <!-- Effective Year -->
          <div class="flex gap-3">
            <div class="w-full space-y-2 text-left flex flex-col">
              <label for="curriculum_effective" class="font-bold"
                >Effective Year:</label
              >
              <input
                v-model="form.curriculum_effective"
                type="text"
                id="curriculum_effective"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                placeholder="Enter effective year"
              />
            </div>
          </div>

          <!-- Divider -->
          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <!-- Buttons -->
          <div class="tracking-wide flex justify-end gap-2 mt-4">
            <button
              class="bg-red-600 p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
              @click="$emit('close')"
              type="button"
            >
              Cancel
            </button>
            <button
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
              type="submit"
            >
              {{ mode === "add" ? "Submit" : "Update" }}
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
  name: "AddEditCurriculumPage",
  components: { icon },
  props: {
    mode: { type: String, default: "add" }, // 'add' or 'edit'
    curriculumData: { type: Object, default: null }, // when editing
  },
  data() {
    return {
      form: {
        program_id: "",
        curriculum_name: "",
        curriculum_effective: "",
      },
      searchProgramQuery: "",
      showProgramDropdown: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["programs"]),
    filteredPrograms() {
      if (!this.searchProgramQuery) return this.programs;
      const query = this.searchProgramQuery.toLowerCase();
      return this.programs.filter((program) =>
        program.program_name.toLowerCase().includes(query)
      );
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
        if (this.mode === "add") {
          await axios.post(
            "http://localhost:8000/curriculums/add-curriculums",
            this.form
          );
          toast.success("Curriculum added successfully!");
          new Audio(require("@/assets/add.mp3")).play();
        } else {
          await axios.patch(
            `http://localhost:8000/curriculums/update-curriculum/${this.curriculumData.curriculum_id}`,
            this.form
          );
          toast.success("Curriculum updated successfully!");
          new Audio(require("@/assets/add.mp3")).play();
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        toast.error("Failed to save curriculum");
      }
    },
  },
  mounted() {
    this.fetchPrograms();

    if (this.mode === "edit" && this.curriculumData) {
      this.form = {
        program_id: this.curriculumData.program_id,
        curriculum_name: this.curriculumData.curriculum_name,
        curriculum_effective: this.curriculumData.curriculum_effective,
      };
      // set program name in input
      const selectedProgram = this.programs.find(
        (p) => p.program_id === this.curriculumData.program_id
      );
      if (selectedProgram) {
        this.searchProgramQuery = selectedProgram.program_name;
      }
    }
  },
};
</script>
