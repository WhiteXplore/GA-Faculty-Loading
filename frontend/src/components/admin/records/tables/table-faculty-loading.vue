<template>
  <div>
    <!-- Table / Auto Generation Button -->
    <div v-if="isTable" class="mb-4">
      <div class="text-sm flex justify-between">
        <div class="text-[13px] text-text mt-4 font-regular">
          Pages / Faculty Loads
        </div>
        <div class="flex gap-2">
          <!-- Auto Generation -->
          <div
            @click="fetchSchedule"
            class="group flex items-center gap-2 px-4 py-2 border text-green-600 border-green-600 hover:bg-green-600 hover:text-white rounded-xl hover:shadow-lg cursor-pointer transition duration-200"
          >
            <div
              class="p-1 bg-green-100 rounded-full flex items-center justify-center transition duration-200 group-hover:bg-white"
            >
              <icon
                :name="'arrow-path'"
                class="w-4 h-4 text-green-600 transition duration-200 group-hover:text-green-600"
              />
            </div>
            <span class="font-medium text-sm">Auto Generation</span>
          </div>

          <!-- Save this schedule -->
          <div
            @click="saveScheduled"
            class="group flex items-center gap-2 px-4 py-2 border text-green-600 border-green-600 hover:bg-green-600 hover:text-white rounded-xl hover:shadow-lg cursor-pointer transition duration-200"
          >
            <div
              class="p-1 bg-green-100 rounded-full flex items-center justify-center transition duration-200 group-hover:bg-white"
            >
              <icon
                :name="'circle-check'"
                class="w-4 h-4 text-green-600 transition duration-200 group-hover:text-green-600"
              />
            </div>
            <span class="font-medium text-sm">Save this schedule</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-overlay">
      <div
        class="loading-content flex flex-col items-center justify-center space-y-4"
      >
        <img src="@/assets/img/loading.gif" alt="Loading" class="w-28" />

        <div class="progress-bar w-full bg-gray-200 rounded-full h-3">
          <div
            class="progress-fill bg-defaultGreen h-3 rounded-full"
            :style="{ width: progress + '%' }"
          ></div>
        </div>

        <div class="loading-text text-gray-700 font-medium">
          Generating Schedule... {{ Math.floor(progress) }}%
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- Schedule -->
    <div v-else class="grid-wrapper">
      <div
        v-for="(slots, instructor) in groupedSchedule"
        :key="instructor"
        class="schedule-wrapper"
      >
        <div class="instructor-header">{{ instructor }}</div>

        <table class="schedule-table">
          <thead>
            <tr>
              <th class="time-col">TIME</th>
              <th v-for="day in days" :key="day">{{ day }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="slot in timeSlots" :key="slot.start + slot.end">
              <td>{{ slot.start }} - {{ slot.end }}</td>
              <td v-for="day in days" :key="day">
                <div
                  v-for="item in getScheduleForCell(slot, day, instructor)"
                  :key="item.course_name + item.start_hour + item.room_name"
                  class="cell-item"
                >
                  <strong>{{ item.course_name }} ({{ item.type }})</strong
                  ><br />
                  Room: {{ item.room_name }}<br />
                  Faculty: {{ item.faculty_name }} Set: {{ item.set }}

                  <!-- Conflict Button -->
                  <button
                    v-if="item.conflict"
                    @click="openConflictModal(item)"
                    class="mt-1 px-2 py-1 text-xs rounded bg-red-100 text-red-600 hover:bg-red-200"
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

    <!-- Conflict Modal -->
    <div
      v-if="showConflictModal"
      class="fixed inset-0 flex items-center justify-center bg-black/50 z-50 animate-slideUp"
    >
      <div class="bg-white w-full max-w-lg rounded-2xl shadow-lg p-6 relative">
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

        <div class="space-y-3">
          <div
            v-for="conflict in selectedConflict.conflicts"
            :key="conflict.course_name + conflict.room_name"
            class="p-3 bg-red-50 border border-red-200 rounded-lg text-sm"
          >
            <p>
              <span class="font-semibold">{{ conflict.course_name }}</span>
              ({{ conflict.type }})
            </p>
            <p>🕒 {{ conflict.start_hour }} - {{ conflict.end_hour }}</p>
            <p>📍 Room: {{ conflict.room_name }}</p>
            <p>👨‍🏫 Faculty: {{ conflict.faculty_name }}</p>
            <p>📌 Set: {{ conflict.set }}</p>
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
</style>
