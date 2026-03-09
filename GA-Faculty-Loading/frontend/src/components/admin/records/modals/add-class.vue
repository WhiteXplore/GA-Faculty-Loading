<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="classForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit " : "Add " }} Class
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
              v-if="showSchoolYearDropdown && filteredSchoolYears.length"
              class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
              @mouseleave="showSchoolYearDropdown = false"
            >
              <div
                v-for="sy in filteredSchoolYears"
                :key="sy.school_year_id"
                class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                @mousedown="selectSchoolYear(sy)"
              >
                {{ sy.school_year_name }}
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
                v-for="prog in filteredPrograms"
                :key="prog.program_id"
                class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                @mousedown="selectProgram(prog)"
              >
                {{ prog.program_name }}
              </div>
            </div>
          </div>

          <!-- Set Name -->
          <div class="w-full space-y-2">
            <label for="set_name" class="font-bold">Set Name:</label>
            <input
              v-model="form.set_name"
              type="text"
              id="set_name"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="e.g., 1st Year - A"
            />
            <div class="text-xs text-gray-500 mt-1">
              Examples: 1st Year - A, 2nd Year - B, 3rd Year - C
            </div>
          </div>

          <!-- Class Size -->
          <div class="w-full space-y-2">
            <label for="class_size" class="font-bold">Class Size:</label>
            <input
              v-model.number="form.class_size"
              type="number"
              id="class_size"
              required
              min="1"
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="Enter class size (e.g., 30)"
            />
          </div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2 mt-4">
            <button
              type="button"
              class="bg-gray-100 text-gray-600 p-2 px-3 rounded-lg hover:bg-white border hover:border-gray-800 hover:text-gray-800"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800"
              type="submit"
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
import { toast } from "vue3-toastify";
import axios from "axios";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "ClassFormModal",
  components: { icon },
  props: {
    classData: { type: Object, default: null },
  },
  data() {
    return {
      form: {
        school_year_id: "",
        program_id: "",
        set_name: "",
        class_size: "",
      },
      searchSchoolYearQuery: "",
      showSchoolYearDropdown: false,
      searchProgramQuery: "",
      showProgramDropdown: false,
      schoolYears: [],
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["programs"]),
    isEdit() {
      return !!this.classData;
    },
    filteredSchoolYears() {
      if (!this.searchSchoolYearQuery) return this.schoolYears;
      const q = this.searchSchoolYearQuery.toLowerCase();
      return this.schoolYears.filter((sy) =>
        sy.school_year_name?.toLowerCase().includes(q),
      );
    },
    filteredPrograms() {
      if (!this.searchProgramQuery) return this.programs;
      const q = this.searchProgramQuery.toLowerCase();
      return this.programs.filter((p) =>
        p.program_name?.toLowerCase().includes(q),
      );
    },
  },
  methods: {
    ...mapActions(useFetchDataStore, ["fetchPrograms"]),
    async fetchSchoolYears() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years",
        );
        this.schoolYears = response.data;
      } catch (error) {
        console.error("Failed to load school years:", error);
      }
    },
    selectSchoolYear(sy) {
      this.form.school_year_id = sy.school_year_id;
      this.searchSchoolYearQuery = sy.school_year_name;
      this.showSchoolYearDropdown = false;
    },
    selectProgram(prog) {
      this.form.program_id = prog.program_id;
      this.searchProgramQuery = prog.program_name;
      this.showProgramDropdown = false;
    },

    async submitData() {
      try {
        // Validation
        if (!this.form.school_year_id) {
          toast.error("Please select a school year");
          return;
        }
        if (!this.form.program_id) {
          toast.error("Please select a program");
          return;
        }

        const payload = { ...this.form };

        if (this.isEdit) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/class/update-class/${this.classData.class_id}`,
            payload,
          );
          toast.success("Class updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/class/add-class",
            payload,
          );
          toast.success("Class added successfully!");
        }

        this.$emit("refresh");
        this.$emit("close");

        // Play audio, but handle errors separately
        try {
          const audio = new Audio(
            require(`@/assets/${this.isEdit ? "update.mp3" : "add.mp3"}`),
          );
          await audio.play();
        } catch (audioErr) {
          console.warn("Audio failed to play:", audioErr);
        }
      } catch (err) {
        console.error(err);
        toast.error(
          this.isEdit ? "Failed to update class." : "Failed to add class.",
        );
      }
    },
  },
  async mounted() {
    await this.fetchSchoolYears();
    await this.fetchPrograms();

    // if editing, fill the form
    if (this.isEdit) {
      this.form = {
        school_year_id: this.classData.school_year_id,
        program_id: this.classData.program_id,
        set_name: this.classData.set_name,
        class_size: this.classData.class_size,
      };
      this.searchSchoolYearQuery =
        this.classData.schoolYear?.school_year_name || "";
      this.searchProgramQuery = this.classData.program?.program_name || "";
    }
  },
};
</script>
