<template>
  <div>
    <!-- Table / Auto Generation Button -->
    <div v-if="isTable" class="mb-6">
      <div class="flex justify-between items-center">
        <div class="text-sm text-gray-600 mt-4 font-medium">
          Pages / Faculty Loads
        </div>

        <div class="flex gap-3">
          <!-- Auto Generation -->
          <div
            @click="fetchSchedule"
            class="group flex items-center gap-2 px-4 py-2 border border-green-600 text-green-600 hover:bg-green-600 hover:text-white rounded-xl shadow-sm cursor-pointer transition"
          >
            <div
              class="p-1 bg-green-100 rounded-full flex items-center justify-center group-hover:bg-white transition"
            >
              <icon
                :name="'arrow-path'"
                class="w-4 h-4 text-green-600 group-hover:text-green-600"
              />
            </div>
            <span class="font-medium text-sm">Auto Generation</span>
          </div>

          <!-- Save this schedule -->
          <div
            @click="saveScheduled"
            class="group flex items-center gap-2 px-4 py-2 border border-green-600 text-green-600 hover:bg-green-600 hover:text-white rounded-xl shadow-sm cursor-pointer transition"
          >
            <div
              class="p-1 bg-green-100 rounded-full flex items-center justify-center group-hover:bg-white transition"
            >
              <icon
                :name="'circle-check'"
                class="w-4 h-4 text-green-600 group-hover:text-green-600"
              />
            </div>
            <span class="font-medium text-sm">Save this schedule</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div
      v-if="loading"
      class="fixed inset-0 flex items-center justify-center bg-black/40 z-50"
    >
      <div
        class="space-y-5 flex flex-col items-center justify-center p-5 bg-white rounded-3xl shadow-lg"
      >
        <!-- Animated dots instead of image -->
        <div class="flex space-x-2">
          <span class="w-3 h-3 bg-green-500 rounded-full bounce-delay-0"></span>
          <span
            class="w-3 h-3 bg-green-500 rounded-full bounce-delay-200"
          ></span>
          <span
            class="w-3 h-3 bg-green-500 rounded-full bounce-delay-400"
          ></span>
        </div>

        <!-- Progress bar -->
        <!-- <div class="w-64 bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            class="bg-green-500 h-3 rounded-full transition-all duration-300"
            :style="{ width: progress + '%' }"
          ></div>
        </div> -->

        <div class="text-gray-700 font-medium">
          Generating Schedule... {{ Math.floor(progress) }}%
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center text-red-600 font-medium py-6">
      {{ error }}
    </div>

    <!-- Schedule -->
    <div
      v-else
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 h-[80vh]"
    >
      <div
        v-for="(slots, instructor) in groupedSchedule"
        :key="instructor"
        class="bg-white rounded-2xl shadow-md overflow-hidden border border-gray-200 flex flex-col"
      >
        <!-- Instructor Header -->
        <div
          class="bg-defaultGreen text-white text-center py-3 font-semibold text-lg"
        >
          {{ instructor }}
        </div>

        <!-- Scrollable Table -->
        <div class="overflow-x-auto overflow-y-auto flex-1">
          <table class="w-full text-sm text-left border-collapse">
            <thead class="sticky top-0 bg-gray-100 z-10">
              <tr class="text-gray-700 text-sm">
                <th class="px-4 py-2 border border-gray-200">Time</th>
                <th
                  v-for="day in days"
                  :key="day"
                  class="px-4 py-2 border border-gray-200 text-center"
                >
                  {{ day }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="slot in timeSlots"
                :key="slot.start + slot.end"
                class="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition"
              >
                <td
                  class="px-4 py-3 border border-gray-200 font-medium text-gray-700"
                >
                  {{ slot.start }} - {{ slot.end }}
                </td>
                <td
                  v-for="day in days"
                  :key="day"
                  class="px-4 py-3 border border-gray-200 text-center align-top"
                >
                  <div
                    v-for="item in getScheduleForCell(slot, day, instructor)"
                    :key="item.course_name + item.start_hour + item.room_name"
                    class="mb-2 p-2 bg-green-50 border border-green-200 rounded-lg text-xs text-gray-800 shadow-sm"
                  >
                    <p class="font-semibold text-green-700">
                      {{ item.course_name }} ({{ item.type }})
                    </p>
                    <p class="text-gray-600">Room: {{ item.room_name }}</p>
                    <!-- <p class="text-gray-600">
                      Faculty: {{ item.faculty_name }}
                    </p> -->
                    <p class="text-gray-600">Set: {{ item.set }}</p>

                    <!-- Conflict Button -->
                    <button
                      v-if="item.conflict"
                      @click="openConflictModal(item)"
                      class="mt-2 px-2 py-1 text-xs rounded bg-red-100 text-red-600 hover:bg-red-200 transition"
                    >
                      ⚠ View Conflict
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Conflict Modal -->
    <div
      v-if="showConflictModal"
      class="fixed inset-0 flex items-center justify-center bg-black/50 z-50"
    >
      <div class="bg-white w-full max-w-lg rounded-2xl shadow-xl p-6 relative">
        <!-- Close Button -->
        <button
          @click="closeConflictModal"
          class="absolute top-3 right-3 text-gray-400 hover:text-gray-600"
        >
          ✖
        </button>

        <h2 class="text-lg font-semibold text-red-600 mb-4">
          ⚠ Schedule Conflict Detected
        </h2>

        <div class="space-y-3 max-h-80 overflow-y-auto pr-2">
          <div
            v-for="conflict in selectedConflict.conflicts"
            :key="conflict.course_name + conflict.room_name"
            class="p-3 bg-red-50 border border-red-200 rounded-lg text-sm"
          >
            <p class="font-semibold text-red-700">
              {{ conflict.course_name }} ({{ conflict.type }})
            </p>
            <p class="text-gray-600">
              🕒 {{ conflict.start_hour }} - {{ conflict.end_hour }}
            </p>
            <p class="text-gray-600">📍 Room: {{ conflict.room_name }}</p>
            <p class="text-gray-600">👨‍🏫 Faculty: {{ conflict.faculty_name }}</p>
            <p class="text-gray-600">📌 Set: {{ conflict.set }}</p>
          </div>
        </div>

        <div class="mt-5 text-right">
          <button
            @click="closeConflictModal"
            class="px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import icon from "@/assets/icon.vue";
export default {
  name: "FacultySchedule",
  components: {
    icon,
  },
  data() {
    return {
      user: {},
      schedule: [],
      groupedSchedule: {},
      loading: false,
      error: null,
      isTable: true,
      days: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      timeSlots: [
        { start: "8:00 AM", end: "9:00 AM" },
        { start: "9:00 AM", end: "10:00 AM" },
        { start: "10:00 AM", end: "11:00 AM" },
        { start: "11:00 AM", end: "12:00 PM" },
        { start: "12:00 PM", end: "1:00 PM" },
        { start: "1:00 PM", end: "2:00 PM" },
        { start: "2:00 PM", end: "3:00 PM" },
        { start: "3:00 PM", end: "4:00 PM" },
        { start: "4:00 PM", end: "5:00 PM" },
      ],
      progress: 0,
      progressInterval: null,

      // Conflict modal state
      showConflictModal: false,
      selectedConflict: {},
    };
  },
  methods: {
    deduplicateSchedules(schedules) {
      const seen = new Set();
      return schedules.filter((s) => {
        const key = `${s.course_id}-${s.room_id}-${s.faculty_id}-${s.start_hour}-${s.end_hour}-${s.day}-${s.set}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    },

    async fetchSchedule() {
      this.loading = true;
      this.error = null;
      this.progress = 0;

      this.progressInterval = setInterval(() => {
        if (this.progress < 90) {
          this.progress += Math.random() * 10;
        }
      }, 200);

      try {
        const response = await axios.get(
          "http://localhost:8000/generated-scheduled/load"
        );

        if (response.data.success && response.data.data) {
          const allSchedules = Object.values(response.data.data).flatMap(
            (set) => set.best_schedule || []
          );

          // ✅ Deduplicate schedules before saving
          const dedupedSchedules = this.deduplicateSchedules(allSchedules);

          // ✅ Filter schedules by same institute as logged-in user
          const filteredSchedules = dedupedSchedules.filter(
            (s) => s.institute_id === this.user.institute_id
          );

          // detect conflicts only on filtered schedules
          const conflicts = this.detectConflicts(filteredSchedules);

          this.schedule = filteredSchedules;
          this.groupedSchedule = this.groupByInstructor(this.schedule);

          if (conflicts.length > 0) {
            this.selectedConflict = { conflicts };
            this.showConflictModal = true;
          }
        } else {
          this.error = "Invalid schedule format.";
        }
      } catch (err) {
        console.error(err);
        this.error = "Failed to fetch schedule.";
      } finally {
        clearInterval(this.progressInterval);
        this.progress = 100;
        setTimeout(() => {
          this.loading = false;
          this.progress = 0;
        }, 300);
      }
    },

    groupByInstructor(schedule) {
      return schedule.reduce((acc, item) => {
        const instructor = item.faculty_name || "Unknown";
        if (!acc[instructor]) acc[instructor] = [];
        acc[instructor].push(item);
        return acc;
      }, {});
    },

    getScheduleForCell(slot, day, instructor) {
      const instructorSlots = this.groupedSchedule[instructor] || [];
      const slotStart = this.timeToMinutes(slot.start);
      const slotEnd = this.timeToMinutes(slot.end);

      return instructorSlots.filter((item) => {
        if (!item.day || !item.start_hour || !item.end_hour) return false;
        const itemDay = item.day.slice(0, 3);
        const itemStart = this.convertToMinutes(item.start_hour);
        const itemEnd = this.convertToMinutes(item.end_hour);

        return slotStart < itemEnd && itemStart < slotEnd && itemDay === day;
      });
    },

    detectConflicts(schedule) {
      let conflicts = [];
      const seen = new Set();

      for (let i = 0; i < schedule.length; i++) {
        for (let j = i + 1; j < schedule.length; j++) {
          const a = schedule[i];
          const b = schedule[j];

          if (a.day === b.day) {
            const overlap =
              this.convertToMinutes(a.start_hour) <
                this.convertToMinutes(b.end_hour) &&
              this.convertToMinutes(b.start_hour) <
                this.convertToMinutes(a.end_hour);

            if (
              overlap &&
              (a.faculty_id === b.faculty_id || a.room_id === b.room_id)
            ) {
              const key = `${a.course_id}-${b.course_id}-${a.day}-${a.start_hour}-${a.end_hour}`;
              if (!seen.has(key)) {
                conflicts.push(a, b);
                seen.add(key);
              }
            }
          }
        }
      }

      return conflicts;
    },

    timeToMinutes(timeStr) {
      let [time, ampm] = timeStr.split(" ");
      let [h, m] = time.split(":").map(Number);
      if (ampm === "PM" && h !== 12) h += 12;
      if (ampm === "AM" && h === 12) h = 0;
      return h * 60 + m;
    },

    convertToMinutes(hour) {
      return Math.floor(hour) * 60 + Math.round((hour % 1) * 60);
    },

    // Conflict modal controls
    openConflictModal(item) {
      this.selectedConflict = item;
      this.showConflictModal = true;
    },
    closeConflictModal() {
      this.showConflictModal = false;
      this.selectedConflict = {};
    },

    async fetchUser() {
      try {
        const response = await axios.get("http://localhost:8000/auth/me", {
          withCredentials: true,
        });
        if (response.data) {
          this.user = response.data;
          console.log("Authenticated User:", this.user);
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },
  },
  async mounted() {
    await this.fetchUser(); // ✅ get user first
  },
};
</script>

<style scoped>
.container {
  padding: 20px;
  background: #f9fafb;
  min-height: 100vh;
}
.text-text {
  color: #4b5563;
}
.grid-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 20px;
}
.schedule-wrapper {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
.instructor-header {
  background: #147452;
  color: white;
  padding: 10px;
  font-size: 1.2rem;
  font-weight: bold;
  text-align: center;
}
.schedule-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0;
}
.schedule-table th,
.schedule-table td {
  border: 1px solid #d1d5db;
  padding: 6px;
  text-align: center;
  font-size: 0.9rem;
}
.schedule-table th {
  background: #f3f4f6;
  font-weight: 600;
}
.cell-item {
  margin-bottom: 4px;
}
.loading,
.error {
  text-align: center;
  font-size: 1.1rem;
}
.error {
  color: #dc2626;
}
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.35);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-content {
  width: 80%;
  max-width: 400px;
  text-align: center;
}

.progress-bar {
  width: 80%;
  height: 20px;
  background: #e5e7eb;
  border-radius: 10px;
  margin: 0 auto;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #4df58b;
  width: 0%;
  transition: width 0.2s ease;
}

.loading-text {
  margin-top: 8px;
  font-size: 0.95rem;
  color: #374151;
}
@keyframes bounce-custom {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}
.bounce-delay-0 {
  animation: bounce-custom 1s infinite;
}
.bounce-delay-200 {
  animation: bounce-custom 1s infinite;
  animation-delay: 0.5s;
}
.bounce-delay-400 {
  animation: bounce-custom 1s infinite;
  animation-delay: 0.4s;
}
</style>
