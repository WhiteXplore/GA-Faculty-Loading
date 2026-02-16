<template>
  <div class="space-y-6 text-[13px]">
    <!-- HEADER -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4">Pages / Assigned Course</div>
      <button
        v-if="user?.role !== 'Admin'"
        @click="openAssignCoursesModal"
        class="flex items-center gap-2 px-4 py-2 text-defaultGreen bg-white border border-green-500 rounded-xl shadow-sm hover:bg-green-600 hover:text-white transition-all duration-300"
      >
        <div
          class="flex items-center justify-center w-5 h-5 bg-green-100 rounded-full"
        >
          <icon name="circle-add" class="w-4 h-4" />
        </div>
        <span class="font-medium">Assign Course</span>
      </button>
    </div>

    <!-- ===================== ADMIN VIEW ===================== -->
    <div v-if="user?.role === 'Admin'">
      <!-- TABLE VIEW -->
      <div
        v-if="!selectedGroup"
        class="bg-white border rounded-xl shadow-sm overflow-hidden"
      >
        <table class="w-full text-sm">
          <thead class="bg-defaultGreen text-white">
            <tr>
              <th class="py-3 px-4 text-left w-[20%]">Institute</th>
              <th class="py-3 px-4 text-left w-[25%]">Program</th>
              <th class="py-3 px-4 text-center w-[20%]">School Year</th>
              <th class="py-3 px-4 text-center w-[20%]">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(group, index) in groupedList"
              :key="index"
              class="border-b hover:bg-gray-50 transition"
            >
              <td class="py-3 px-4">{{ group.institute }}</td>
              <td class="py-3 px-4">{{ group.program }}</td>
              <td class="py-3 px-4 text-center">{{ group.schoolYear }}</td>
              <td class="py-3 px-4 flex justify-center">
                <button
                  class="px-3 py-1 h-8 border border-blue-300 hover:bg-blue-200 text-blue-800 rounded-lg flex items-center gap-1"
                >
                  <icon name="eye" /> View
                </button>
              </td>
            </tr>
            <tr v-if="groupedList.length === 0">
              <td colspan="4" class="py-4 text-center text-gray-500">
                No assigned courses found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- DETAILED VIEW -->
      <div
        v-else
        class="bg-white border rounded-2xl p-5 mt-5 shadow-sm animate-fadeIn"
      >
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
          <div>
            <h2 class="text-lg font-bold text-gray-800">
              {{ selectedGroup.program }} ({{ selectedGroup.schoolYear }})
            </h2>
            <p class="text-sm text-gray-700">
              {{ selectedGroup.institute }}
            </p>
          </div>
          <button
            @click="closeDetails"
            class="flex items-center gap-1 px-3 py-1 text-sm bg-gray-200 hover:bg-gray-300 rounded-lg transition"
          >
            ← Back to List
          </button>
        </div>

        <!-- YEAR LEVEL SECTIONS (with collapsible headers + counts) -->
        <div class="space-y-4">
          <div
            v-for="year in [1, 2, 3, 4]"
            :key="year"
            class="border rounded-xl overflow-hidden"
          >
            <!-- Header with Arrow + Year Label + Count -->
            <div
              @click="toggleYearDisplay(year)"
              class="flex justify-between items-center p-3 bg-gray-50 hover:bg-gray-100 cursor-pointer border-b"
            >
              <div class="flex items-center gap-2">
                <icon
                  :name="
                    expandedYears.includes(year) ? 'arrow-down' : 'arrow-right'
                  "
                  class="w-4 h-4 text-gray-600"
                />
                <h4 class="font-semibold text-sm text-gray-800">
                  {{ getYearLabel(year) }}
                </h4>
              </div>
              <span
                v-if="getCoursesByYear(selectedGroup.courses, year).length > 0"
                class="px-2 py-1 bg-defaultGreen text-white text-xs rounded-full"
              >
                {{ getCoursesByYear(selectedGroup.courses, year).length }}
                course(s)
              </span>
            </div>

            <!-- Expandable Table -->
            <transition name="fade">
              <div v-if="expandedYears.includes(year)" class="p-2 bg-white">
                <div
                  v-if="
                    getCoursesByYear(selectedGroup.courses, year).length > 0
                  "
                  class="overflow-x-auto border rounded-lg"
                >
                  <table class="min-w-full border rounded-lg overflow-hidden">
                    <thead class="bg-defaultGreen text-white text-sm">
                      <tr>
                        <th class="px-4 py-2 border-b text-left w-1/4">
                          Course Code
                        </th>
                        <th class="px-4 py-2 border-b text-left">
                          Course Description
                        </th>
                      </tr>
                    </thead>
                    <tbody class="text-gray-700 text-sm">
                      <tr
                        v-for="course in getCoursesByYear(
                          selectedGroup.courses,
                          year,
                        )"
                        :key="course.id"
                        class="border-b hover:bg-gray-50 transition"
                      >
                        <td class="px-4 py-3">
                          {{ course.course?.course_code }}
                        </td>
                        <td class="px-4 py-3">
                          {{ course.course?.course_description }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <div v-else class="text-sm text-gray-400 italic ml-2">
                  No courses assigned for this year.
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>

    <!-- ===================== PROGRAM CHAIRPERSON VIEW ===================== -->
    <div
      v-else-if="userProgram"
      class="bg-white border p-5 rounded-2xl shadow-sm"
    >
      <h2 class="text-lg font-bold text-gray-800">
        {{ userProgram.program_name }}
      </h2>
      <p class="text-sm text-gray-600" v-if="userProgram.institute">
        Institute: {{ userProgram.institute.institute_name }}
      </p>

      <div class="mt-5 space-y-4">
        <div
          v-for="year in [1, 2, 3, 4]"
          :key="year"
          class="border rounded-xl overflow-hidden"
        >
          <!-- Header with arrow and course count -->
          <div
            @click="toggleYearDisplay(year)"
            class="flex justify-between items-center p-3 bg-gray-50 hover:bg-gray-100 cursor-pointer border-b"
          >
            <div class="flex items-center gap-2">
              <icon
                :name="
                  expandedYears.includes(year) ? 'arrow-down' : 'arrow-right'
                "
                class="w-4 h-4 text-gray-600"
              />
              <h4 class="font-semibold text-sm text-gray-800">
                {{ getYearLabel(year) }}
              </h4>
            </div>
            <span
              v-if="getCoursesByYear(assignedCourses, year).length > 0"
              class="px-2 py-1 bg-defaultGreen text-white text-xs rounded-full"
            >
              {{ getCoursesByYear(assignedCourses, year).length }} course(s)
            </span>
          </div>

          <!-- Expandable Table -->
          <transition name="fade">
            <div v-if="expandedYears.includes(year)" class="p-2 bg-white">
              <div
                v-if="getCoursesByYear(assignedCourses, year).length > 0"
                class="overflow-x-auto border rounded-lg"
              >
                <table
                  class="min-w-full border rounded-lg overflow-hidden text-sm"
                >
                  <thead class="bg-defaultGreen text-white">
                    <tr>
                      <th class="px-4 py-2 border-b text-left w-1/4">
                        Course Code
                      </th>
                      <th class="px-4 py-2 border-b text-left">
                        Course Description
                      </th>
                    </tr>
                  </thead>
                  <tbody class="text-gray-700">
                    <tr
                      v-for="course in getCoursesByYear(assignedCourses, year)"
                      :key="course.id"
                      class="border-b hover:bg-gray-50 transition"
                    >
                      <td class="px-4 py-3">
                        {{ course.course?.course_code }}
                      </td>
                      <td class="px-4 py-3">
                        {{ course.course?.course_description }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div v-else class="text-sm text-gray-400 italic ml-2">
                No courses assigned for this year.
              </div>
            </div>
          </transition>
        </div>
      </div>
      <!-- MODAL FOR CHAIRPERSON -->
      <assignYearCourses
        v-if="showAssignCoursesModal && userProgram"
        :programData="userProgram"
        @close="closeAssignCoursesModal"
        @refresh="loadAssignedCourses"
      />
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import assignYearCourses from "@/components/admin/records/modals/assign-year-courses.vue";
import axios from "axios";

export default {
  name: "AssignCoursesManagement",
  components: { icon, assignYearCourses },
  data() {
    return {
      user: null,
      userProgram: null,
      assignedCourses: [],
      showAssignCoursesModal: false,
      activeSchoolYearId: null,
      expandedYears: [1, 2, 3, 4],
      selectedGroup: null,
    };
  },
  computed: {
    groupedList() {
      if (!this.assignedCourses.length) return [];
      const groups = {};
      this.assignedCourses.forEach((item) => {
        const key = `${item.program?.institute?.institute_name}|${item.program?.program_name}|${item.schoolYear?.school_year_name}`;
        if (!groups[key]) {
          groups[key] = {
            institute: item.program?.institute?.institute_name,
            program: item.program?.program_name,
            schoolYear: item.schoolYear?.school_year_name,
            courses: [],
          };
        }
        groups[key].courses.push(item);
      });
      return Object.values(groups);
    },
  },
  methods: {
    async fetchUser() {
      const { data } = await axios.get(
        process.env.VUE_APP_API_BASE_URL + "/auth/me",
        {
          withCredentials: true,
        },
      );
      this.user = data;
    },
    async loadUserProgram() {
      if (this.user?.role !== "Program Chairperson") return;
      const { data } = await axios.get(
        process.env.VUE_APP_API_BASE_URL + "/programs/get-programs",
      );
      this.userProgram = data.find(
        (p) => String(p.program_id) === String(this.user.program_id),
      );
    },
    async loadAssignedCourses() {
      const url =
        this.user?.role === "Admin"
          ? process.env.VUE_APP_API_BASE_URL + "/program-year-courses/get-all"
          : process.env.VUE_APP_API_BASE_URL +
            "/program-year-courses/get-by-program-and-school-year";
      const params =
        this.user?.role !== "Admin"
          ? {
              program_id: this.userProgram.program_id,
              school_year_id: this.activeSchoolYearId,
            }
          : {};
      const { data } = await axios.get(url, { params });
      this.assignedCourses = data;
    },
    async loadSchoolYears() {
      const { data } = await axios.get(
        process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years",
      );
      const active = data.find((s) => s.is_active);
      if (active) this.activeSchoolYearId = active.school_year_id;
    },
    getYearLabel(year) {
      return ["1st", "2nd", "3rd", "4th"][year - 1] + " Year";
    },
    getCoursesByYear(courses, year) {
      return courses.filter((c) => c.year_level === year);
    },
    toggleYearDisplay(year) {
      const idx = this.expandedYears.indexOf(year);
      if (idx > -1) this.expandedYears.splice(idx, 1);
      else this.expandedYears.push(year);
    },
    viewDetails(group) {
      this.selectedGroup = group;
    },
    closeDetails() {
      this.selectedGroup = null;
    },
    openAssignCoursesModal() {
      this.showAssignCoursesModal = true;
    },
    closeAssignCoursesModal() {
      this.showAssignCoursesModal = false;
      this.loadAssignedCourses();
    },
  },
  async mounted() {
    await this.fetchUser();
    await this.loadSchoolYears();
    await this.loadUserProgram();
    await this.loadAssignedCourses();
  },
};
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
