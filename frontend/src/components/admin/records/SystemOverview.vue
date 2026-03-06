<template>
  <div class="px-2 mt-2">
    <!-- Header -->
    <div class="flex justify-between items-start mb-4">
      <h1 class="font-semibold tracking-wide text-sm px-1">System Overview</h1>
    </div>

    <!-- Faculty with Expertise Section -->
    <div class="mb-6">
      <div class="border rounded-xl bg-white shadow-sm overflow-hidden">
        <div
          class="bg-defaultGreen text-white px-4 py-3 flex justify-between items-center"
        >
          <h2 class="font-bold text-lg">Faculty & Expertise</h2>
          <span
            class="text-sm bg-white text-defaultGreen px-3 py-1 rounded-full"
          >
            {{ faculty.length }} Faculty
          </span>
        </div>

        <!-- Search and Filter -->
        <div class="p-4 bg-gray-50 border-b">
          <div class="flex gap-3">
            <input
              v-model="facultySearch"
              type="text"
              placeholder="Search faculty by name..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <select
              v-model="selectedInstitute"
              class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="">All Institutes</option>
              <option
                v-for="inst in uniqueInstitutes"
                :key="inst"
                :value="inst"
              >
                {{ inst }}
              </option>
            </select>
          </div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="min-w-full text-sm">
            <thead class="bg-gray-100 border-b">
              <tr>
                <th class="px-4 py-3 text-left font-semibold">#</th>
                <th class="px-4 py-3 text-left font-semibold">Faculty Name</th>
                <th class="px-4 py-3 text-left font-semibold">Institute</th>
                <th class="px-4 py-3 text-left font-semibold">Program</th>
                <th class="px-4 py-3 text-left font-semibold">Role</th>
                <th class="px-4 py-3 text-left font-semibold">
                  Course Expertise
                </th>
                <th class="px-4 py-3 text-left font-semibold">
                  Schedule Assignments
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(fac, index) in paginatedFaculty"
                :key="fac.id"
                class="border-b hover:bg-green-50 transition-colors"
              >
                <td class="px-4 py-3">{{ facultyStartIndex + index }}</td>
                <td class="px-4 py-3 font-semibold text-gray-800">
                  {{ getFacultyFullName(fac) }}
                </td>
                <td class="px-4 py-3">
                  {{ fac.institute?.institute_name || "N/A" }}
                </td>
                <td class="px-4 py-3">
                  {{ fac.program?.program_name || "N/A" }}
                </td>
                <td class="px-4 py-3">
                  <span
                    class="px-2 py-1 rounded-full text-xs bg-green-100 text-green-800"
                  >
                    Faculty
                  </span>
                </td>
                <td class="px-4 py-3">
                  <div
                    v-if="fac.expertise && fac.expertise.length > 0"
                    class="flex flex-wrap gap-1"
                  >
                    <span
                      v-for="exp in fac.expertise.slice(0, 3)"
                      :key="exp.id"
                      class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-md"
                    >
                      {{ exp.course?.course_code || "N/A" }}
                    </span>
                    <span
                      v-if="fac.expertise.length > 3"
                      class="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-md"
                    >
                      +{{ fac.expertise.length - 3 }} more
                    </span>
                  </div>
                  <span v-else class="text-gray-400 text-xs"
                    >No expertise listed</span
                  >
                </td>
                <td class="px-4 py-3">
                  <div v-if="getFacultyAssignments(fac).length > 0">
                    <button
                      @click="showFacultyCourses(fac)"
                      class="px-3 py-1 bg-green-600 text-white text-xs rounded-lg hover:bg-defaultGreen transition-colors"
                    >
                      View Courses ({{ getFacultyAssignments(fac).length }})
                    </button>
                  </div>
                  <span v-else class="text-gray-400 text-xs"
                    >No courses assigned</span
                  >
                </td>
              </tr>
              <tr v-if="filteredFaculty.length === 0">
                <td colspan="7" class="px-4 py-8 text-center text-gray-500">
                  No faculty found
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div
          v-if="filteredFaculty.length > 0"
          class="px-4 py-3 bg-gray-50 border-t"
        >
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">
              Showing {{ facultyStartIndex }} to {{ facultyEndIndex }} of
              {{ filteredFaculty.length }} entries
            </span>
            <div class="flex gap-2">
              <button
                @click="facultyPage = Math.max(1, facultyPage - 1)"
                :disabled="facultyPage === 1"
                class="px-3 py-1 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
              >
                Previous
              </button>
              <button
                v-for="page in facultyTotalPages"
                :key="page"
                @click="facultyPage = page"
                :class="
                  facultyPage === page
                    ? 'bg-defaultGreen text-white'
                    : 'bg-white hover:bg-gray-100'
                "
                class="px-3 py-1 border rounded-lg"
              >
                {{ page }}
              </button>
              <button
                @click="
                  facultyPage = Math.min(facultyTotalPages, facultyPage + 1)
                "
                :disabled="facultyPage === facultyTotalPages"
                class="px-3 py-1 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Rooms Section -->
    <div class="mb-6">
      <div class="border rounded-xl bg-white shadow-sm overflow-hidden">
        <div
          class="bg-blue-600 text-white px-4 py-3 flex justify-between items-center"
        >
          <h2 class="font-bold text-lg">Available Rooms</h2>
          <span class="text-sm bg-white text-blue-600 px-3 py-1 rounded-full">
            {{ rooms.length }} Rooms
          </span>
        </div>

        <!-- Search -->
        <div class="p-4 bg-gray-50 border-b">
          <input
            v-model="roomSearch"
            type="text"
            placeholder="Search rooms by name..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="min-w-full text-sm">
            <thead class="bg-gray-100 border-b">
              <tr>
                <th class="px-4 py-3 text-left font-semibold">#</th>
                <th class="px-4 py-3 text-left font-semibold">Room Name</th>
                <th class="px-4 py-3 text-left font-semibold">Room Type</th>
                <th class="px-4 py-3 text-left font-semibold">Building</th>
                <th class="px-4 py-3 text-center font-semibold">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(room, index) in filteredRooms"
                :key="room.room_id"
                class="border-b hover:bg-blue-50 transition-colors"
              >
                <td class="px-4 py-3">{{ index + 1 }}</td>
                <td class="px-4 py-3 font-semibold text-gray-800">
                  {{ room.room_name }}
                </td>
                <td class="px-4 py-3">
                  <span
                    class="px-2 py-1 rounded-full text-xs"
                    :class="
                      room.room_type === 'Lecture'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-orange-100 text-orange-800'
                    "
                  >
                    {{ room.room_type || "N/A" }}
                  </span>
                </td>
                <td class="px-4 py-3">{{ room.room_building || "N/A" }}</td>
                <td class="px-4 py-3 text-center">
                  <span
                    class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full"
                  >
                    Available
                  </span>
                </td>
              </tr>
              <tr v-if="filteredRooms.length === 0">
                <td colspan="5" class="px-4 py-8 text-center text-gray-500">
                  No rooms found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Classes with Courses Section -->
    <div class="mb-6">
      <div class="border rounded-xl bg-white shadow-sm overflow-hidden">
        <div
          class="bg-purple-600 text-white px-4 py-3 flex justify-between items-center"
        >
          <h2 class="font-bold text-lg">Classes & Assigned Courses</h2>
          <span class="text-sm bg-white text-purple-600 px-3 py-1 rounded-full">
            {{ classes.length }} Classes
          </span>
        </div>

        <!-- Search and Filter -->
        <div class="p-4 bg-gray-50 border-b">
          <div class="flex gap-3">
            <input
              v-model="classSearch"
              type="text"
              placeholder="Search classes..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
            <select
              v-model="selectedProgram"
              class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">All Programs</option>
              <option v-for="prog in uniquePrograms" :key="prog" :value="prog">
                {{ prog }}
              </option>
            </select>
          </div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="min-w-full text-sm">
            <thead class="bg-gray-100 border-b">
              <tr>
                <th class="px-4 py-3 text-left font-semibold">#</th>
                <th class="px-4 py-3 text-left font-semibold">Class/Section</th>
                <th class="px-4 py-3 text-left font-semibold">Program</th>
                <th class="px-4 py-3 text-center font-semibold">Class Size</th>
                <th class="px-4 py-3 text-left font-semibold">School Year</th>
                <th class="px-4 py-3 text-left font-semibold">
                  Assigned Courses
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(cls, index) in paginatedClasses"
                :key="cls.class_id"
                class="border-b hover:bg-purple-50 transition-colors"
              >
                <td class="px-4 py-3">{{ classStartIndex + index }}</td>
                <td class="px-4 py-3 font-semibold text-gray-800">
                  {{ cls.set_name }}
                </td>
                <td class="px-4 py-3">
                  {{ cls.program?.program_name || "N/A" }}
                </td>
                <td class="px-4 py-3 text-center">
                  <span
                    class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                  >
                    {{ cls.class_size }} students
                  </span>
                </td>
                <td class="px-4 py-3">
                  {{ cls.schoolYear?.school_year_name || "N/A" }}
                </td>
                <td class="px-4 py-3">
                  <button
                    @click="showClassCourses(cls)"
                    class="px-3 py-1 bg-purple-600 text-white text-xs rounded-lg hover:bg-purple-700 transition-colors"
                  >
                    View Courses
                  </button>
                </td>
              </tr>
              <tr v-if="filteredClasses.length === 0">
                <td colspan="6" class="px-4 py-8 text-center text-gray-500">
                  No classes found
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div
          v-if="filteredClasses.length > 0"
          class="px-4 py-3 bg-gray-50 border-t"
        >
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">
              Showing {{ classStartIndex }} to {{ classEndIndex }} of
              {{ filteredClasses.length }} entries
            </span>
            <div class="flex gap-2">
              <button
                @click="classPage = Math.max(1, classPage - 1)"
                :disabled="classPage === 1"
                class="px-3 py-1 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
              >
                Previous
              </button>
              <button
                v-for="page in classTotalPages"
                :key="page"
                @click="classPage = page"
                :class="
                  classPage === page
                    ? 'bg-purple-600 text-white'
                    : 'bg-white hover:bg-gray-100'
                "
                class="px-3 py-1 border rounded-lg"
              >
                {{ page }}
              </button>
              <button
                @click="classPage = Math.min(classTotalPages, classPage + 1)"
                :disabled="classPage === classTotalPages"
                class="px-3 py-1 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Course Details Modal -->
    <div
      v-if="showCoursesModal"
      class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center"
      @click.self="closeCoursesModal"
    >
      <div
        class="bg-white rounded-xl shadow-2xl w-[800px] max-h-[80vh] overflow-y-auto"
      >
        <div
          class="bg-purple-600 text-white px-6 py-4 flex justify-between items-center sticky top-0"
        >
          <h3 class="font-bold text-lg">
            Courses for {{ selectedClass?.set_name }}
          </h3>
          <button
            @click="closeCoursesModal"
            class="text-white hover:text-gray-200"
          >
            <icon name="close" class="w-6 h-6" />
          </button>
        </div>

        <div class="p-6">
          <div v-if="classCourses.length > 0" class="space-y-3">
            <div
              v-for="(course, index) in classCourses"
              :key="course.id"
              class="p-4 border border-gray-200 rounded-lg hover:border-purple-400 transition-colors"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <p class="font-bold text-gray-800">
                    {{ index + 1 }}. {{ course.course?.course_code }}
                  </p>
                  <p class="text-sm text-gray-600 mt-1">
                    {{ course.course?.course_description }}
                  </p>
                  <div class="mt-2 flex gap-4 text-xs text-gray-500">
                    <span
                      >Year Level:
                      {{ getYearLevelLabel(course.year_level) }}</span
                    >
                    <span>Lec: {{ course.course?.course_lec || 0 }} hrs</span>
                    <span>Lab: {{ course.course?.course_lab || 0 }} hrs</span>
                    <span>Units: {{ course.course?.course_credit || 0 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            <icon
              name="question"
              class="w-16 h-16 text-gray-300 mx-auto mb-4"
            />
            <p>No courses assigned to this class yet.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Faculty Courses Modal -->
    <div
      v-if="showFacultyCoursesModal"
      class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center"
      @click.self="closeFacultyCoursesModal"
    >
      <div
        class="bg-white rounded-xl shadow-2xl w-[900px] max-h-[80vh] overflow-y-auto"
      >
        <div
          class="bg-green-600 text-white px-6 py-4 flex justify-between items-center sticky top-0"
        >
          <h3 class="font-bold text-lg">
            Faculty Details:
            {{ selectedFaculty ? getFacultyFullName(selectedFaculty) : "" }}
          </h3>
          <button
            @click="closeFacultyCoursesModal"
            class="text-white hover:text-gray-200"
          >
            <icon name="close" class="w-6 h-6" />
          </button>
        </div>

        <div class="p-6">
          <!-- Course Expertise Section -->
          <div class="mb-6">
            <h4
              class="font-bold text-md text-gray-800 mb-3 flex items-center gap-2"
            >
              <span
                class="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs"
                >EXPERTISE</span
              >
              Courses Faculty Can Teach
            </h4>
            <div
              v-if="
                selectedFaculty?.expertise &&
                selectedFaculty.expertise.length > 0
              "
              class="flex flex-wrap gap-2"
            >
              <span
                v-for="exp in selectedFaculty.expertise"
                :key="exp.id"
                class="px-3 py-2 bg-purple-100 text-purple-800 text-sm rounded-lg border border-purple-200"
              >
                {{ exp.course?.course_code }} -
                {{ exp.course?.course_description }}
              </span>
            </div>
            <div v-else class="text-gray-500 text-sm italic">
              No course expertise registered
            </div>
          </div>

          <!-- Schedule Assignments Section -->
          <div>
            <h4
              class="font-bold text-md text-gray-800 mb-3 flex items-center gap-2"
            >
              <span
                class="px-2 py-1 bg-green-100 text-green-800 rounded text-xs"
                >SCHEDULED</span
              >
              Current Teaching Schedule
            </h4>
            <div v-if="facultyCourses.length > 0" class="space-y-3">
              <div
                v-for="(assignment, index) in facultyCourses"
                :key="index"
                class="p-4 border border-gray-200 rounded-lg hover:border-green-400 transition-colors bg-green-50"
              >
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <p class="font-bold text-gray-800 text-base">
                      {{ index + 1 }}. {{ assignment.course_name }}
                    </p>
                    <div
                      class="mt-2 grid grid-cols-2 gap-2 text-sm text-gray-600"
                    >
                      <div><strong>Type:</strong> {{ assignment.type }}</div>
                      <div>
                        <strong>Year Level & Section:</strong>
                        {{ getYearLevelFromSet(assignment.set) }} -
                        {{ assignment.set }}
                      </div>
                      <div><strong>Day:</strong> {{ assignment.day }}</div>
                      <div>
                        <strong>Time:</strong> {{ assignment.start_hour }}:00 -
                        {{ assignment.end_hour }}:00
                      </div>
                      <div>
                        <strong>Room:</strong> {{ assignment.room_name }}
                      </div>
                      <div>
                        <strong>Duration:</strong>
                        {{ assignment.end_hour - assignment.start_hour }}
                        hour(s)
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              <icon
                name="question"
                class="w-16 h-16 text-gray-300 mx-auto mb-4"
              />
              <p>No courses assigned in the generated schedule yet.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import axios from "axios";
import { toast } from "vue3-toastify";

export default {
  name: "SystemOverview",
  components: { icon },
  data() {
    return {
      faculty: [],
      rooms: [],
      classes: [],
      classCourses: [],
      selectedClass: null,
      showCoursesModal: false,

      // Faculty courses
      generatedSchedule: [],
      facultyCourses: [],
      selectedFaculty: null,
      showFacultyCoursesModal: false,

      // Search and filters
      facultySearch: "",
      roomSearch: "",
      classSearch: "",
      selectedInstitute: "",
      selectedProgram: "",

      // Pagination
      facultyPage: 1,
      classPage: 1,
      itemsPerPage: 10,

      loading: true,
    };
  },
  computed: {
    // Faculty filtering and pagination
    filteredFaculty() {
      let result = this.faculty;

      if (this.facultySearch) {
        const query = this.facultySearch.toLowerCase();
        result = result.filter((f) => {
          const fullName = this.getFacultyFullName(f).toLowerCase();
          return fullName.includes(query);
        });
      }

      if (this.selectedInstitute) {
        result = result.filter(
          (f) => f.institute?.institute_name === this.selectedInstitute,
        );
      }

      return result;
    },
    paginatedFaculty() {
      const start = (this.facultyPage - 1) * this.itemsPerPage;
      return this.filteredFaculty.slice(start, start + this.itemsPerPage);
    },
    facultyTotalPages() {
      return Math.ceil(this.filteredFaculty.length / this.itemsPerPage) || 1;
    },
    facultyStartIndex() {
      return this.filteredFaculty.length === 0
        ? 0
        : (this.facultyPage - 1) * this.itemsPerPage + 1;
    },
    facultyEndIndex() {
      const end = this.facultyPage * this.itemsPerPage;
      return Math.min(end, this.filteredFaculty.length);
    },
    uniqueInstitutes() {
      const institutes = this.faculty
        .map((f) => f.institute?.institute_name)
        .filter(Boolean);
      return [...new Set(institutes)];
    },

    // Rooms filtering
    filteredRooms() {
      if (!this.roomSearch) return this.rooms;

      const query = this.roomSearch.toLowerCase();
      return this.rooms.filter((r) =>
        r.room_name?.toLowerCase().includes(query),
      );
    },

    // Classes filtering and pagination
    filteredClasses() {
      let result = this.classes;

      if (this.classSearch) {
        const query = this.classSearch.toLowerCase();
        result = result.filter((c) =>
          c.set_name?.toLowerCase().includes(query),
        );
      }

      if (this.selectedProgram) {
        result = result.filter(
          (c) => c.program?.program_name === this.selectedProgram,
        );
      }

      return result;
    },
    paginatedClasses() {
      const start = (this.classPage - 1) * this.itemsPerPage;
      return this.filteredClasses.slice(start, start + this.itemsPerPage);
    },
    classTotalPages() {
      return Math.ceil(this.filteredClasses.length / this.itemsPerPage) || 1;
    },
    classStartIndex() {
      return this.filteredClasses.length === 0
        ? 0
        : (this.classPage - 1) * this.itemsPerPage + 1;
    },
    classEndIndex() {
      const end = this.classPage * this.itemsPerPage;
      return Math.min(end, this.filteredClasses.length);
    },
    uniquePrograms() {
      const programs = this.classes
        .map((c) => c.program?.program_name)
        .filter(Boolean);
      return [...new Set(programs)];
    },
  },
  methods: {
    async loadFaculty() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/users/get-users",
        );
        // Filter only users with role 'faculty'
        this.faculty = response.data.filter((user) => user.role === "Faculty");
      } catch (error) {
        console.error("Failed to load faculty:", error);
        toast.error("Failed to load faculty data");
      }
    },
    async loadRooms() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/rooms/get-rooms",
        );
        this.rooms = response.data;
      } catch (error) {
        console.error("Failed to load rooms:", error);
        toast.error("Failed to load rooms data");
      }
    },
    async loadClasses() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/class/get-classes",
        );
        this.classes = response.data;
      } catch (error) {
        console.error("Failed to load classes:", error);
        toast.error("Failed to load classes data");
      }
    },
    async loadGeneratedSchedule() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/generated-scheduled/load",
        );

        if (response.data.success && response.data.data) {
          // Extract all schedules from the response
          const allSchedules = Object.values(response.data.data).flatMap(
            (set) => set.best_schedule || [],
          );
          this.generatedSchedule = allSchedules;
        }
      } catch (error) {
        console.error("Failed to load generated schedule:", error);
        // Don't show error toast as schedule might not exist yet
        this.generatedSchedule = [];
      }
    },
    async showClassCourses(cls) {
      this.selectedClass = cls;
      this.showCoursesModal = true;

      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/program-year-courses/get-by-program-and-school-year",
          {
            params: {
              program_id: cls.program_id,
              school_year_id: cls.school_year_id,
            },
          },
        );

        // Filter by year level extracted from set_name
        const yearLevel = this.extractYearLevel(cls.set_name);
        if (yearLevel) {
          this.classCourses = response.data.filter(
            (c) => c.year_level === yearLevel,
          );
        } else {
          this.classCourses = response.data;
        }
      } catch (error) {
        console.error("Failed to load class courses:", error);
        this.classCourses = [];
      }
    },
    closeCoursesModal() {
      this.showCoursesModal = false;
      this.selectedClass = null;
      this.classCourses = [];
    },
    getFacultyAssignments(faculty) {
      if (!this.generatedSchedule || this.generatedSchedule.length === 0) {
        return [];
      }

      const facultyFullName = this.getFacultyFullName(faculty);

      // Filter schedule by faculty name
      const assignments = this.generatedSchedule.filter(
        (item) => item.faculty_name === facultyFullName,
      );

      return assignments;
    },
    showFacultyCourses(faculty) {
      this.selectedFaculty = faculty;
      this.facultyCourses = this.getFacultyAssignments(faculty);
      this.showFacultyCoursesModal = true;
    },
    closeFacultyCoursesModal() {
      this.showFacultyCoursesModal = false;
      this.selectedFaculty = null;
      this.facultyCourses = [];
    },
    getFacultyFullName(faculty) {
      const parts = [faculty.first_name, faculty.last_name].filter(Boolean);
      return parts.join(" ");
    },
    getYearLevelLabel(level) {
      const labels = {
        1: "1st Year",
        2: "2nd Year",
        3: "3rd Year",
        4: "4th Year",
      };
      return labels[level] || `Year ${level}`;
    },
    extractYearLevel(setName) {
      if (!setName) return null;
      const match = setName.match(/(\d+)(?:st|nd|rd|th)\s*year/i);
      return match ? parseInt(match[1]) : null;
    },
    getYearLevelFromSet(setLetter) {
      // Find the class that matches this set letter
      const matchedClass = this.classes.find((cls) => {
        // Extract the last character(s) from set_name as the section letter
        const setNameParts = cls.set_name?.match(/([A-Z])$/i);
        return setNameParts && setNameParts[1] === setLetter;
      });

      if (matchedClass && matchedClass.set_name) {
        const yearLevel = this.extractYearLevel(matchedClass.set_name);
        if (yearLevel) {
          return this.getYearLevelLabel(yearLevel);
        }
      }

      // Fallback: Return generic text if no match found
      return "Unknown Year";
    },
  },
  async mounted() {
    this.loading = true;
    await Promise.all([
      this.loadFaculty(),
      this.loadRooms(),
      this.loadClasses(),
      this.loadGeneratedSchedule(),
    ]);
    this.loading = false;
  },
};
</script>

<style scoped>
/* Custom scrollbar for modal */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
