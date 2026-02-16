<template>
  <div class="max-w-screen min-h-screen bg-gray-100 rounded-md">
    <div class="w-full h-auto justify-center items-center">
      <div class="bg-white w-full h-screen rounded-md">
        <div class="w-full h-auto">
          <!-- Semester Selection + Download Button -->
          <div class="flex justify-between mb-4 flex-wrap gap-2 items-center">
            <!-- Semester Buttons -->
            <div class="flex gap-2">
              <button
                @click="selectSemester(1)"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition',
                  selectedSemester === 1
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-blue-600 border border-blue-600 hover:bg-blue-600 hover:text-white',
                ]"
              >
                First Semester
              </button>
              <button
                @click="selectSemester(2)"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition',
                  selectedSemester === 2
                    ? 'bg-green-600 text-white'
                    : 'bg-white text-defaultGreen border border-green-600 hover:bg-green-600 hover:text-white',
                ]"
              >
                Second Semester
              </button>
            </div>

            <!-- Download Button -->
            <router-link
              v-if="authenticatedEmployeeId"
              :to="{
                name: 'view-pdf-faculty-loadings',
                params: { id: authenticatedEmployeeId },
                query: { course_semester: selectedSemester },
              }"
              class="flex items-center gap-2 px-4 py-2 border text-blue-600 border-blue-600 rounded-xl hover:bg-blue-700 hover:text-white hover:shadow-lg cursor-pointer transition duration-200 w-auto"
            >
              <div
                class="p-1 bg-blue-600 bg-opacity-20 rounded-full flex items-center justify-center"
              >
                <icon :name="'download'" class="w-4 h-4" />
              </div>
              <span class="font-medium text-sm">Show Download Previews</span>
            </router-link>
          </div>

          <!-- Header -->
          <div
            class="flex flex-col items-center text-center border-b pb-4 mb-4"
          >
            <img
              src="@/assets/img/dnsc_logo.png"
              alt="School Logo"
              class="w-20 h-20 object-contain mb-2"
            />
            <h1
              class="text-2xl font-extrabold text-gray-800 uppercase tracking-wide"
            >
              Davao del Norte State College
            </h1>
            <p class="text-sm text-gray-600 mt-1">
              Panabo City, Davao del Norte
            </p>
          </div>

          <!-- Content -->
          <div class="w-full h-[75vh] overflow-y-auto">
            <div class="text-center mt-5">
              <h1 class="font-bold text-lg">TEACHER'S LOAD</h1>
              <p>
                {{ semesterName }} Semester/Term : School Year
                {{ schoolYears }}
              </p>
            </div>

            <!-- Table or Message -->
            <div v-if="filteredFacultyLoads.length > 0">
              <table
                class="min-w-full table-auto border border-gray-300 shadow-sm rounded-md overflow-hidden text-sm mt-5"
              >
                <thead
                  class="bg-gray-100 text-gray-700 uppercase text-xs font-semibold"
                >
                  <tr>
                    <th class="px-4 py-3 border">Offer Code</th>
                    <th class="px-4 py-2 border">Code</th>
                    <th class="px-4 py-2 border">Description</th>
                    <th class="px-4 py-2 border">Lec</th>
                    <th class="px-4 py-2 border">Lab</th>
                    <th class="px-4 py-2 border">Credet <br />(Units)</th>
                    <th class="px-4 py-2 border">Requisition</th>
                    <th class="px-4 py-2 border">Schedule</th>
                  </tr>
                </thead>
                <tbody class="text-gray-800">
                  <tr
                    class="hover:bg-gray-50"
                    v-for="load in groupedFacultyLoads"
                    :key="load.schedule_id"
                  >
                    <td class="px-4 py-3 border text-center">
                      {{ load.course?.course_offer_code }}
                    </td>
                    <td class="px-4 py-2 border">
                      {{ load.course?.course_code }}
                    </td>
                    <td class="px-4 py-2 border">
                      {{ load.course?.course_description }}
                    </td>
                    <td class="px-4 py-2 border text-center">
                      {{ load.course?.course_lec }}
                    </td>
                    <td class="px-4 py-2 border text-center">
                      {{ load.course?.course_lab }}
                    </td>
                    <td class="px-4 py-2 border text-center">
                      {{ load.course?.course_lec + load.course?.course_lab }}
                    </td>
                    <td class="px-4 py-2 border text-center">
                      {{ load.course?.course_requisite }}
                    </td>
                    <td class="px-4 py-2 border text-center">
                      {{ load.schedule_days }} |
                      {{ formatTime(load.time_start) }} -
                      {{ formatTime(load.time_end) }} | {{ load.room?.room_name
                      }}{{ load.room?.room_number }}
                    </td>
                  </tr>

                  <tr class="font-semibold bg-gray-100 text-center">
                    <td colspan="5" class="px-4 py-2 border text-right">
                      TOTAL UNITS
                    </td>
                    <td class="px-4 py-2 border">{{ totalUnits }}</td>
                    <td class="px-4 py-2 border"></td>
                    <td class="px-4 py-2 border"></td>
                  </tr>
                </tbody>
              </table>

              <div class="flex justify-between items-start w-full mt-8 px-10">
                <div
                  class="grid grid-cols-2 gap-x-10 gap-y-2 text-sm text-gray-500"
                >
                  <div>Total Preparation: 3</div>
                  <div>Overload Units: 3</div>
                  <div>Minor Subjects: 3</div>
                  <div>Major Subjects: 3</div>
                </div>
                <div class="text-center text-sm">
                  <p class="underline font-bold">{{ instructorName }}</p>
                  <p>Instructor</p>
                </div>
              </div>

              <div class="mt-10 text-right px-10">
                <p class="text-sm text-gray-500">Generated by: Admin</p>
                <p class="text-sm text-gray-500">
                  Date: {{ new Date().toLocaleDateString() }}
                </p>
              </div>
            </div>

            <div v-else class="text-center mt-20 text-gray-500 text-sm">
              No schedule data available for this instructor.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      selectedSemester: 1,
      authenticatedEmployeeId: 1001,
      instructorName: "Prof. Remarjohn Sibug",
      schoolYears: "2025-2026",
      // Static faculty loads (sample data)
      filteredFacultyLoads: [
        {
          schedule_id: 1,
          course: {
            course_offer_code: "CSC101",
            course_code: "CS101",
            course_description: "Introduction to Computer Science",
            course_lec: 3,
            course_lab: 0,
            course_requisite: "None",
          },
          schedule_days: "Mon/Wed",
          time_start: "08:00",
          time_end: "09:30",
          room: {
            room_name: "Room",
            room_number: "101",
          },
        },
        {
          schedule_id: 2,
          course: {
            course_offer_code: "CSC202",
            course_code: "CS202",
            course_description: "Data Structures",
            course_lec: 2,
            course_lab: 1,
            course_requisite: "CS101",
          },
          schedule_days: "Tue/Thu",
          time_start: "10:00",
          time_end: "11:30",
          room: {
            room_name: "Lab",
            room_number: "202",
          },
        },
      ],
    };
  },
  computed: {
    groupedFacultyLoads() {
      return this.filteredFacultyLoads;
    },
    totalUnits() {
      return this.filteredFacultyLoads.reduce((total, load) => {
        const lec = load.course?.course_lec || 0;
        const lab = load.course?.course_lab || 0;
        return total + lec + lab;
      }, 0);
    },
    semesterName() {
      return this.selectedSemester === 1 ? "First" : "Second";
    },
  },
  methods: {
    selectSemester(sem) {
      this.selectedSemester = sem;
      // If switching semesters, you can update filteredFacultyLoads here with new static data
    },
    formatTime(time) {
      // Simple formatter for 24hr to 12hr format
      const [hour, minute] = time.split(":");
      const h = parseInt(hour);
      const suffix = h >= 12 ? "PM" : "AM";
      const formattedHour = h % 12 || 12;
      return `${formattedHour}:${minute} ${suffix}`;
    },
  },
};
</script>

<style scoped></style>
