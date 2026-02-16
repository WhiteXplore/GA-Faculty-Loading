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
            <h1 class="text-lg font-bold">Edit Schedules</h1>
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
                  <div class="flex flex-col">
                    <span class="text-md font-bold">{{ instructor }}</span>

                    <div v-if="facultyTotalUnits[instructor]">
                      <p class="font-normal text-xs">
                        Total Units:
                        {{ facultyTotalUnits[instructor].totalUnits }}
                      </p>
                    </div>
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
                          class="relative border p-0 overflow-visible transition-colors"
                          :class="{
                            'bg-red-100':
                              draggedRecord &&
                              getConflictsForDrag(
                                draggedRecord,
                                instructor,
                                day,
                                slot.start,
                              ).length,
                          }"
                          :style="{ height: timeSlotHeight + 'px' }"
                          @dragover.prevent
                          @drop="onDrop($event, instructor, day, slot.start)"
                        >
                          <template
                            v-for="item in getScheduleForCell(
                              slot,
                              day,
                              instructor,
                            )"
                            :key="item.id"
                          >
                            <div
                              v-if="isStartingSlot(item, slot)"
                              draggable="true"
                              @dragstart="onDragStart($event, item)"
                              @click="highlightRow(item)"
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
                              <!-- MODE BADGE -->
                              <span
                                v-if="item.mode"
                                :class="[
                                  'absolute top-2 right-2 w-auto h-4 px-1 rounded-full text-[10px] font-bold flex items-center justify-center text-white',
                                  item.mode === 'face to face'
                                    ? 'bg-orange-500'
                                    : '',
                                  item.mode === 'online' ? 'bg-purple-500' : '',
                                ]"
                              >
                                {{
                                  item.mode === "face to face"
                                    ? "F2F"
                                    : "Online"
                                }}
                              </span>

                              <div class="truncate font-semibold">
                                {{ item.course_code }}
                              </div>
                              <div class="truncate">{{ item.room_name }}</div>
                              <div class="truncate">
                                {{ item.program_name }}-{{ item.set_name }}
                              </div>

                              <div class="w-full flex justify-center">
                                <button
                                  v-if="hasRoomConflict(item)"
                                  @click.stop="openConflictModal(item)"
                                  class="mt-1 px-2 h-5 text-[10px] bg-red-100 text-red-600 rounded"
                                >
                                  ⚠ View
                                </button>
                              </div>
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
            class="bg-defaultGreen text-white px-4 py-2 rounded-lg hover:bg-defaultGreen"
            :disabled="saving || !isValid"
          >
            {{ saving ? "Saving..." : "Save" }}
          </button>
        </div>
      </div>
      <!-- RIGHT: SLIDING ADD PANEL -->
      <div
        v-if="showAddSchedulePanel"
        class="w-[50%] h-[40%] bg-white border shadow-xl transition-all duration-300 flex justify-start rounded-xl overflow-hidden"
      >
        <div class="max-h-[95vh] overflow-y-auto border-t p-0.5">
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
                <th class="px-4 py-3 border w-[15%]">Section</th>
                <th class="px-4 py-3 border w-[15%]">Course</th>
                <th class="px-4 py-3 border w-[13%]">Room</th>
                <th class="px-4 py-3 border w-[10%]">Day</th>
                <th class="px-4 py-3 border w-[10%]">Start</th>
                <th class="px-4 py-3 border w-[10%]">Hours</th>
                <th class="px-4 py-3 border">Set Up</th>
                <th class="px-4 py-3 border text-center">Action</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="record in sortedLocalData"
                :key="record.id || record.tempId"
                :id="'row-' + (record.id || record.tempId)"
                :class="[
                  'hover:bg-green-200',
                  highlightedRecordId === (record.id || record.tempId)
                    ? 'bg-blue-100'
                    : '',
                ]"
              >
                <td class="px-2 py-2 border relative">
                  <input
                    v-model="record.searchSectionQuery"
                    type="text"
                    placeholder="Select section..."
                    class="px-3 py-2 border w-full rounded-md text-md"
                    @focus="record.showSectionDropdown = true"
                    @input="record.class_id = null"
                  />

                  <div
                    v-if="
                      record.showSectionDropdown &&
                      filteredSections(record).length
                    "
                    class="absolute z-10 w-full bg-white border rounded-md max-h-40 overflow-y-auto mt-1"
                  >
                    <div
                      v-for="section in filteredSections(record)"
                      :key="section.class_id"
                      class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                      @mousedown.prevent="selectSection(record, section)"
                    >
                      {{ section.set_name }}
                    </div>
                  </div>
                </td>
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
                    class="w-full px-3 py-2 border rounded-md text-center"
                  />
                </td>

                <td class="px-2 py-2 border text-center">
                  <input
                    v-model.number="record.start_hour"
                    type="number"
                    step="0.5"
                    min="8"
                    max="20"
                    class="w-full px-3 py-2 border rounded-md text-center"
                  />
                </td>

                <td class="px-2 py-2 border text-center">
                  <input
                    v-model.number="record.duration"
                    type="number"
                    class="w-full px-3 py-2 border rounded-md text-center"
                  />
                </td>
                <td class="px-2 py-2 border">
                  <select
                    v-model="record.mode"
                    @change="onModeChange(record)"
                    class="w-full border rounded px-2 py-1 text-sm"
                  >
                    <option value="" disabled selected>Select mode</option>
                    <option value="face to face">Face to face</option>
                    <option value="online">Online</option>
                  </select>
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
      class="fixed inset-0 z-50 bg-black/40 flex items-center justify-center"
    >
      <div class="bg-white w-[900px] rounded-2xl p-6 shadow-xl">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4 border-b pb-2">
          <h3 class="text-lg font-semibold text-red-700">
            Schedule Conflict Detected
          </h3>
          <button
            @click="closeConflictModal"
            class="text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        </div>

        <!-- Body -->
        <div class="grid grid-cols-2 gap-6 mt-6">
          <!-- LEFT: Selected Schedule -->
          <div class="relative bg-white rounded-2xl p-5 border">
            <span
              class="absolute -top-3 left-4 bg-green-600 text-white text-xs px-3 py-1 rounded-full shadow"
            >
              Selected Schedule
            </span>

            <div class="mt-3 space-y-3 text-sm text-gray-800">
              <div class="flex justify-between items-center">
                <h4 class="font-semibold text-base">
                  {{ selectedSchedule.course_code || "No Course Selected" }}
                </h4>
                <span
                  class="text-xs px-2 py-1 rounded-full font-medium"
                  :class="{
                    'bg-orange-500 text-white':
                      selectedSchedule.mode === 'face to face',
                    'bg-purple-700 text-white':
                      selectedSchedule.mode === 'online',
                  }"
                >
                  {{
                    selectedSchedule.mode === "face to face"
                      ? "Face to Face"
                      : "Online"
                  }}
                </span>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <p class="text-xs text-gray-500">Faculty</p>
                  <p class="font-medium">{{ selectedSchedule.faculty_name }}</p>
                </div>

                <div>
                  <p class="text-xs text-gray-500">Section</p>
                  <p class="font-medium">
                    {{ selectedSchedule.program_name }}-{{
                      selectedSchedule.set_name
                    }}
                  </p>
                </div>

                <div>
                  <p class="text-xs text-gray-500">Room</p>
                  <p class="font-medium">{{ selectedSchedule.room_name }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500">Type</p>
                  <p class="font-medium">{{ selectedSchedule.room_type }}</p>
                </div>

                <div>
                  <p class="text-xs text-gray-500">Time</p>
                  <p class="font-medium">
                    {{ formatTime(selectedSchedule.time_start) }} –
                    {{ formatTime(selectedSchedule.time_end) }}
                  </p>
                </div>

                <div>
                  <p class="text-xs text-gray-500">Day</p>
                  <p class="font-medium">{{ selectedSchedule.day }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- RIGHT: Conflicts -->
          <div class="relative bg-white rounded-2xl p-5 border">
            <span
              class="absolute -top-3 left-4 bg-red-600 text-white text-xs px-3 py-1 rounded-full shadow"
            >
              Conflicting Schedules
            </span>

            <div class="mt-3 space-y-4 max-h-[420px] overflow-y-auto pr-2">
              <div
                v-for="conflict in conflictRecords"
                :key="conflict.id"
                class="bg-white rounded-xl p-4 ring-1 ring-red-200"
              >
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between items-center">
                    <h5 class="font-semibold">{{ conflict.course_code }}</h5>
                    <span
                      class="text-xs px-2 py-1 rounded-full font-medium"
                      :class="{
                        'bg-orange-500 text-white':
                          conflict.mode === 'face to face',
                        'bg-purple-700 text-white': conflict.mode === 'online',
                      }"
                    >
                      {{
                        conflict.mode === "face to face"
                          ? "Face to Face"
                          : "Online"
                      }}
                    </span>
                  </div>

                  <div class="grid grid-cols-2 gap-2">
                    <div>
                      <p class="text-xs text-gray-500">Faculty</p>
                      <p class="font-medium">{{ conflict.faculty_name }}</p>
                    </div>

                    <div>
                      <p class="text-xs text-gray-500">Section</p>
                      <p class="font-medium">
                        {{ conflict.program_name }}-{{ conflict.set_name }}
                      </p>
                    </div>

                    <div>
                      <p class="text-xs text-gray-500">Room</p>
                      <p class="font-medium">{{ conflict.room_name }}</p>
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Type</p>
                      <p class="font-medium">{{ conflict.room_type }}</p>
                    </div>

                    <div>
                      <p class="text-xs text-gray-500">Time</p>
                      <p class="font-medium">
                        {{ formatTime(conflict.start_hour) }} –
                        {{
                          formatTime(conflict.start_hour + conflict.duration)
                        }}
                      </p>
                    </div>

                    <div>
                      <p class="text-xs text-gray-500">Day</p>
                      <p class="font-medium">{{ conflict.day }}</p>
                    </div>
                  </div>

                  <div
                    class="mt-2 p-2 rounded-lg bg-red-50 text-xs text-red-700 flex gap-2"
                  >
                    ⚠ {{ conflict.reason || "Schedule overlap detected" }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex justify-end mt-5">
          <button
            @click="closeConflictModal"
            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- TODO CONFIRM DELETE MODAL -->
    <div
      v-if="showConfirmDelete"
      class="fixed inset-0 flex items-center justify-center bg-black/30 z-50"
    >
      <div class="bg-white rounded-2xl shadow-2xl p-6 w-96">
        <!-- TODO  Header -->
        <div class="flex justify-between items-center border-b pb-3 mb-4">
          <div class="flex gap-1 items-center">
            <icon
              name="exclamation-circle"
              class="text-red-900 w-7 p-1 rounded-full bg-red-200"
            />
            <h3 class="text-lg font-semibold text-gray-800">Confirm Delete</h3>
          </div>

          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 transition"
          >
            ✕
          </button>
        </div>

        <!-- TODO  Message -->
        <p class="text-gray-600 mb-6">
          Are you sure you want to delete this schedule?
          <strong>This action cannot be undone!</strong>
        </p>

        <!-- TODO  Buttons -->
        <div class="flex justify-center gap-2 text-sm">
          <button
            @click="cancelDelete"
            class="px-4 py-2 border rounded-xl hover:bg-gray-100 transition"
          >
            Cancel
          </button>
          <button
            @click="confirmDelete"
            class="px-4 py-2 bg-red-500 text-white rounded-xl hover:bg-red-600 transition"
          >
            Yes, Delete
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
      // 8 AM to 8 PM
      timeSlots: Array.from({ length: 13 }, (_, i) => ({
        start: 8 + i,
        end: 9 + i,
      })),
      selectedSchedule: {},
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

      deletedIds: new Set(),
      highlightedRecordId: null,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rooms"]),
    sortedLocalData() {
      const dayOrder = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ];

      return [...this.localData].sort((a, b) => {
        const dayA = dayOrder.indexOf(a.day);
        const dayB = dayOrder.indexOf(b.day);

        // Unknown days go last
        if (dayA === -1 && dayB === -1) return 0;
        if (dayA === -1) return 1;
        if (dayB === -1) return -1;

        // Sort by day first
        if (dayA !== dayB) return dayA - dayB;

        // Then sort by start time
        return (a.start_hour ?? 0) - (b.start_hour ?? 0);
      });
    },

    coursesList() {
      const store = useFetchDataStore();
      return store.courses || [];
    }, // Total units per faculty
    facultyTotalUnits() {
      const result = {};

      Object.entries(this.groupedSchedule).forEach(([faculty, schedules]) => {
        let totalLecture = 0;
        let totalLab = 0;

        schedules.forEach((sched) => {
          const course = this.coursesList.find(
            (c) => c.course_code === sched.course_code,
          );
          if (course) {
            if (sched.type === "Lecture") {
              totalLecture += Number(course.course_lec || 0);
            } else if (sched.type === "Laboratory") {
              totalLab += Number(course.course_lab || 0);
            }
          }
        });

        const totalUnits = totalLecture + totalLab;

        result[faculty] = {
          lectureUnits: totalLecture,
          labUnits: totalLab,
          totalUnits,
        };
      });

      return result;
    },
    unscheduledCourses() {
      const scheduledCourseIds = new Set(
        this.localData.map((r) => r.course_id).filter(Boolean),
      );

      const fetchDataStore = useFetchDataStore();

      let courses = fetchDataStore.courses.filter(
        (c) => !scheduledCourseIds.has(c.course_id),
      );

      // Only show courses matching user's institute & program if Program Chairperson
      if (this.user.role === "Program Chairperson") {
        courses = courses.filter(
          (c) =>
            c.institute_id === this.user.institute_id &&
            c.program_id === this.user.program_id,
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
      const merged = [...this.localData];

      const localKeys = new Set(this.localData.map((r) => r.id || r.tempId));

      (this.fullSchedules || []).forEach((r) => {
        const key = r.id || r.tempId;
        if (!localKeys.has(key)) {
          merged.push({
            ...r,
            searchRoomQuery: r.room_name || "",
            showRoomDropdown: false,
            searchCourseQuery: r.course_code || "",
            showCourseDropdown: false,
            searchSectionQuery: r.set_name || "",
            showSectionDropdown: false,
          });
        }
      });

      return merged;
    },
  },
  watch: {
    // Watch for changes in instructorData to update localData
    instructorData: {
      immediate: true,
      handler(newVal) {
        const fetchDataStore = useFetchDataStore();
        const sections = fetchDataStore.sections || [];

        // Create fresh reactive copy
        this.localData = (newVal || []).map((rec) => {
          const class_size =
            rec.class_size ||
            (rec.class_id
              ? sections.find((s) => s.class_id === rec.class_id)?.class_size
              : null);

          return {
            ...rec,
            class_size,
            searchRoomQuery: rec.room_name || "",
            showRoomDropdown: false,
            searchCourseQuery: rec.course_code || "",
            showCourseDropdown: false,
            searchSectionQuery: rec.set_name || "",
            showSectionDropdown: false,
            program_id: rec.program_id || this.user.program_id || null,
            institute_id: rec.institute_id || this.user.institute_id || null,
          };
        });

        // Reset drag state to prevent false conflicts
        this.draggedRecord = null;
      },
    },

    // Watch for modal open (show = true) to refresh all data
    show: {
      immediate: false,
      handler(isVisible) {
        if (isVisible) {
          // Refresh user info
          this.fetchUser();

          // Refresh Pinia stores
          this.fetchRooms();
          this.fetchClassSections();

          // Reload full schedules from API
          this.loadData();

          // Refresh localData to sync with parent props
          this.refreshInstructorData([...this.instructorData]);
        }
      },
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, [
      "fetchRooms",
      "fetchCourses",
      "fetchClassSections",
    ]),
    /* ------------------ 1. UTILITY ------------------ */ // called whenever mode changes

    sanitizePayload(record) {
      const allowed = [
        "class_id",
        "course_id",
        "program_id",
        "institute_id",
        "type",
        "day",
        "start_hour",
        "duration",

        "room_id",
        "room_type",
        "room_capacity",
        "class_size",
        "faculty_id",
        "school_year",
        "semester",
        "mode",
      ];

      const payload = {};

      allowed.forEach((key) => {
        if (record[key] !== undefined) {
          payload[key] = record[key];
        }
      });

      return payload;
    },
    highlightRow(item) {
      this.highlightedRecordId = item.id || item.tempId;
      // optional: scroll to the row
      this.$nextTick(() => {
        const el = document.getElementById(`row-${this.highlightedRecordId}`);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    },
    onModeChange(record) {
      if ((record.mode || "").toLowerCase() === "online") {
        record.room_id = null;
        record.room_name = "None";
        record.room_type = null;
        record.room_capacity = null;
        record.searchRoomQuery = "None";
      } else {
        record.room_name = "";
        record.searchRoomQuery = "";
      }
    },
    normalizeHour(hour) {
      const h = Number(hour);
      if (Number.isNaN(h)) return null;
      return h; // ✅ already 24-hour based
    },
    formatTime(h) {
      if (h == null) return "";
      const hour = Math.floor(h); // integer hour
      const minutes = Math.round((h - hour) * 60); // decimal -> minutes
      const period = hour >= 12 ? "PM" : "AM";
      const hour12 = hour % 12 || 12;
      const minutesStr = minutes.toString().padStart(2, "0");
      return `${hour12}:${minutesStr} ${period}`;
    },
    isStartingSlot(item, slot) {
      return item.start_hour >= slot.start && item.start_hour < slot.end;
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

    /* ------------------ 2. FETCHING ------------------ */
    async loadData() {
      try {
        const fetchDataStore = useFetchDataStore();
        await fetchDataStore.fetchFinalSchedules();
        this.fullSchedules = (fetchDataStore.final_schedules || []).map(
          (rec) => {
            const cloned = JSON.parse(JSON.stringify(rec)); // deep clone
            if (!cloned.id && !cloned.tempId) {
              cloned.tempId = `temp-${Date.now()}-${Math.floor(
                Math.random() * 1000,
              )}`;
            }
            return {
              ...cloned,
              searchRoomQuery: cloned.room_name || "",
              showRoomDropdown: false,
              searchCourseQuery: cloned.course_code || "",
              showCourseDropdown: false,
              searchSectionQuery: cloned.set_name || "",
              showSectionDropdown: false,
            };
          },
        );
      } catch (error) {
        console.error("Failed to load full schedules:", error);
        this.fullSchedules = [];
      }
    },

    async fetchUser() {
      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/auth/me`,
          {
            withCredentials: true,
          },
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
    refreshInstructorData(newData) {
      this.localData = (newData || []).map((rec) => {
        const cloned = JSON.parse(JSON.stringify(rec)); // deep clone
        if (!cloned.id && !cloned.tempId) {
          cloned.tempId = `temp-${Date.now()}-${Math.floor(
            Math.random() * 1000,
          )}`;
        }
        return {
          ...cloned,
          searchRoomQuery: cloned.room_name || "",
          showRoomDropdown: false,
          searchCourseQuery: cloned.course_code || "",
          showCourseDropdown: false,
          searchSectionQuery: cloned.set_name || "",
          showSectionDropdown: false,
        };
      });

      // Reset drag state
      this.draggedRecord = null;
    },

    openAddSchedulePanel(instructor) {
      this.selectedInstructorName = instructor;
      this.showAddSchedulePanel = true;
    },
    closeAddSchedulePanel() {
      this.showAddSchedulePanel = false;
    },

    /* ------------------ 3. FILTERING ------------------ */

    filteredRooms(record) {
      if (!record.searchRoomQuery) return this.rooms;
      return this.rooms.filter((r) =>
        r.room_name
          .toLowerCase()
          .includes(record.searchRoomQuery.toLowerCase()),
      );
    },
    filteredSections(record) {
      const fetchDataStore = useFetchDataStore();
      const sections = fetchDataStore.sections || [];

      let filtered = sections;

      // If user is Program Chairperson, filter by institute & program
      if (this.user.role === "Program Chairperson") {
        filtered = filtered.filter(
          (s) =>
            s.program?.institute?.institute_id === this.user.institute_id &&
            s.program_id === this.user.program_id,
        );
      }
      const query = record.searchSectionQuery?.trim().toLowerCase();
      if (query) {
        filtered = filtered.filter((s) =>
          s.set_name?.toLowerCase().includes(query),
        );
      }

      return filtered;
    },

    filteredCourses(record) {
      const fetchDataStore = useFetchDataStore();
      if (!fetchDataStore.courses) return [];

      let filtered = fetchDataStore.courses.filter((c) =>
        c.course_code
          .toLowerCase()
          .includes(record.searchCourseQuery.toLowerCase()),
      );

      // Only show courses matching user's institute & program if Program Chairperson
      if (this.user.role === "Program Chairperson") {
        filtered = filtered.filter(
          (c) =>
            c.institute_id === this.user.institute_id &&
            c.program_id === this.user.program_id,
        );
      }

      return filtered;
    },
    /* ------------------ 4. SELECT ACTIONS ------------- */

    selectSection(record, section) {
      record.class_id = section.class_id;
      record.set_name = section.set_name;
      record.program_id = section.program?.program_id || null;
      record.institute_id = section.program?.institute?.institute_id || null;

      record.searchSectionQuery = section.set_name;
      record.showSectionDropdown = false;
    },

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
      record.semester = String(course.course_semester);

      const startYear = course?.curriculum?.curriculum_start_year;
      const endYear = course?.curriculum?.curriculum_end_year;
      record.school_year =
        startYear && endYear ? `${startYear} - ${endYear}` : startYear || "";

      record.searchCourseQuery = course.course_code;
      record.showCourseDropdown = false;
    },
    /* ------------------ 5. ROW MANAGEMENT ------------- */

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
        isNew: true, // <-- mark as new
        faculty_name: first?.faculty_name || "TBD",
        faculty_id: first?.faculty_id || null,
        class_id,
        class_size,
        mode: "face to face",
        day: "Monday",
        start_hour: startHour,
        duration: Math.floor(duration),
        time_slot: `${formatTime(startHour)} - ${formatTime(
          startHour + duration,
        )}`,

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
        searchSectionQuery: "",
        showSectionDropdown: false,
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
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${this.deleteTarget.id}`,
        );

        // After removing locally
        this.localData = this.localData.filter(
          (item) => item.id !== this.deleteTarget.id,
        );

        this.$emit("deleted", this.deleteTarget.id);
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
    /* ------------------ 6. SCHEDULE GRID -------------- */
    getConflictsInCell(slot, day, instructor) {
      const cellRecords = this.getScheduleForCell(slot, day, instructor);
      return cellRecords
        .map((r) => this.getConflictingRecords(r))
        .flat()
        .filter((r) => r.faculty_name !== instructor);
    },
    getConflictingRecords(record) {
      const recordStart = this.normalizeHour(record.start_hour);
      const recordEnd = recordStart + Number(record.duration);

      return this.allData
        .map((r) => {
          // Ignore self
          if (
            (r.id && record.id && r.id === record.id) ||
            (r.tempId && record.tempId && r.tempId === record.tempId)
          )
            return null;

          // Same day only
          if (r.day !== record.day) return null;

          const rStart = this.normalizeHour(r.start_hour);
          const rEnd = rStart + Number(r.duration);

          // No time overlap
          if (Math.max(rStart, recordStart) >= Math.min(rEnd, recordEnd))
            return null;

          // Determine conflict reason
          let reason = [];
          if (r.class_id && record.class_id && r.class_id === record.class_id)
            reason.push("Same set and section in the same day and time!");
          if (
            record.mode === "face to face" &&
            r.mode === "face to face" &&
            r.room_id &&
            record.room_id &&
            r.room_id === record.room_id
          )
            reason.push("Same Room");
          if (
            r.faculty_id === record.faculty_id &&
            (r.mode || "").toLowerCase() === (record.mode || "").toLowerCase()
          )
            reason.push("Same Faculty and Same Mode");

          if (!reason.length) return null;

          return {
            ...r,
            reason: reason.join(", "),
          };
        })
        .filter(Boolean);
    },
    openConflictModal(record) {
      this.selectedSchedule = {
        ...record,
        time_start: record.start_hour ?? 0,
        time_end: (record.start_hour ?? 0) + (record.duration ?? 0),
        course_code: record.course_code || "N/A",
        faculty_name: record.faculty_name || "TBD",
        set_name: record.set_name || "TBD",
        room_name: record.room_name || "TBD",
        day: record.day || "TBD",
        mode: record.mode || "face to face",
      };

      this.conflictRecords = this.getConflictingRecords(record);
      this.conflictModalVisible = true;
    },
    closeConflictModal() {
      this.conflictModalVisible = false;
      this.conflictRecords = [];
    },

    /* ------------------ 7. CONFLICT LOGIC ------------- */

    hasRoomConflict(record) {
      return this.getConflictingRecords(record).length > 0;
    },

    getConflictTooltip(record) {
      const conflicts = this.getConflictingRecords(record);
      if (!conflicts.length) return "";
      return conflicts
        .map(
          (c) =>
            `Conflict with: ${c.faculty_name} (${c.course_code}) in ${c.room_name}`,
        )
        .join("\n");
    },

    getScheduleForCell(slot, day, instructor) {
      return (this.localData || []).filter(
        (r) =>
          r.faculty_name === instructor &&
          r.day === day &&
          r.start_hour != null &&
          r.duration != null &&
          r.start_hour < slot.end &&
          r.start_hour + r.duration > slot.start,
      );
    },
    isValid() {
      return this.localData.every(
        (r) =>
          r.faculty_name &&
          r.day &&
          r.start_hour != null &&
          r.duration != null &&
          !this.hasRoomConflict(r),
      );
    },

    /* ------------------ 8. DRAG & DROP ---------------- */
    getConflictsForDrag(record, targetInstructor, targetDay, targetStartHour) {
      const clonedRecord = { ...record };
      clonedRecord.faculty_name = targetInstructor;
      clonedRecord.day = targetDay;
      clonedRecord.start_hour = targetStartHour;

      return this.getConflictingRecords(clonedRecord);
    },
    onDragOver(event, instructor, day, slotStart) {
      if (!this.draggedRecord) return;
      this.previewX = event.clientX + 12;
      this.previewY = event.clientY + 12;
      this.conflictPreview = this.getConflictsForDrag(
        this.draggedRecord,
        instructor,
        day,
        slotStart,
      );
    },
    onDragStart(event, record) {
      this.draggedRecord = record;
      event.dataTransfer.effectAllowed = "move";
    },

    async onDrop(event, targetInstructor, targetDay, targetStartHour) {
      if (!this.draggedRecord) return;

      // Create temporary record for new position
      const tempRecord = {
        ...this.draggedRecord,
        faculty_name: targetInstructor,
        day: targetDay,
        start_hour: targetStartHour,
        mode: this.draggedRecord.mode,
      };

      // Check for conflicts
      const conflicts = this.getConflictingRecords(tempRecord);
      if (conflicts.length) {
        // ✅ Set the dragged record as the selected schedule in conflict modal
        this.selectedSchedule = {
          ...tempRecord,
          time_start: tempRecord.start_hour ?? 0,
          time_end: (tempRecord.start_hour ?? 0) + (tempRecord.duration ?? 0),
          course_code: tempRecord.course_code || "N/A",
          faculty_name: tempRecord.faculty_name || "TBD",
          set_name: tempRecord.set_name || "TBD",
          room_name: tempRecord.room_name || "TBD",
          day: tempRecord.day || "TBD",
          mode: tempRecord.mode || "face to face",
        };

        this.conflictRecords = conflicts;
        this.conflictModalVisible = true;
        this.draggedRecord = null;
        return; // do not move
      }

      // Check if target cell has a record to swap
      const targetRecord = this.localData.find(
        (r) =>
          r.faculty_name === targetInstructor &&
          r.day === targetDay &&
          r.start_hour === targetStartHour,
      );

      if (targetRecord) {
        // Swap records
        const temp = {
          day: targetRecord.day,
          start_hour: targetRecord.start_hour,
          faculty_name: targetRecord.faculty_name,
        };

        Object.assign(targetRecord, {
          day: this.draggedRecord.day,
          start_hour: this.draggedRecord.start_hour,
          faculty_name: this.draggedRecord.faculty_name,
          mode: this.draggedRecord.mode || "face to face",
        });

        Object.assign(this.draggedRecord, temp);

        // PATCH both records
        await Promise.all(
          [targetRecord, this.draggedRecord].map(async (rec) => {
            const payload = this.sanitizePayload(rec);
            delete payload.searchRoomQuery;
            delete payload.showRoomDropdown;
            delete payload.searchCourseQuery;
            delete payload.showCourseDropdown;
            delete payload.searchSectionQuery;
            delete payload.showSectionDropdown;
            const id = rec.id || rec.schedule_id || rec.final_generated_id;
            if (!id) return;
            try {
              await axios.patch(
                `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
                payload,
              );
            } catch (error) {
              console.error("Failed to update schedule:", error);
              toast.error("Failed to update schedule.");
            }
          }),
        );
      } else {
        // Move dragged record to empty cell
        Object.assign(this.draggedRecord, {
          faculty_name: targetInstructor,
          day: targetDay,
          start_hour: targetStartHour,
        });

        const payload = this.sanitizePayload(this.draggedRecord);
        delete payload.searchRoomQuery;
        delete payload.showRoomDropdown;
        delete payload.searchCourseQuery;
        delete payload.showCourseDropdown;
        delete payload.searchSectionQuery;
        delete payload.showSectionDropdown;

        const id =
          this.draggedRecord.id ||
          this.draggedRecord.schedule_id ||
          this.draggedRecord.final_generated_id;
        if (id) {
          try {
            await axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
              payload,
            );
          } catch (error) {
            console.error("Failed to update schedule:", error);
            toast.error("Failed to update schedule.");
          }
        }
      }

      this.draggedRecord = null; // reset drag state
    },
    /* ------------------ 9. SAVING TO DATABASE  ---------------- */
    async saveEdit() {
      this.saving = true;

      try {
        // Remove duplicates
        const seen = new Set();
        this.localData = this.localData.filter((record) => {
          const key =
            record.id ||
            record.tempId ||
            `${record.course_id}|${record.room_id}|${record.class_id}|${record.mode}|${record.day}|${record.start_hour}|${record.faculty_id}`;
          if (seen.has(key)) return false;
          seen.add(key);
          return true;
        });

        const newRows = [];
        const existingRows = [];

        this.localData.forEach((record) => {
          // 🔒 SANITIZE PAYLOAD HERE
          const payload = this.sanitizePayload({
            ...record,
            mode:
              record.mode?.toLowerCase() === "online"
                ? "online"
                : "face to face",
          });

          const existingId =
            record.id || record.schedule_id || record.final_generated_id;

          if (existingId) {
            existingRows.push({ id: existingId, payload });
          } else {
            newRows.push(payload);
          }
        });

        // ➕ Create new schedules
        if (newRows.length) {
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/bulk`,
            newRows,
          );
        }

        // ✏️ Update existing schedules
        if (existingRows.length) {
          await Promise.all(
            existingRows.map(({ id, payload }) =>
              axios.patch(
                `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
                payload,
              ),
            ),
          );
        }

        // 🔄 Refresh schedules
        const fetchDataStore = useFetchDataStore();
        await fetchDataStore.fetchFinalSchedules();

        this.localData = (fetchDataStore.final_schedules || []).map((rec) => ({
          ...rec,
          searchRoomQuery: rec.room_name || "",
          showRoomDropdown: false,
          searchCourseQuery: rec.course_code || "",
          showCourseDropdown: false,
          searchSectionQuery: rec.set_name || "",
          showSectionDropdown: false,
        }));

        toast.success("Schedules saved successfully!");
        this.$emit("saved", this.localData);
        this.$emit("close");
      } catch (err) {
        console.error("Failed to save schedules:", err.response?.data || err);
        toast.error("Failed to save schedules. Check console for details.");
      } finally {
        this.saving = false;
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
