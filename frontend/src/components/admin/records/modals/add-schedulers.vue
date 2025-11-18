<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg fixed top-20">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="schedulesForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">Add Class Schedule</h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <div class="p-5 w-[40vw] text-left">
          <!-- Fields -->
          <div class="space-y-5">
            <!-- Instructor -->
            <div class="w-full space-y-2">
              <label for="instructor_id" class="font-bold">Instructor :</label>
              <select
                v-model="form.instructor_id"
                id="instructor_id"
                required
                class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
              >
                <option value="" disabled>Select Instructor:</option>
                <option
                  v-for="instructor in instructors"
                  :key="instructor.instructor_id"
                  :value="instructor.instructor_id"
                >
                  {{ instructor.instructor_lname }},
                  {{ instructor.instructor_fname }}
                </option>
              </select>
            </div>

            <!-- Course -->
            <div class="w-full space-y-2">
              <label for="course_id" class="font-bold">Course :</label>
              <select
                v-model="form.course_id"
                id="course_id"
                required
                class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
              >
                <option value="" disabled>Select Course:</option>
                <option
                  v-for="course in courses"
                  :key="course.course_id"
                  :value="course.course_id"
                >
                  {{ course.course_code }}
                </option>
              </select>
            </div>

            <!-- Room -->
            <div class="w-full space-y-2">
              <label for="room_id" class="font-bold">Room :</label>
              <select
                v-model="form.room_id"
                id="room_id"
                required
                class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
              >
                <option value="" disabled>Select Room:</option>
                <option
                  v-for="room in rooms"
                  :key="room.room_id"
                  :value="room.room_id"
                >
                  {{ room.room_name }}
                </option>
              </select>
            </div>

            <!-- Section -->
            <div class="w-full space-y-2">
              <label for="section_id" class="font-bold">Section:</label>
              <select
                v-model="form.section_id"
                id="section_id"
                required
                class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
              >
                <option value="" disabled>Select Section:</option>
                <option
                  v-for="section in sections"
                  :key="section.section_id"
                  :value="section.section_id"
                >
                  {{ section.section_set }}
                </option>
              </select>
            </div>

            <!-- Days -->

            <div class="w-full space-y-2 text-left">
              <label class="font-bold">Days:</label>
              <div class="flex flex-wrap gap-2">
                <div
                  v-for="day in schedule_days"
                  :key="day"
                  @click="toggleDay(day)"
                  :class="[
                    'cursor-pointer px-4 py-2 rounded-full border transition-all duration-200 text-sm',
                    form.schedule_days.includes(day)
                      ? ' bg-defaultGreen text-white border-green01 shadow-md'
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100',
                  ]"
                >
                  {{ day }}
                </div>
              </div>
            </div>

            <!-- Time -->
            <div class="w-full text-left gap-3 flex mt-2">
              <div class="w-full space-y-2">
                <label class="font-bold">Start Time:</label>
                <select
                  v-model="form.time_start"
                  required
                  class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
                >
                  <option value="" disabled>Select Time Start:</option>
                  <option
                    v-for="time in time"
                    :key="time.time_id"
                    :value="time.time"
                  >
                    {{ formatTime12Hour(time.time) }}
                  </option>
                </select>
              </div>
              <div class="w-full space-y-2">
                <label class="font-bold">End Time:</label>
                <select
                  v-model="form.time_end"
                  required
                  class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
                >
                  <option value="" disabled>Select Time End:</option>
                  <option
                    v-for="time in time"
                    :key="time.time_id"
                    :value="time.time"
                  >
                    {{ formatTime12Hour(time.time) }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <!-- Buttons -->
          <div class="tracking-wide flex justify-end gap-2 mt-4">
            <button
              class="bg-red-600 p-2 px-3 rounded-md text-white hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              class="bg-defaultGreen p-2 px-3 rounded-md text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
              type="submit"
            >
              Submit
            </button>
          </div>
        </div>
      </form>
    </div>

    <!-- Conflict Modal -->
    <div
      v-if="showConflictModal"
      class="fixed inset-0 bg-gray-900 bg-opacity-40 flex justify-center items-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-[90%] max-w-md shadow-xl">
        <h2 class="text-lg font-bold text-red-600 mb-4">Schedule Conflict</h2>

        <div
          class="mb-4 text-sm text-gray-800 text-left w-full bg-red-200 px-3 py-3 gap-2 rounded-md flex items-center"
        >
          <icon name="exclamationmark" class="text-red-600 w-5 h-5" />
          <p>This schedule conflicts with an existing one:</p>
        </div>

        <ul v-if="conflictSchedule" class="text-sm space-y-2 text-left">
          <li>
            <strong>Instructor:</strong>
            {{
              (conflictSchedule.instructor_fname ||
                conflictSchedule.instructor?.instructor_fname ||
                "") +
              " " +
              (conflictSchedule.instructor_lname ||
                conflictSchedule.instructor?.instructor_lname ||
                "")
            }}
          </li>
          <li>
            <strong>Course:</strong>
            {{
              conflictSchedule.course_name ||
              conflictSchedule.course?.course_code
            }}
          </li>
          <li>
            <strong>Room:</strong>
            {{ conflictSchedule.room_name || conflictSchedule.room?.room_name }}
          </li>
          <li>
            <strong>Section:</strong>
            {{
              conflictSchedule.section_name ||
              conflictSchedule.section?.section_set
            }}
          </li>
          <li>
            <strong>Days:</strong>
            {{
              Array.isArray(conflictSchedule.schedule_days)
                ? conflictSchedule.schedule_days.join(", ")
                : typeof conflictSchedule.schedule_days === "string"
                ? conflictSchedule.schedule_days
                : "N/A"
            }}
          </li>
          <li>
            <strong>Time:</strong>
            {{ formatTime12Hour(conflictSchedule.time_start) }} –
            {{ formatTime12Hour(conflictSchedule.time_end) }}
          </li>
        </ul>

        <div class="flex justify-end gap-2 mt-6">
          <button
            @click="showConflictModal = false"
            class="px-4 py-2 text-sm rounded-md bg-gray-300 hover:bg-gray-400 text-gray-800"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";
import axios from "axios";

export default {
  name: "AddClassSchedules",
  components: {
    icon,
  },
  data() {
    return {
      schedule_days: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ],
      form: {
        schedule_days: [],
        instructor_id: "",
        instructor_name: "",
        course_id: "",
        course_name: "",
        section_id: "",
        section_name: "",
        room_id: "",
        room_name: "",
        time_start: "",
        time_end: "",
      },
      conflictSchedule: null,
      showConflictModal: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, [
      "instructors",
      "courses",
      "rooms",
      "sections",
      "time",
    ]),
  },
  methods: {
    toggleDay(day) {
      const index = this.form.schedule_days.indexOf(day);
      if (index === -1) {
        this.form.schedule_days.push(day);
      } else {
        this.form.schedule_days.splice(index, 1);
      }
    },
    formatTime12Hour(time) {
      if (!time) return "";
      const [hour, minute] = time.split(":");
      const h = parseInt(hour);
      const ampm = h >= 12 ? "PM" : "AM";
      const hour12 = h % 12 || 12;
      return `${String(hour12).padStart(2, "0")}:${minute} ${ampm}`;
    },
    isTimeOverlap(start1, end1, start2, end2) {
      return start1 < end2 && start2 < end1;
    },
    ...mapActions(useFetchDataStore, [
      "fetchInstructors",
      "fetchCourses",
      "fetchRooms",
      "fetchSections",
      "fetchTime",
    ]),
    async submitData() {
      const formEl = this.$refs.schedulesForm;

      if (!formEl.checkValidity()) {
        formEl.reportValidity();
        return;
      }

      if (this.form.schedule_days.length === 0) {
        toast.error("Please select at least one day.");
        return;
      }

      if (!this.form.time_start || !this.form.time_end) {
        toast.error("Please select both start and end times.");
        return;
      }

      const startIndex = this.time.findIndex(
        (t) => t.time === this.form.time_start
      );
      const endIndex = this.time.findIndex(
        (t) => t.time === this.form.time_end
      );

      if (startIndex === -1 || endIndex === -1) {
        toast.error("Invalid time selected.");
        return;
      }

      if (startIndex >= endIndex) {
        toast.error("End time must be after start time.");
        return;
      }

      // Populate names
      const instructor = this.instructors.find(
        (i) => i.instructor_id === this.form.instructor_id
      );
      const course = this.courses.find(
        (c) => c.course_id === this.form.course_id
      );
      const room = this.rooms.find((r) => r.room_id === this.form.room_id);
      const section = this.sections.find(
        (s) => s.section_id === this.form.section_id
      );

      this.form.instructor_name = instructor
        ? `${instructor.instructor_fname} ${instructor.instructor_lname}`
        : "";
      this.form.course_name = course ? course.course_code : "";
      this.form.room_name = room ? room.room_name : "";
      this.form.section_name = section ? section.section_set : "";

      console.log("Submitting schedule:", this.form);

      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/class-schedules/get-class-schedules"
        );
        const existing = response.data;
        console.log("Fetched schedules:", existing);

        const conflict = existing.find((sched) => {
          let scheduleDays = sched.schedule_days;

          // Normalize schedule_days to array
          if (!Array.isArray(scheduleDays)) {
            try {
              scheduleDays = JSON.parse(scheduleDays);
            } catch {
              console.warn(
                "Falling back to split for schedule_days:",
                sched.schedule_days
              );
              scheduleDays = String(scheduleDays)
                .split(",")
                .map((d) => d.trim());
            }
          }

          const hasCommonDay = scheduleDays.some((day) =>
            this.form.schedule_days.includes(day)
          );

          // ✅ FIXED: Handle nested room object
          const isRoomConflict =
            (sched.room?.room_id ?? sched.room_id) === this.form.room_id;

          const isTimeConflict = this.isTimeOverlap(
            this.form.time_start,
            this.form.time_end,
            sched.time_start,
            sched.time_end
          );

          // Debugging
          console.log("Checking schedule:", sched);
          console.log("Parsed Days:", scheduleDays);
          console.log("Form Days:", this.form.schedule_days);
          console.log("hasCommonDay:", hasCommonDay);
          console.log("Room Match:", isRoomConflict);
          console.log("Time Overlap:", isTimeConflict);

          return hasCommonDay && isTimeConflict && isRoomConflict;
        });

        if (conflict) {
          // Ensure schedule_days is an array
          if (typeof conflict.schedule_days === "string") {
            try {
              conflict.schedule_days = JSON.parse(conflict.schedule_days);
            } catch {
              conflict.schedule_days = conflict.schedule_days
                .split(",")
                .map((d) => d.trim());
            }
          }

          this.conflictSchedule = {
            ...conflict,

            instructor_fname:
              this.instructors.find(
                (c) => c.instructor_id === conflict.instructor_id
              )?.instructor_lname || conflict.instructor_id,
            course_name:
              this.courses.find((c) => c.course_id === conflict.course_id)
                ?.course_code || conflict.course_id,

            room_name:
              this.rooms.find((r) => r.room_id === conflict.room_id)
                ?.room_name || conflict.room_id,

            section_name:
              this.sections.find((s) => s.section_id === conflict.section_id)
                ?.section_set || conflict.section_id,

            schedule_days: Array.isArray(conflict.schedule_days)
              ? conflict.schedule_days
              : typeof conflict.schedule_days === "string"
              ? conflict.schedule_days.split(",").map((d) => d.trim())
              : [],
          };
          this.showConflictModal = true;
          return;
        }

        // No conflict — proceed
        await axios.post(
          process.env.VUE_APP_API_BASE_URL +
            "/class-schedules/add-class-schedules",
          {
            instructor_id: this.form.instructor_id,
            course_id: this.form.course_id,
            section_id: this.form.section_id,
            room_id: this.form.room_id,
            schedule_days: this.form.schedule_days,
            time_start: this.form.time_start,
            time_end: this.form.time_end,
          }
        );

        new Audio(require("@/assets/add.mp3")).play();
        toast.success("Schedule saved!");

        // Optionally update localStorage
        existing.push({
          ...this.form,
        });
        localStorage.setItem("classSchedules", JSON.stringify(existing));

        this.$emit("refresh");
        this.$emit("close");

        // Reset form
        this.form = {
          schedule_days: [],
          instructor_id: "",
          instructor_name: "",
          course_id: "",
          course_name: "",
          section_id: "",
          section_name: "",
          room_id: "",
          room_name: "",
          time_start: "",
          time_end: "",
        };
      } catch (error) {
        toast.error("Failed to add class schedule.");
        console.error(error);
      }
    },
  },
  mounted() {
    this.fetchInstructors();
    this.fetchCourses();
    this.fetchRooms();
    this.fetchSections();
    this.fetchTime();
  },
};
</script>
