<template>
  <div
    class="fixed inset-0 flex justify-center items-center bg-gray-800 bg-opacity-40 z-50"
  >
    <div
      class="rounded-[16px] shadow-lg flex flex-col lg:flex-row animate-slideUp overflow-hidden"
    >
      <!-- LEFT: Main Form -->
      <form
        @submit.prevent="submitData"
        class="w-full lg:w-[60vw] text-[13px] bg-white rounded-b-[16px] lg:rounded-b-none lg:rounded-l-[16px] shadow-md flex flex-col"
        ref="yearSectionForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 bg-defaultGreen text-white rounded-t-[16px] lg:rounded-tl-[16px] lg:rounded-tr-none flex justify-between items-center border-b border-green-700 shadow"
        >
          <div class="flex gap-2 items-center">
            <icon :name="'add-students'" class="size-5" />
            <h1 class="font-semibold tracking-wide text-lg">
              Add Year/Section – {{ programData.program_name }}
            </h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer hover:scale-110 transition-transform"
          />
        </div>

        <!-- Body -->
        <div class="p-6 space-y-6 text-[13px] max-h-[80vh] overflow-y-auto">
          <div class="flex flex-col space-y-2">
            <!-- PROGRAM INFO -->
            <div class="p-4 bg-gray-50 border rounded-xl">
              <div
                class="flex flex-col md:flex-row md:items-center md:justify-between gap-2"
              >
                <p class="text-gray-800">
                  <span class="font-semibold text-gray-800">Program:</span>
                  {{ programData.program_name }} ({{
                    programData.program_code
                  }})
                </p>
              </div>
            </div>
            <!-- Instructions -->
            <div class="p-4 bg-blue-50 border rounded-xl">
              <h3 class="font-bold text-gray-800">Instructions</h3>
              <ul
                class="list-disc list-inside text-gray-700 space-y-1 text-[12px]"
              >
                <li>Click "Add Year/Section" to configure sections.</li>
                <li>Set number of sections for each year level (1st–4th).</li>
                <li>Sections will be automatically named (A, B, C, etc.).</li>
              </ul>
            </div>
          </div>

          <!-- School Year Selection -->
          <div class="flex flex-col space-y-2 w-full relative">
            <label class="font-semibold text-gray-800">
              School Year <span class="text-red-500">*</span>
            </label>
            <input
              v-model="searchSchoolYearQuery"
              type="text"
              placeholder="Search school year..."
              required
              class="px-4 py-3 border border-gray-300 rounded-lg text-gray-800 focus:ring-2 focus:ring-green-400 focus:border-green-400 outline-none transition"
              @focus="showSchoolYearDropdown = true"
            />
            <div
              v-if="showSchoolYearDropdown && filteredSchoolYears.length"
              class="absolute top-[75px] w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-40 overflow-y-auto z-10"
              @mouseleave="showSchoolYearDropdown = false"
            >
              <div
                v-for="sy in filteredSchoolYears"
                :key="sy.school_year_id"
                class="px-4 py-2 hover:bg-green-50 cursor-pointer transition-colors"
                @mousedown="selectSchoolYear(sy)"
              >
                {{ sy.school_year_name }}
              </div>
            </div>
          </div>

          <!-- Year/Section Configuration -->
          <div class="mt-2">
            <h3
              class="font-semibold text-gray-800 text-md mb-4 flex items-center gap-2"
            >
              <icon name="setting" class="size-4 text-green-700" />
              <span> Configure Sections per Year Level</span>
            </h3>

            <div class="space-y-6">
              <!-- Each Year Level Card -->
              <div
                v-for="year in yearLevels"
                :key="year.value"
                class="rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200"
              >
                <!-- Header -->
                <div
                  class="flex justify-between items-center px-5 py-3 bg-green-50 border-b rounded-t-xl"
                >
                  <div class="flex items-start gap-2">
                    <icon name="calendar" class="size-4 text-green-700" />
                    <h4 class="font-semibold text-green-800 tracking-wide">
                      {{ year.label }}
                    </h4>
                  </div>

                  <!-- Number of Sections Input -->
                  <div class="flex items-center gap-2 text-sm">
                    <label class="text-gray-700 font-medium whitespace-nowrap">
                      Sections:
                    </label>
                    <input
                      v-model.number="year.numSections"
                      type="number"
                      min="0"
                      max="10"
                      class="w-20 border border-gray-300 rounded-md px-3 py-1.5 text-center focus:ring-2 focus:ring-defaultGreen focus:border-defaultGreen outline-none transition"
                      placeholder="0"
                      @input="updateSections(year)"
                    />
                  </div>
                </div>

                <!-- Section List -->
                <transition-group
                  name="fade"
                  tag="div"
                  class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 px-5 py-4"
                >
                  <div
                    v-for="(section, index) in year.sections"
                    :key="index"
                    class="group bg-green-50 border border-green-100 rounded-lg shadow-sm hover:border-defaultGreen transition-all duration-200 p-4 flex flex-col gap-2 relative"
                  >
                    <!-- Section Header -->
                    <div class="flex justify-between items-center">
                      <span class="font-semibold text-defaultGreen text-sm">
                        Section {{ getSectionLetter(index) }}
                      </span>
                      <span
                        class="bg-green-100 text-green-700 text-xs font-medium px-2 py-0.5 rounded-full"
                      >
                        {{ section.classSize || 0 }} students
                      </span>
                    </div>

                    <!-- Class Size Input -->
                    <div class="flex items-center gap-2 mt-2">
                      <icon name="users" class="size-4 text-defaultGreen" />
                      <input
                        v-model.number="section.classSize"
                        type="number"
                        min="1"
                        max="100"
                        class="flex-1 border border-gray-300 rounded-md px-3 py-2 text-center text-sm focus:ring-2 focus:ring-green-300 focus:border-green-400 outline-none transition"
                        placeholder="Enter size"
                      />
                    </div>
                  </div>
                </transition-group>

                <!-- Helper -->
                <div
                  v-if="year.numSections === 0"
                  class="text-gray-500 text-sm italic px-5 py-3 border-t border-green-100 bg-gray-50 rounded-b-xl"
                >
                  No sections configured for {{ year.label }}.
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Buttons -->
        <div class="flex justify-end gap-2 pt-4 border-t p-4">
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
            :disabled="totalSections === 0 || !selectedSchoolYearId"
          >
            Create Sections
          </button>
        </div>
      </form>

      <!-- RIGHT: Summary Section -->
      <div
        class="w-full lg:w-[25vw] bg-gray-50 p-4 border-l border-green-100 flex flex-col justify-start rounded-b-[16px] lg:rounded-b-none lg:rounded-r-[16px] overflow-y-auto max-h-[99vh] shadow-inner"
        v-if="totalSections > 0"
      >
        <!-- Header -->
        <div
          class="font-semibold text-lg text-green-800 mb-4 flex items-center gap-2"
        >
          <icon name="summary" />
          <h2>Summary</h2>
        </div>

        <!-- Total Sections -->
        <p class="text-sm mb-3 text-gray-700">
          Total sections to be created:
          <span class="font-bold text-green-700">{{ totalSections }}</span>
        </p>

        <!-- Year Levels -->
        <div class="text-sm text-gray-700 space-y-4">
          <div v-for="year in yearLevels" :key="year.value">
            <div
              v-if="year.numSections > 0 && year.sections.length > 0"
              class="bg-white rounded-xl shadow-sm border border-green-100 p-3 transition-all duration-200"
            >
              <h3 class="font-semibold text-green-700 mb-2">
                {{ year.label }}
              </h3>

              <div class="space-y-2">
                <div
                  v-for="(section, index) in year.sections"
                  :key="index"
                  class="flex justify-between items-center bg-green-50 rounded-md px-3 py-2 border border-green-100 hover:bg-green-100 transition-colors duration-200"
                >
                  <span class="text-gray-800 font-medium">
                    Section {{ getSectionLetter(index) }}
                  </span>
                  <span class="text-gray-600 text-xs">
                    {{ section.classSize }} students
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- No Sections -->
        <div
          v-if="totalSections === 0"
          class="text-gray-500 text-sm italic mt-4 text-center"
        >
          No sections configured yet.
        </div>
      </div>
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
        sy.school_year_name?.toLowerCase().includes(q),
      );
    },
    totalSections() {
      return this.yearLevels.reduce(
        (sum, year) => sum + (year.numSections || 0),
        0,
      );
    },
  },
  methods: {
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
          axios.post(
            process.env.VUE_APP_API_BASE_URL + "/class/add-class",
            classData,
          ),
        );

        await Promise.all(promises);

        toast.success(
          `Successfully created ${classesToCreate.length} section(s)!`,
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

<style>
/* Scrollbar styling */
section::-webkit-scrollbar {
  width: 8px;
}
section::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.25);
  border-radius: 10px;
}
/* Elegant Glass Green Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 128, 0, 0.05); /* faint green track */
  border-radius: 10px;
  backdrop-filter: blur(4px);
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(
    180deg,
    rgba(34, 197, 94, 0.4) 0%,
    rgba(21, 128, 61, 0.6) 100%
  );
  border-radius: 10px;
  box-shadow: inset 0 0 4px rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(6px);
  transition: all 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(
    180deg,
    rgba(34, 197, 94, 0.6) 0%,
    rgba(21, 128, 61, 0.8) 100%
  );
  box-shadow: inset 0 0 6px rgba(255, 255, 255, 0.4);
}
</style>
