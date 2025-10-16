<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="yearSectionForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              Add Year/Section - {{ programData.program_name }}
            </h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- Body -->
        <div class="p-5 w-[50vw] space-y-5">
          <!-- Program Info -->
          <div class="bg-blue-50 p-3 rounded-md">
            <p class="text-sm">
              <span class="font-bold">Program:</span>
              {{ programData.program_code }} - {{ programData.program_name }}
            </p>
            <p class="text-sm" v-if="programData.institute">
              <span class="font-bold">Institute:</span>
              {{ programData.institute.institute_name }}
            </p>
          </div>

          <!-- School Year Selection -->
          <div class="flex flex-col space-y-2 w-full relative">
            <label class="font-bold">School Year <span class="text-red-500">*</span>:</label>
            <input
              v-model="searchSchoolYearQuery"
              type="text"
              placeholder="Search school year..."
              required
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

          <!-- Year/Section Configuration -->
          <div class="mt-4">
            <h3 class="font-bold mb-3">Configure Sections per Year Level:</h3>
            
            <div class="space-y-4">
              <div
                v-for="year in yearLevels"
                :key="year.value"
                class="border rounded-lg p-4 bg-white"
              >
                <!-- Year Level Header -->
                <div class="flex items-center gap-4 mb-3">
                  <label class="font-semibold text-gray-800 min-w-[100px]">
                    {{ year.label }}:
                  </label>
                  <div class="flex items-center gap-2">
                    <label class="text-sm text-gray-600">Number of Sections:</label>
                    <input
                      v-model.number="year.numSections"
                      type="number"
                      min="0"
                      max="10"
                      class="w-20 border border-gray-300 rounded-md px-3 py-2 text-center"
                      placeholder="0"
                      @input="updateSections(year)"
                    />
                  </div>
                </div>

                <!-- Individual Section Inputs -->
                <div
                  v-if="year.numSections > 0"
                  class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mt-3 pl-4 border-l-4 border-green-200"
                >
                  <div
                    v-for="(section, index) in year.sections"
                    :key="index"
                    class="flex items-center gap-2 bg-gray-50 p-3 rounded-md"
                  >
                    <label class="font-semibold text-sm min-w-[80px]">
                      Section {{ getSectionLetter(index) }}:
                    </label>
                    <input
                      v-model.number="section.classSize"
                      type="number"
                      min="1"
                      max="100"
                      class="flex-1 border border-gray-300 rounded-md px-3 py-2 text-center"
                      placeholder="30"
                    />
                    <span class="text-xs text-gray-500">students</span>
                  </div>
                </div>
              </div>
            </div>

            <p class="text-xs text-gray-500 mt-3 bg-blue-50 p-2 rounded">
              <strong>Note:</strong> Enter the number of sections for each year level, then specify the class size for each section individually.
            </p>
          </div>

          <!-- Summary -->
          <div class="bg-green-50 p-3 rounded-md" v-if="totalSections > 0">
            <p class="font-bold text-sm">Summary:</p>
            <p class="text-sm">
              Total sections to be created: <span class="font-bold">{{ totalSections }}</span>
            </p>
            <div class="mt-2 text-xs text-gray-700 space-y-1">
              <div v-for="year in yearLevels" :key="year.value">
                <div v-if="year.numSections > 0 && year.sections.length > 0">
                  <span class="font-semibold">{{ year.label }}:</span>
                  <div class="ml-4 mt-1">
                    <span
                      v-for="(section, index) in year.sections"
                      :key="index"
                      class="inline-block mr-3"
                    >
                      Section {{ getSectionLetter(index) }} ({{ section.classSize }} students)
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2 mt-4">
            <button
              type="button"
              class="bg-red-600 p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-red-800 hover:text-red-800"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800"
              type="submit"
              :disabled="totalSections === 0 || !selectedSchoolYearId"
            >
              Create {{ totalSections }} Section(s)
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

export default {
  name: "AddYearSectionModal",
  components: { icon },
  props: {
    programData: { type: Object, required: true },
  },
  data() {
    return {
      selectedSchoolYearId: null,
      searchSchoolYearQuery: "",
      showSchoolYearDropdown: false,
      schoolYears: [],
      yearLevels: [
        { value: 1, label: "1st Year", numSections: 0, sections: [] },
        { value: 2, label: "2nd Year", numSections: 0, sections: [] },
        { value: 3, label: "3rd Year", numSections: 0, sections: [] },
        { value: 4, label: "4th Year", numSections: 0, sections: [] },
      ],
    };
  },
  computed: {
    filteredSchoolYears() {
      if (!this.searchSchoolYearQuery) return this.schoolYears;
      const q = this.searchSchoolYearQuery.toLowerCase();
      return this.schoolYears.filter((sy) =>
        sy.school_year_name?.toLowerCase().includes(q)
      );
    },
    totalSections() {
      return this.yearLevels.reduce((sum, year) => sum + (year.numSections || 0), 0);
    },
  },
  methods: {
    async fetchSchoolYears() {
      try {
        const response = await axios.get(
          "http://localhost:8000/school-year/get-school-years"
        );
        this.schoolYears = response.data;
      } catch (error) {
        console.error("Failed to load school years:", error);
      }
    },
    selectSchoolYear(sy) {
      this.selectedSchoolYearId = sy.school_year_id;
      this.searchSchoolYearQuery = sy.school_year_name;
      this.showSchoolYearDropdown = false;
    },
    getSectionLetter(index) {
      const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
      return letters[index] || "?";
    },
    getSectionNames(numSections) {
      const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
      const names = [];
      for (let i = 0; i < numSections; i++) {
        names.push(letters[i]);
      }
      return names.join(", ");
    },
    updateSections(year) {
      const currentNum = year.sections.length;
      const newNum = year.numSections || 0;

      if (newNum > currentNum) {
        // Add new sections
        for (let i = currentNum; i < newNum; i++) {
          year.sections.push({ classSize: 30 });
        }
      } else if (newNum < currentNum) {
        // Remove excess sections
        year.sections.splice(newNum);
      }
    },
    async submitData() {
      try {
        if (!this.selectedSchoolYearId) {
          toast.error("Please select a school year");
          return;
        }

        if (this.totalSections === 0) {
          toast.error("Please add at least one section");
          return;
        }

        const classesToCreate = [];
        const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        // Generate class records for each year level
        this.yearLevels.forEach((year) => {
          if (year.numSections > 0 && year.sections.length > 0) {
            year.sections.forEach((section, index) => {
              const sectionLetter = letters[index];
              classesToCreate.push({
                school_year_id: this.selectedSchoolYearId,
                program_id: this.programData.program_id,
                set_name: `${year.label} - ${sectionLetter}`,
                class_size: section.classSize || 30,
              });
            });
          }
        });

        // Create all classes
        const promises = classesToCreate.map((classData) =>
          axios.post("http://localhost:8000/class/add-class", classData)
        );

        await Promise.all(promises);

        toast.success(
          `Successfully created ${classesToCreate.length} section(s)!`
        );

        this.$emit("refresh");
        this.$emit("close");

        // Play audio
        try {
          const audio = new Audio(require("@/assets/add.mp3"));
          await audio.play();
        } catch (audioErr) {
          console.warn("Audio failed to play:", audioErr);
        }
      } catch (err) {
        console.error(err);
        toast.error("Failed to create sections.");
      }
    },
  },
  async mounted() {
    await this.fetchSchoolYears();
  },
};
</script>

