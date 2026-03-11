<template>
  <div
    class="w-[45vw] h-[47vh] bg-white border shadow-xl transition-all duration-300 flex flex-col justify-start rounded-xl overflow-hidden p-1"
  >
    <!-- Header -->
    <div
      class="flex items-center justify-between px-2 py-2 text-white bg-defaultGreen rounded-t-lg"
    >
      <h3 class="font-semibold text-base ml-2">Unscheduled Courses</h3>

      <div class="flex items-center gap-2">
        <input
          v-model="searchQuery"
          @input="changePage(1)"
          type="text"
          placeholder="Search course, program, SY..."
          class="rounded-full border border-green-600 px-4 py-2 text-xs w-64 focus:outline-none focus:ring-2 focus:ring-green-400"
        />
      </div>
    </div>

    <!-- Body -->
    <div class="flex-1 overflow-y-auto p-2">
      <!-- Table -->
      <div class="w-full rounded-md border bg-white overflow-hidden">
        <table class="min-w-full text-xs text-gray-700">
          <thead class="bg-gray-100 text-defaultGreen">
            <tr>
              <th class="px-4 py-3 text-left">Set</th>
              <th class="px-4 py-3 text-center">Program</th>
              <th class="px-4 py-3 text-left">Course</th>
              <th class="px-4 py-3 text-center">Type</th>
              <th class="px-4 py-3 text-center">Semester</th>
              <th class="px-4 py-3 text-center w-[29%]">Reason</th>
              <th class="px-4 py-3 text-center">Action</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="item in paginatedData"
              :key="item.id"
              class="border-t hover:bg-green-50"
            >
              <td class="px-4 py-3 font-semibold">
                {{ getSetName(item.class_id) }}
              </td>
              <td class="px-4 py-3 text-center">{{ item.program_code }}</td>
              <td class="px-4 py-3 font-semibold">{{ item.course_code }}</td>
              <td class="px-4 py-3 text-center">{{ item.type }}</td>
              <td class="px-4 py-3 text-center">
                {{ semesterLabel(item.semester) }}
              </td>
              <td class="px-4 py-3 text-xs text-red-600 max-w-xs">
                {{ item.reason }}
              </td>
              <td class="px-4 py-3 text-center">
                <button
                  @click="openAssignModal(item)"
                  class="px-3 py-1 text-white bg-defaultGreen rounded-md hover:bg-green-700 text-xs"
                >
                  Assign
                </button>
              </td>
            </tr>

            <tr v-if="paginatedData.length === 0">
              <td colspan="7" class="text-center py-8 text-gray-400">
                No unscheduled courses found
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4 text-xs">
        <div class="text-gray-700">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredData.length }} entries
        </div>
        <div class="flex items-center gap-1">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400"
          >
            &lt;
          </button>

          <span v-for="page in pageNumbers" :key="'page-' + page">
            <button
              @click="changePage(page)"
              :class="{
                'bg-defaultGreen text-white': currentPage === page,
                'bg-gray-200 text-gray-700': currentPage !== page,
              }"
              class="px-3 py-1 rounded-md hover:bg-green-300"
            >
              {{ page }}
            </button>
          </span>

          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>

    <!-- Assign Modal -->
    <div
      v-if="assignModalVisible"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
    >
      <div class="bg-white w-[400px] rounded-xl shadow-xl p-6 relative">
        <h3 class="font-semibold text-lg mb-4">Assign Course</h3>
        <p class="mb-4">
          Assign
          <span class="font-bold">{{ selectedCourse.course_code }}</span> to an
          instructor.
        </p>

        <select
          v-model="selectedInstructor"
          class="w-full border rounded px-3 py-2 mb-4 text-sm"
        >
          <option value="">Select Instructor</option>
          <option
            v-for="instr in uniqueInstructors"
            :key="instr.faculty_id"
            :value="instr.faculty_id"
          >
            {{ instr.faculty_name }}
          </option>
        </select>

        <div class="flex justify-end gap-2">
          <button
            @click="closeAssignModal"
            class="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400 text-xs"
          >
            Cancel
          </button>
          <button
            @click="assignCourse"
            class="px-3 py-1 bg-defaultGreen text-white rounded hover:bg-green-700 text-xs"
          >
            Assign
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useFetchDataStore } from "@/store/fetch-data-store";
import axios from "axios";

export default {
  name: "AssignCoursePage",
  props: { closeAddSchedulePanel: { type: Function, required: true } },

  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      user: {},
      assignModalVisible: false,
      selectedCourse: {},
      selectedInstructor: "",
    };
  },

  computed: {
    store() {
      return useFetchDataStore();
    },

    filteredData() {
      const query = this.searchQuery?.toLowerCase() || "";
      return this.store.unscheduled_meetings.filter((item) => {
        const isSameProgram = this.user.program_id
          ? item.program_id === this.user.program_id
          : true;
        const matchesQuery =
          item.course_code?.toLowerCase().includes(query) ||
          item.program_name?.toLowerCase().includes(query) ||
          item.school_year?.toLowerCase().includes(query) ||
          item.type?.toLowerCase().includes(query) ||
          item.semester?.toLowerCase().includes(query) ||
          item.reason?.toLowerCase().includes(query);
        return isSameProgram && matchesQuery;
      });
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredData.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;
    },

    pageNumbers() {
      return Array.from({ length: this.totalPages }, (_, i) => i + 1);
    },

    startIndex() {
      return this.filteredData.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(
        this.currentPage * this.itemsPerPage,
        this.filteredData.length,
      );
    },

    uniqueInstructors() {
      if (!this.user.program_id) return [];
      const seen = new Set();
      return (this.store.final_schedules || [])
        .filter((s) => s.faculty_id && s.program_id === this.user.program_id)
        .filter((s) => {
          if (seen.has(s.faculty_id)) return false;
          seen.add(s.faculty_id);
          return true;
        });
    },
  },

  methods: {
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },

    semesterLabel(sem) {
      return sem === "1" ? "1st Semester" : sem === "2" ? "2nd Semester" : sem;
    },

    openAssignModal(item) {
      const courseInfo = this.store.courses?.find(
        (c) => c.course_id === item.course_id,
      );
      const programInfo = this.store.programs?.find(
        (p) => p.program_id === item.program_id,
      );

      this.selectedCourse = {
        ...item,
        course_code: item.course_code || courseInfo?.course_code || "Unknown",
        program_code:
          item.program_code || programInfo?.program_code || "Unknown",
        set_name: this.getSetName(item.class_id) || `Set ${item.class_id}`,
        hours: item.hours || "3h lec",
      };

      this.assignModalVisible = true;
    },

    closeAssignModal() {
      this.assignModalVisible = false;
      this.selectedCourse = {};
      this.selectedInstructor = "";
    },

    assignCourse() {
      if (!this.selectedInstructor) {
        return alert("Please select an instructor");
      }

      const course = {
        ...JSON.parse(JSON.stringify(this.selectedCourse)),
        faculty_id: this.selectedInstructor,
        faculty_name: this.getFacultyName(this.selectedInstructor),
      };
      delete course.id;

      // Determine durations
      const lectureMatch = course.hours?.match(/(\d+(\.\d+)?)h lec/);
      const labMatch = course.hours?.match(/(\d+(\.\d+)?)h lab/);
      const lectureDuration = lectureMatch ? parseFloat(lectureMatch[1]) : 3;
      const labDuration = labMatch ? parseFloat(labMatch[1]) : 3;

      const instituteId = this.getInstituteId(course.program_id);

      let payload = [];

      if (course.type === "Lecture+Lab") {
        payload = [
          {
            ...course,
            type: "Lecture",
            duration: lectureDuration,
            institute_id: instituteId,
            start_hour: 7,
            day: "Monday",
            time_slot: "7:00 AM - 10:00 AM",
            mode: course.mode || "online",
          },
          {
            ...course,
            type: "Laboratory",
            duration: labDuration,
            institute_id: instituteId,
            start_hour: 13,
            day: "Monday",
            time_slot: "1:00 PM - 4:00 PM",
            mode: "face to face",
          },
        ];
      } else {
        payload = [
          {
            ...course,
            duration: lectureDuration || labDuration,
            institute_id: instituteId,
            start_hour: 7,
            day: "Monday",
            time_slot: "7:00 AM - 10:00 AM",
            mode: course.mode || "face to face",
          },
        ];
      }

      // 🔹 Instead of sending to backend, just emit to parent
      this.$emit("open-edit-schedule", payload);

      // Reset modal
      this.closeAssignModal();
    },

    async fetchUser() {
      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/auth/me`,
          { withCredentials: true },
        );
        this.user = res.data || {};
      } catch {
        this.user = {};
      }
    },

    getSetName(classId) {
      const section = this.store.sections.find(
        (sec) => sec.class_id === classId,
      );
      return section ? section.set_name : classId;
    },

    getInstituteId(programId) {
      const program = this.store.programs.find(
        (p) => p.program_id === programId,
      );
      return program ? program.institute_id : null;
    },

    getFacultyName(facultyId) {
      const user = this.store.rawusers?.find((u) => u.id === facultyId);
      if (!user) return "Unknown Faculty";
      return [user.first_name, user.middle_name, user.last_name]
        .filter(Boolean)
        .join(" ");
    },
  },

  async mounted() {
    await this.fetchUser();
    await this.store.fetchUnscheduledMeetings();
    await this.store.fetchFinalSchedules();
    await this.store.fetchClassSections();
    await this.store.fetchRawUsers();
  },
};
</script>
