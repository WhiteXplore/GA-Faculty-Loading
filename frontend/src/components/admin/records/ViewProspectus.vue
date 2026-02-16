<template>
  <div class="p-4 bg-gray-50 min-h-screen">
    <!-- Top Controls -->
    <div class="flex items-center justify-between mb-2">
      <h1 class="text-xl font-semibold text-gray-800">
        {{ currentInstituteName }}
      </h1>

      <div class="flex items-center space-x-2">
        <!-- Program select -->
        <div class="relative w-[20rem]">
          <select
            v-model="selectedProgram"
            id="program"
            class="appearance-none w-full rounded-xl border border-green-500 bg-white px-6 py-2 pr-10 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-300 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
          >
            <option value="" disabled>Select a program</option>
            <option
              v-for="program in uniquePrograms"
              :key="program"
              :value="program"
            >
              {{ program }}
            </option>
          </select>

          <!-- Custom arrow -->
          <div
            class="absolute inset-y-0 right-3 flex items-center pointer-events-none"
          >
            <svg
              class="w-4 h-4 text-defaultGreen"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </div>
        </div>

        <!-- Generate report button -->
        <div
          @click="toggleGenerate"
          class="flex items-center gap-2 px-3 py-2 bg-white text-defaultGreen rounded-xl shadow-sm hover:shadow-md border border-green-500 hover:bg-green-600 hover:text-white transition-all duration-300 cursor-pointer"
        >
          <div
            class="flex items-center justify-center w-5 h-5 bg-white rounded-full group-hover:bg-green-100 transition-colors duration-300"
          >
            <icon
              :name="'circle-add'"
              class="w-4 h-4 text-defaultGreen transition-colors duration-300 group-hover:text-defaultGreen"
            />
          </div>
          <span class="font-medium text-sm">Generate Report</span>
        </div>
      </div>
    </div>

    <!-- Grouped Tables -->

    <div
      v-if="groupedCourses.length"
      class="bg-white rounded-lg p-6 space-y-6 overflow-x-auto h-[85vh] border shadow"
    >
      <!-- Header  -->
      <div class="flex gap-2 border-b-2 border-gray-300 pb-2 mb-4">
        <div class="flex items-center gap-2">
          <img src="@/assets/img/dnsc_logo.png" alt="" class="w-28" />
          <div class="flex flex-col text-left gap-1 font-poppins">
            <h1 class="text-2xl font-bold">DAVAO DEL NORTE</h1>
            <h1 class="text-2xl font-regular">STATE COLLEGE</h1>
            <p class="italic">"Inspiring Change, Creating Futures"</p>
          </div>
        </div>
        <div class="flex items-center gap-2 ml-auto text-right">
          <div>
            <p>president@dnsc.edu.ph</p>
            <p>dnsc.edu.ph</p>
            <p>@officialdnsc</p>
          </div>
          <div>
            <icon :name="'eye'" />
            <icon :name="'eye'" />
            <icon :name="'eye'" />
          </div>
        </div>
      </div>

      <!-- Sub Header  -->
      <div class="w-full text-center mb-6">
        <!-- <h1 class="uppercase text-lg">Office of the Registrar</h1> -->
        <p class="font-bold text-lg">{{ currentInstituteName }}</p>
        <p class="text-lg">{{ selectedProgram }}</p>
        <p v-if="filteredCourses.length" class="text-lg">
          Curriculum Checklist Year
          {{ filteredCourses[0].curriculum?.curriculum_start_year }}-
          {{ filteredCourses[0].curriculum?.curriculum_end_year }}
        </p>
      </div>

      <div
        v-for="(group, index) in groupedCourses"
        :key="index"
        class="text-[14px]"
      >
        <h3 class="text-md font-semibold text-gray-800 mb-2 px-4">
          {{ formatYearLevel(group.level) }} -
          {{ formatSemester(group.semester) }}
        </h3>

        <div class="">
          <table
            class="min-w-full table-fixed text-sm text-gray-700 border-collapse"
          >
            <thead class="text-gray-700 sticky top-0 z-10 bg-white">
              <tr>
                <th class="w-[10%] px-4 py-2 text-left font-bold rounded-tl-md">
                  Code
                </th>
                <th class="w-[25%] px-4 py-2 text-left font-bold">
                  Description
                </th>
                <th class="w-[10%] px-4 py-2 text-center font-bold">
                  Semester
                </th>
                <th class="w-[10%] px-4 py-2 text-center font-bold">Level</th>
                <th class="w-[10%] px-4 py-2 text-center font-bold">
                  Lec<br />Hours
                </th>
                <th class="w-[10%] px-4 py-2 text-center font-bold">
                  Lab<br />Hours
                </th>
                <th class="w-[10%] px-4 py-2 text-center font-bold">
                  Credit<br />Units
                </th>
                <th class="w-[15%] px-4 py-2 text-left font-bold rounded-tr-md">
                  Requisite
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="course in group.courses"
                :key="course.course_id"
                class="bg-white hover:bg-green-50"
              >
                <td class="px-4 py-2 text-left">{{ course.course_code }}</td>
                <td class="px-4 py-2 text-left">
                  {{ course.course_description }}
                </td>
                <td class="px-4 py-2 text-center">
                  {{ course.course_semester }}
                </td>
                <td class="px-4 py-2 text-center">{{ course.course_level }}</td>
                <td class="px-4 py-2 text-center">{{ course.course_lec }}</td>
                <td class="px-4 py-2 text-center">{{ course.course_lab }}</td>
                <td class="px-4 py-2 text-center">
                  {{ course.course_lec + course.course_lab }}
                </td>
                <td class="px-4 py-2 text-left">
                  {{ course.course_requisite }}
                </td>
              </tr>

              <!-- Totals Row -->
              <tr
                class="font-semibold text-gray-800 bg-gray-50 border-t border-gray-300"
              >
                <td colspan="6" class="px-4 py-2 text-right">
                  Total Credit Units:
                </td>
                <td class="px-4 py-2 text-center">
                  {{
                    group.courses.reduce(
                      (sum, course) =>
                        sum + course.course_lec + course.course_lab,
                      0,
                    )
                  }}
                </td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- No Courses Fallback -->
    <div v-else-if="selectedProgram" class="text-gray-500 text-center mt-6">
      No courses found for this curriculum.
    </div>

    <!-- Prompt to Select a Program -->
    <div
      v-else
      class="flex items-center justify-center min-h-screen border rounded-lg bg-white text-gray-400 text-center"
    >
      Please select a program to view curriculum courses.
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { mapState } from "pinia";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { eventBus } from "@/bus/event-bus";

export default {
  name: "ViewReportCurriculumPage",
  components: {
    icon,
  },

  data() {
    return {
      selectedProgram: "",
      selectedCurriculum: null,
      instituteId: null,

      // ✅ SAME AS TableCourses
      activeSchoolYear: null,
      stopEventBus: null,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["detailedReportCurriculum", "courses"]),

    currentInstituteName() {
      const match = this.detailedReportCurriculum.find(
        (item) => item.institute_id === this.instituteId,
      );
      return match?.institute_name || "No institute name found";
    },

    uniquePrograms() {
      if (!this.instituteId || !this.courses.length) return [];

      const programs = this.courses
        .filter(
          (course) =>
            String(course.curriculum?.program?.institute?.institute_id) ===
            String(this.instituteId),
        )
        .map((course) => course.curriculum?.program?.program_name)
        .filter(Boolean);

      return [...new Set(programs)];
    },

    filteredCourses() {
      if (!this.selectedProgram || !this.instituteId) return [];

      let result = this.courses || [];

      // Institute filter
      result = result.filter(
        (c) =>
          String(c.curriculum?.program?.institute?.institute_id) ===
          String(this.instituteId),
      );

      // Program filter
      result = result.filter(
        (c) => c.curriculum?.program?.program_name === this.selectedProgram,
      );

      // ✅ SAME ACTIVE YEAR FILTER AS TableCourses
      if (this.activeSchoolYear) {
        result = result.filter(
          (c) =>
            String(c.curriculum?.curriculum_start_year) ===
              String(this.activeSchoolYear.start_year) &&
            String(c.curriculum?.curriculum_end_year) ===
              String(this.activeSchoolYear.end_year) &&
            Number(c.course_semester) ===
              Number(this.activeSchoolYear.semester),
        );
      }

      return result;
    },

    groupedCourses() {
      const groups = {};

      this.filteredCourses.forEach((course) => {
        const key = `${course.course_level}-${course.course_semester}`;
        if (!groups[key]) {
          groups[key] = {
            level: course.course_level,
            semester: course.course_semester,
            courses: [],
          };
        }
        groups[key].courses.push(course);
      });

      return Object.values(groups).sort((a, b) => {
        if (a.level === b.level) return a.semester - b.semester;
        return a.level - b.level;
      });
    },
  },

  watch: {
    selectedProgram(newProgram) {
      if (!newProgram || !this.instituteId) return;

      const curriculum = this.detailedReportCurriculum.find(
        (curr) =>
          curr.program?.program_name === newProgram &&
          String(curr.program?.institute?.institute_id) ===
            String(this.instituteId),
      );

      this.selectedCurriculum = curriculum || null;
    },
  },

  methods: {
    formatYearLevel(level) {
      switch (level) {
        case 1:
          return "First Year";
        case 2:
          return "Second Year";
        case 3:
          return "Third Year";
        case 4:
          return "Fourth Year";
        default:
          return `Year ${level}`;
      }
    },

    formatSemester(sem) {
      return sem === 1
        ? "First Semester"
        : sem === 2
        ? "Second Semester"
        : `Semester ${sem}`;
    },

    toggleGenerate() {
      console.log("Generate Report clicked!");
    },
  },

  async mounted() {
    const store = useFetchDataStore();
    this.instituteId = parseInt(this.$route.params.institute_id);

    if (!this.instituteId) {
      console.error("No institute_id provided in the route.");
      return;
    }

    // ✅ READ YEAR FROM ROUTE QUERY (IF PRESENT)
    const { sy_start, sy_end, semester } = this.$route.query;

    if (sy_start && sy_end && semester) {
      this.activeSchoolYear = {
        start_year: sy_start,
        end_year: sy_end,
        semester: Number(semester),
      };
    }

    if (!this.detailedReportCurriculum.length) {
      await store.fetchReportCurriculum();
    }

    if (!this.courses.length) {
      await store.fetchCourses();
    }

    this.stopEventBus = eventBus.on((newYear) => {
      if (!newYear) return;
      this.activeSchoolYear = newYear;
    });
  },

  beforeUnmount() {
    this.stopEventBus?.();
  },
};
</script>
