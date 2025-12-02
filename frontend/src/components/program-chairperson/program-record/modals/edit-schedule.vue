<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 p-10 gap-2"
  >
    <div class="flex justify-center gap-4 w-full">
      <!-- MAIN MODAL WRAPPER -->
      <div
        class="bg-white w-[50vw] h-[95vh] rounded-xl shadow-xl flex flex-col overflow-hidden p-1"
      >
        <!-- HEADER -->
        <div
          class="flex items-center justify-between bg-defaultGreen text-white px-6 py-3 rounded-t-lg"
        >
          <div class="flex items-center gap-2">
            <icon name="edit" />
            <h1 class="text-lg font-bold">Edit Schedule</h1>
          </div>

          <icon
            name="circle-close3"
            @click="$emit('close')"
            class="cursor-pointer text-white w-6 h-6"
          />
        </div>

        <!-- BODY -->
        <div class="flex flex-1 overflow-hidden">
          <!-- LEFT: CALENDAR AREA -->
          <div
            :class="[
              'transition-all duration-300 overflow-hidden h-full',
              showAddSchedulePanel ? 'w-[100%]' : 'w-full',
            ]"
          >
            <div class="flex-1 overflow-auto bg-gray-50 p-2 h-full">
              <div
                v-for="(records, instructor) in groupedSchedule"
                :key="instructor"
                class="border rounded-lg shadow-sm bg-white mb-4"
              >
                <!-- Instructor Header -->
                <div
                  class="py-3 px-4 border-b bg-gray-100 flex items-center justify-between"
                >
                  <div class="font-semibold text-gray-800">
                    {{ instructor }}
                  </div>

                  <button
                    @click="openAddSchedulePanel(instructor)"
                    class="px-3 py-1 text-xs font-bold text-defaultGreen rounded-full border border-defaultGreen hover:bg-defaultGreen hover:text-white"
                  >
                    Add
                  </button>
                </div>

                <!-- TABLE -->
                <div class="overflow-x-auto">
                  <table
                    class="w-full table-auto border-separate border-spacing-0 text-[11px]"
                  >
                    <thead class="bg-gray-200 sticky top-0 z-10">
                      <tr>
                        <th class="px-3 py-3 border text-center w-24">Time</th>
                        <th
                          v-for="day in days"
                          :key="day"
                          class="px-3 py-2 border text-center w-28"
                        >
                          {{ day }}
                        </th>
                      </tr>
                    </thead>

                    <tbody>
                      <tr
                        v-for="slot in timeSlots"
                        :key="slot.start + slot.end"
                        class="odd:bg-white even:bg-gray-50"
                      >
                        <td class="px-2 py-5 border text-center">
                          {{ formatTime(slot.start) }} -
                          {{ formatTime(slot.end) }}
                        </td>

                        <td
                          v-for="day in days"
                          :key="day"
                          class="relative border h-[60px] p-0"
                          @dragover.prevent
                          @drop="onDrop($event, instructor, day, slot.start)"
                        >
                          <template
                            v-for="item in getScheduleForCell(
                              slot,
                              day,
                              instructor
                            )"
                            :key="item.id"
                          >
                            <div
                              v-if="isStartingSlot(item, slot)"
                              draggable="true"
                              @dragstart="onDragStart($event, item)"
                              :class="[
                                'absolute inset-x-1 border rounded-lg text-[11px] p-1 shadow-sm truncate transition cursor-pointer hover:bg-yellow-100 hover:defaultGreen',
                                item.id?.toString().startsWith('temp-')
                                  ? 'bg-purple-200 border-purple-400 text-purple-900'
                                  : getTypeColor(item.type),
                                hasRoomConflict(item)
                                  ? 'bg-red-300 border-red-500 text-red-900'
                                  : '',
                              ]"
                              :style="{
                                top: getBlockTop(item, slot.start) + 'px',
                                height: getBlockHeight(item) + 'px',
                                width: 'calc(100% - 0.5rem)',
                                zIndex: 10,
                              }"
                            >
                              <div class="truncate font-semibold">
                                {{ item.course_code }}
                              </div>
                              <div class="truncate">
                                {{ item.room_name }}
                              </div>
                              <div class="truncate">
                                {{ item.class_id }}
                              </div>

                              <button
                                v-if="hasRoomConflict(item)"
                                @click.stop="openConflictModal(item)"
                                class="mt-1 w-full text-[10px] bg-red-100 text-red-600 rounded"
                              >
                                ⚠ View Conflict
                              </button>
                            </div>
                          </template>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <!-- instructor loop -->
            </div>
          </div>
        </div>

        <!-- FOOTER -->
        <div
          class="flex justify-end gap-2 p-4 bg-white border-t shadow-md text-xs"
        >
          <button
            @click="$emit('close')"
            class="bg-gray-100 text-gray-600 px-4 py-2 rounded-lg hover:bg-gray-200"
          >
            Cancel
          </button>

          <button
            @click="saveEdit"
            class="bg-defaultGreen text-white px-4 py-2 rounded-lg hover:bg-green-700"
            :disabled="saving || !isValid"
          >
            {{ saving ? "Saving..." : "Save" }}
          </button>
        </div>
      </div>
      <!-- RIGHT: SLIDING ADD PANEL -->
      <div
        v-if="showAddSchedulePanel"
        class="w-[40%] h-[40%] bg-white border shadow-xl transition-all duration-300 flex justify-start rounded-xl overflow-hidden"
      >
        <div class="max-h-[95vh] overflow-y-auto border-t p-1">
          <div
            class="flex items-center justify-between px-4 py-3 bg-defaultGreen text-white rounded-t-lg"
          >
            <h3 class="font-semibold">
              Add Schedule — {{ selectedInstructorName }}
            </h3>
            <icon
              name="circle-close3"
              @click="closeAddSchedulePanel"
              class="cursor-pointer text-white w-6 h-6"
            />
          </div>

          <table class="min-w-full divide-y divide-gray-200 text-xs">
            <thead class="bg-gray-100">
              <tr>
                <th class="px-4 py-3 border w-[20%]">Course</th>
                <th class="px-4 py-3 border">Room</th>
                <th class="px-4 py-3 border">Day</th>
                <th class="px-4 py-3 border">Start</th>
                <th class="px-4 py-3 border">Hours</th>
                <th class="px-4 py-3 border text-center">Action</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="record in localData"
                :key="record.id"
                class="hover:bg-gray-50"
              >
                <td class="px-2 py-2 border relative">
                  <input
                    v-model="record.searchCourseQuery"
                    type="text"
                    placeholder="Select course..."
                    class="px-3 py-2 border w-full rounded-md text-md"
                    @focus="record.showCourseDropdown = true"
                    @input="record.course_id = null"
                  />

                  <div
                    v-if="
                      record.showCourseDropdown &&
                      filteredCourses(record).length
                    "
                    class="absolute z-10 w-full bg-white border rounded-md max-h-40 overflow-y-auto mt-1"
                  >
                    <div
                      v-for="course in filteredCourses(record)"
                      :key="course.course_id"
                      class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                      @mousedown="selectCourse(record, course)"
                    >
                      {{ course.course_code }}
                    </div>
                  </div>
                </td>

                <td class="px-2 py-2 border relative">
                  <input
                    v-model="record.searchRoomQuery"
                    type="text"
                    placeholder="Select room..."
                    class="px-3 py-2 border w-full rounded-md text-md"
                    @focus="record.showRoomDropdown = true"
                    @input="record.room_id = null"
                  />

                  <div
                    v-if="
                      record.showRoomDropdown && filteredRooms(record).length
                    "
                    class="absolute z-10 w-full bg-white border rounded-md max-h-40 overflow-y-auto mt-1"
                  >
                    <div
                      v-for="room in filteredRooms(record)"
                      :key="room.room_id"
                      class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                      @mousedown="selectRoom(record, room)"
                    >
                      {{ room.room_name }}
                    </div>
                  </div>
                </td>

                <td class="px-2 py-2 border">
                  <input
                    v-model="record.day"
                    class="w-full px-3 py-2 border rounded-md"
                  />
                </td>

                <td class="px-2 py-2 border">
                  <input
                    v-model.number="record.start_hour"
                    type="number"
                    class="w-full px-3 py-2 border rounded-md"
                  />
                </td>

                <td class="px-2 py-2 border">
                  <input
                    v-model.number="record.duration"
                    type="number"
                    class="w-full px-3 py-2 border rounded-md"
                  />
                </td>

                <td class="px-2 py-3 border text-center">
                  <button
                    @click="toggleDelete(record)"
                    class="bg-red-500 text-white px-3 py-1 rounded-full hover:bg-red-600"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <div class="flex justify-end gap-2 p-3 text-xs">
            <button
              @click="addNewRow"
              class="bg-defaultGreen text-white px-3 py-2 rounded-lg flex items-center gap-1"
            >
              <icon name="circle-add1" />
              Add Row
            </button>
            <button
              @click="cancelNewRow"
              class="bg-gray-300 text-gray-800 px-2 py-2 rounded-lg"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="conflictModalVisible"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50"
    >
      <div
        class="bg-white rounded-xl shadow-lg w-full max-w-lg relative max-h-[80vh] overflow-y-auto p-6"
      >
        <!-- TODO  Header -->
        <div class="flex justify-between items-center border-b pb-3 mb-4">
          <div class="flex gap-1">
            <icon
              name="exclamation-circle"
              class="text-red-900 w-7 p-1 rounded-full bg-red-200"
            />
            <h3 class="text-lg font-semibold text-gray-800">
              Schedule Conflicts
            </h3>
          </div>

          <button
            @click="closeConflictModal"
            class="text-gray-400 hover:text-gray-600 transition"
          >
            ✕
          </button>
        </div>

        <!-- TODO  Conflicts List -->
        <div class="space-y-3">
          <div class="px-4 py-3 rounded-xl bg-red-50 text-sm">
            Please select another shedule.
          </div>
          <div
            v-for="conflict in conflictRecords"
            :key="conflict.id"
            class="p-3 rounded-md shadow-sm space-y-2"
          >
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Faculty:</span>
              {{ conflict.faculty_name }}
            </p>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Course:</span>
              {{ conflict.course_code }}
            </p>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Room:</span> {{ conflict.room_name }}
            </p>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Day:</span> {{ conflict.day }}
            </p>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Time:</span>
              {{ conflict.time_slot }}
            </p>
            <p class="text-sm text-gray-800">
              <span class="font-semibold">Time:</span>
              {{ conflict.class_id }}
            </p>
          </div>
        </div>

        <!-- TODO  Footer -->
        <div class="flex justify-end mt-5">
          <button
            @click="closeConflictModal"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition text-sm"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- TODO CONFIRM DELETE MODAL -->

    <div
      v-if="showConfirmDelete"
      class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-xl shadow-xl w-full max-w-sm p-6">
        <!-- Header -->
        <h2
          class="text-lg font-semibold text-red-600 flex items-center gap-2 mb-4"
        >
          <icon name="exclamation-circle" class="text-red-600 w-6 h-6" />
          Confirm Delete
        </h2>

        <!-- Message -->
        <p class="text-gray-700 mb-6">
          Are you sure you want to delete this scheduled course?
          <br />
          <span class="font-semibold text-gray-900 block mt-1">
            This action cannot be undone.
          </span>
        </p>

        <!-- Buttons -->
        <div class="flex justify-end gap-3">
          <button
            @click="cancelDelete"
            class="px-4 py-2 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300"
          >
            Cancel
          </button>

          <button
            @click="confirmDelete"
            class="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";
import icon from "@/assets/icon.vue";
export default {
  components: { icon },
  props: {
    show: Boolean,
    instructorData: { type: Array, default: () => [] },
  },
  data() {
    return {
      user: {},
      localData: [],
      saving: false,
      days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      timeSlots: Array.from({ length: 12 }, (_, i) => ({
        start: i + 8,
        end: i + 9,
      })),
      draggedRecord: null,
      hourHeight: 60,
      fullSchedules: [],
      conflictModalVisible: false,
      conflictRecords: [],

      showConfirmDelete: false,
      deleteTarget: null,
      deleting: false,

      showAddSchedulePanel: false,
      selectedInstructorName: "",
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rooms"]),
    unscheduledCourses() {
      const scheduledCourseIds = new Set(
        this.localData.map((r) => r.course_id).filter(Boolean)
      );

      const fetchDataStore = useFetchDataStore();

      let courses = fetchDataStore.courses.filter(
        (c) => !scheduledCourseIds.has(c.course_id)
      );

      // Only show courses matching user's institute & program if Program Chairperson
      if (this.user.role === "Program Chairperson") {
        courses = courses.filter(
          (c) =>
            c.institute_id === this.user.institute_id &&
            c.program_id === this.user.program_id
        );
      }

      return courses;
    },
    groupedSchedule() {
      const groups = {};
      this.localData.forEach((rec) => {
        if (!rec.faculty_name) return; // skip rows without instructor
        if (!groups[rec.faculty_name]) groups[rec.faculty_name] = [];
        groups[rec.faculty_name].push(rec);
      });
      return groups;
    },

    allData() {
      // combine fullSchedules and localData, avoid duplicates
      const localIds = new Set(this.localData.map((r) => r.id));
      const merged = [...this.localData];

      (this.fullSchedules || []).forEach((r) => {
        if (!localIds.has(r.id)) {
          merged.push({
            ...r,
            searchRoomQuery: r.room_name || "",
            showRoomDropdown: false,
            searchCourseQuery: r.course_code || "",
            showCourseDropdown: false,
          });
        }
      });

      return merged;
    },
    isValid() {
      return this.localData.every(
        (r) =>
          r.faculty_name &&
          r.day &&
          r.start_hour != null &&
          r.duration != null &&
          !this.hasRoomConflict(r)
      );
    },
  },
  watch: {
    instructorData: {
      immediate: true,
      handler(newVal) {
        const fetchDataStore = useFetchDataStore();

        // Ensure class sections are loaded
        const sections = fetchDataStore.sections || [];

        this.localData = (Array.isArray(newVal) ? [...newVal] : []).map(
          (rec) => {
            // --- FIND CLASS SIZE FROM class_id ---
            let class_size = rec.class_size || null;
            if (rec.class_id) {
              const section = sections.find((s) => s.class_id === rec.class_id);
              if (section) {
                class_size = section.class_size;
              }
            }

            // Ensure course_id & course_code sync
            if (rec.course_code) {
              const course = fetchDataStore.courses.find(
                (c) => c.course_code === rec.course_code
              );
              if (course) {
                rec.course_id = course.course_id;
                rec.course_code = course.course_code;
              }
            } else if (rec.course_id) {
              const course = fetchDataStore.courses.find(
                (c) => c.course_id === rec.course_id
              );
              if (course) {
                rec.course_code = course.course_code;
              }
            }

            return {
              ...rec,
              faculty_id: rec.faculty_id || null,
              class_size, // <-- AUTO SET HERE
              searchRoomQuery: rec.room_name || "",
              showRoomDropdown: false,
              searchCourseQuery: rec.course_code || "",
              showCourseDropdown: false,
              program_id: rec.program_id || this.user.program_id || null,
              institute_id: rec.institute_id || this.user.institute_id || null,
            };
          }
        );
      },
    },
  },

  methods: {
    openAddSchedulePanel(instructor) {
      this.selectedInstructorName = instructor;
      this.showAddSchedulePanel = true;
    },
    closeAddSchedulePanel() {
      this.showAddSchedulePanel = false;
    },
    addNewRow() {
      const first = this.instructorData[0];
      const tempId = `temp-${Date.now()}`;
      const class_id = first?.class_id || null;
      const class_size = first?.class_size || null;

      const startHour = 8;
      const duration = 3;

      const formatTime = (h) => {
        const period = h >= 12 ? "PM" : "AM";
        const hour = h % 12 || 12;
        return `${hour}:00 ${period}`;
      };

      this.localData.push({
        tempId,
        faculty_name: first?.faculty_name || "TBD",
        faculty_id: first?.faculty_id || null,
        class_id,
        class_size,

        day: "Monday",
        start_hour: startHour,
        duration: duration,
        time_slot: `${formatTime(startHour)} - ${formatTime(
          startHour + duration
        )}`, // <-- ADD TIME SLOT

        room_id: null,
        room_name: "",
        room_type: "",
        room_capacity: "",

        course_id: null,
        course_code: "",
        type: "Lecture",
        semester: "",

        program_id: this.user.program_id || null,
        institute_id: this.user.institute_id || null,

        searchRoomQuery: "",
        showRoomDropdown: false,
        searchCourseQuery: "",
        showCourseDropdown: false,
      });
    },
    cancelNewRow() {
      // Remove the last temp row only
      for (let i = this.localData.length - 1; i >= 0; i--) {
        if (
          this.localData[i].tempId &&
          this.localData[i].tempId.startsWith("temp-")
        ) {
          this.localData.splice(i, 1);
          break;
        }
      }
    },
    toggleDelete(record) {
      this.deleteTarget = record;
      this.showConfirmDelete = true;
    },

    cancelDelete() {
      this.showConfirmDelete = false;
      this.deleteTarget = null;
    },

    async confirmDelete() {
      if (!this.deleteTarget) return;

      try {
        this.deleting = true;

        // 🔥 CALL API DELETE ENDPOINT
        await axios.delete(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${this.deleteTarget.id}`
        );

        // 🔥 Remove locally
        this.localData = this.localData.filter(
          (item) => item.id !== this.deleteTarget.id
        );

        toast.success("Schedule deleted successfully.");
      } catch (error) {
        console.error(error);
        toast.error("Failed to delete schedule.");
      } finally {
        this.deleting = false;
        this.showConfirmDelete = false;
        this.deleteTarget = null;

        // 🔄 OPTIONAL: refresh all schedules from Pinia store
        if (this.fetchFacultyLoads) {
          await this.fetchFacultyLoads();
        }
      }
    },

    logRow(record) {
      console.log("New schedule row:", record);
      toast.success("Logged to console!"); // optional feedback
    },
    ...mapActions(useFetchDataStore, [
      "fetchRooms",
      "fetchCourses",
      "fetchClassSections",
    ]),
    // Filter function
    filteredRooms(record) {
      if (!record.searchRoomQuery) return this.rooms;
      return this.rooms.filter((r) =>
        r.room_name.toLowerCase().includes(record.searchRoomQuery.toLowerCase())
      );
    },

    filteredCourses(record) {
      const fetchDataStore = useFetchDataStore();
      if (!fetchDataStore.courses) return [];

      let filtered = fetchDataStore.courses.filter((c) =>
        c.course_code
          .toLowerCase()
          .includes(record.searchCourseQuery.toLowerCase())
      );

      // Only show courses matching user's institute & program if Program Chairperson
      if (this.user.role === "Program Chairperson") {
        filtered = filtered.filter(
          (c) =>
            c.institute_id === this.user.institute_id &&
            c.program_id === this.user.program_id
        );
      }

      return filtered;
    },
    // Select a room from dropdown
    // When user selects a room from the dropdown

    selectRoom(record, room) {
      // Only update if room changed
      if (record.room_id !== room.room_id) {
        record.room_id = room.room_id;
        record.room_name = room.room_name;
        record.room_type = room.room_type;
        record.room_capacity = room.room_capacity;
      }
      record.searchRoomQuery = room.room_name; // for display only
      record.showRoomDropdown = false;
    },
    selectCourse(record, course) {
      record.course_id = course.course_id;
      record.course_code = course.course_code;
      record.semester = String(course.course_semester); // <-- convert to string

      const startYear = course?.curriculum?.curriculum_start_year;
      const endYear = course?.curriculum?.curriculum_end_year;
      record.school_year =
        startYear && endYear ? `${startYear} - ${endYear}` : startYear || "";

      record.searchCourseQuery = course.course_code;
      record.showCourseDropdown = false;
    },
    selectSection(record, section) {
      record.class_id = section.class_id;
      record.class_size = section.class_size; // auto update
    },
    openConflictModal(record) {
      const conflicts = this.getConflictingRecords(record);
      if (!conflicts.length) return;

      this.conflictRecords = conflicts;
      this.conflictModalVisible = true;
    },

    closeConflictModal() {
      this.conflictModalVisible = false;
      this.conflictRecords = [];
    },
    getConflictsInCell(slot, day, instructor) {
      const cellRecords = this.getScheduleForCell(slot, day, instructor);
      return cellRecords
        .map((r) => this.getConflictingRecords(r))
        .flat()
        .filter((r) => r.faculty_name !== instructor);
    },

    async loadData() {
      try {
        const fetchDataStore = useFetchDataStore();
        await fetchDataStore.fetchFinalSchedules();
        this.fullSchedules = Array.isArray(fetchDataStore.final_schedules)
          ? fetchDataStore.final_schedules
          : [];
      } catch (error) {
        console.error("Failed to load full schedules:", error);
        this.fullSchedules = [];
      }
    },
    getConflictingRecords(record) {
      return this.allData.filter((r) => {
        if (r.id === record.id) return false;

        // ✅ Only compare schedules on the same day
        if (r.day !== record.day) return false;

        // Convert to numeric hours
        const rStart = Number(r.start_hour);
        const rEnd = rStart + Number(r.duration);
        const newStart = Number(record.start_hour);
        const newEnd = newStart + Number(record.duration);

        // Check time overlap
        const overlaps = Math.max(rStart, newStart) < Math.min(rEnd, newEnd);
        if (!overlaps) return false;

        // Room or Faculty conflict
        const roomConflict = r.room_id === record.room_id;
        const facultyConflict = r.faculty_name === record.faculty_name;

        return roomConflict || facultyConflict;
      });
    },
    hasRoomConflict(record) {
      return this.getConflictingRecords(record).length > 0;
    },

    getConflictTooltip(record) {
      const conflicts = this.getConflictingRecords(record);
      if (!conflicts.length) return "";
      return conflicts
        .map(
          (c) =>
            `Conflict with: ${c.faculty_name} (${c.course_code}) in ${c.room_name}`
        )
        .join("\n");
    },

    formatTime(h) {
      const period = h >= 12 ? "PM" : "AM";
      const hour = h % 12 || 12;
      return `${hour}:00 ${period}`;
    },

    getScheduleForCell(slot, day, instructor) {
      return (this.localData || []).filter(
        (r) =>
          r.faculty_name === instructor &&
          r.day === day &&
          r.start_hour != null &&
          r.duration != null &&
          r.start_hour < slot.end &&
          r.start_hour + r.duration > slot.start
      );
    },

    isStartingSlot(item, slot) {
      return item.start_hour === slot.start;
    },
    getBlockTop(item, slotStart) {
      return (item.start_hour - slotStart) * this.hourHeight;
    },

    getBlockHeight(item) {
      return Math.max(1, Number(item.duration)) * this.hourHeight - 1;
    },

    getTypeColor(type) {
      switch (type) {
        case "Lecture":
          return "bg-green-200 border-green-400";
        case "Laboratory":
          return "bg-blue-200 border-blue-400";
        default:
          return "bg-gray-200 border-gray-400";
      }
    },

    onDragStart(event, record) {
      this.draggedRecord = record;
      event.dataTransfer.effectAllowed = "move";
    },

    async onDrop(event, targetInstructor, targetDay, targetStartHour) {
      if (!this.draggedRecord) return;

      // Create a temporary record representing the new position
      const tempRecord = {
        ...this.draggedRecord,
        faculty_name: targetInstructor,
        day: targetDay,
        start_hour: targetStartHour,
      };

      // Check for conflicts
      const conflicts = this.getConflictingRecords(tempRecord);

      if (conflicts.length) {
        // Show conflict modal with details
        this.conflictRecords = conflicts;
        this.conflictModalVisible = true;
        this.draggedRecord = null;
        return; // do not move or PATCH
      }

      // Find existing record in target cell (for swapping)
      const targetRecord = this.localData.find(
        (r) =>
          r.faculty_name === targetInstructor &&
          r.day === targetDay &&
          r.start_hour === targetStartHour
      );

      if (targetRecord) {
        // Swap records safely
        const temp = {
          day: targetRecord.day,
          start_hour: targetRecord.start_hour,
          faculty_name: targetRecord.faculty_name,
        };

        Object.assign(targetRecord, {
          day: this.draggedRecord.day,
          start_hour: this.draggedRecord.start_hour,
          faculty_name: this.draggedRecord.faculty_name,
        });

        Object.assign(this.draggedRecord, temp);

        // PATCH both records
        await Promise.all(
          [targetRecord, this.draggedRecord].map(async (rec) => {
            const payload = { ...rec };
            delete payload.searchRoomQuery;
            delete payload.showRoomDropdown;
            delete payload.searchCourseQuery;
            delete payload.showCourseDropdown;

            const id = rec.id || rec.schedule_id || rec.final_generated_id;
            if (!id)
              throw new Error("Cannot update unsaved schedule. Save first.");

            await axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
              payload
            );
          })
        );

        toast.success("Schedules swapped successfully!");
      } else {
        // No existing record, just move dragged record
        Object.assign(this.draggedRecord, {
          day: targetDay,
          start_hour: targetStartHour,
          faculty_name: targetInstructor,
        });

        const payload = { ...this.draggedRecord };
        delete payload.searchRoomQuery;
        delete payload.showRoomDropdown;
        delete payload.searchCourseQuery;
        delete payload.showCourseDropdown;

        const id =
          this.draggedRecord.id ||
          this.draggedRecord.schedule_id ||
          this.draggedRecord.final_generated_id;
        if (!id) {
          toast.error("Cannot update unsaved schedule. Please save first.");
          this.draggedRecord = null;
          return;
        }

        await axios.patch(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
          payload
        );

        // toast.success("Schedule moved successfully!");
      }

      this.draggedRecord = null;
    },
    async saveEdit() {
      this.saving = true;
      try {
        const fetchDataStore = useFetchDataStore();

        // 1️⃣ Remove duplicates locally
        const seen = new Set();
        this.localData = this.localData.filter((record) => {
          const key = `${record.course_code}|${record.room_name}|${record.class_id}`;
          if (seen.has(key)) return false;
          seen.add(key);
          return true;
        });

        // 2️⃣ Prepare payloads
        const payloads = this.localData.map((record) => {
          const start = Number(record.start_hour) || 0;
          const duration = Number(record.duration) || 0;
          const formatTime = (h) => {
            const hour = h % 12 || 12;
            const period = h >= 12 ? "PM" : "AM";
            return `${hour}:00 ${period}`;
          };
          return {
            ...record,
            start_hour: start,
            duration,
            time_slot: `${formatTime(start)} - ${formatTime(start + duration)}`,
          };
        });

        // 3️⃣ Separate new vs existing rows
        const newRows = [];
        const existingRows = [];

        this.localData.forEach((record, index) => {
          const payload = { ...payloads[index] };
          delete payload.searchRoomQuery;
          delete payload.showRoomDropdown;
          delete payload.searchCourseQuery;
          delete payload.showCourseDropdown;

          const existingId =
            record.id || record.schedule_id || record.final_generated_id;
          if (existingId) {
            existingRows.push({ id: existingId, payload });
          } else {
            newRows.push(payload);
          }
        });

        // 4️⃣ Save new rows
        if (newRows.length) {
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/bulk`,
            newRows
          );
        }

        // 5️⃣ Update existing rows
        if (existingRows.length) {
          await Promise.all(
            existingRows.map(({ id, payload }) =>
              axios.patch(
                `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
                payload
              )
            )
          );
        }

        // 6️⃣ Refresh Pinia store
        await fetchDataStore.fetchFinalSchedules();

        // 7️⃣ Map to fresh objects for reactivity
        const updatedSchedules = (fetchDataStore.final_schedules || []).map(
          (rec) => ({
            ...rec,
            searchRoomQuery: rec.room_name || "",
            showRoomDropdown: false,
            searchCourseQuery: rec.course_code || "",
            showCourseDropdown: false,
          })
        );

        this.localData = updatedSchedules; // update child
        this.$emit(
          "saved",
          updatedSchedules.map((r) => ({ ...r }))
        ); // emit fresh copies to parent

        toast.success("Schedules saved successfully!");
        this.$emit("close");
      } catch (err) {
        console.error("Failed to save schedules:", err);
        toast.error("Failed to save schedules. Check console.");
      } finally {
        this.saving = false;
      }
    },
    async fetchUser() {
      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/auth/me`,
          { withCredentials: true }
        );
        this.user = res.data || {};
        await this.fetchCoursesForUser();
      } catch {
        this.user = {};
      }
    },
    async fetchCoursesForUser() {
      const fetchDataStore = useFetchDataStore();
      if (!this.user.role) return;

      let url = `${process.env.VUE_APP_API_BASE_URL}/courses/get-courses`;

      if (this.user.role === "Program Chairperson") {
        const params = new URLSearchParams();
        if (this.user.institute_id)
          params.append("institute_id", this.user.institute_id);
        if (this.user.program_id)
          params.append("program_id", this.user.program_id);
        url += `?${params.toString()}`;
      }

      try {
        const { data } = await axios.get(url);
        fetchDataStore.courses = data;
      } catch {
        fetchDataStore.courses = [];
      }
    },
  },
  async mounted() {
    await this.fetchUser();
    const roomsPromise = this.fetchRooms();
    if (roomsPromise && roomsPromise.then) await roomsPromise;
    await this.fetchClassSections();
    await this.loadData();
  },
};
</script>

<style scoped>
td {
  transition: background 0.2s;
  position: relative;
}
</style>
