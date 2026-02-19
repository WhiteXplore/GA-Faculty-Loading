<template>
  <div class="flex flex-col h-[82vh]">
    <!-- TODO  Top Controls -->

    <FacultyTopControls
      v-model:isJoined="isJoined"
      :showFacultyTable="showFacultyTable"
      :showCompareSelection="showCompareSelection"
      v-model:compareInstructorA="compareInstructorA"
      v-model:compareInstructorB="compareInstructorB"
      :instructorList="Object.keys(groupedSchedule)"
      @toggleFacultyTable="showFacultyTable = !showFacultyTable"
      @toggleCompareSelection="toggleShowCompareSelection"
      @compare="showCompareFacultyCards"
      @backFromCompare="backFromCompare"
    />

    <div class="flex flex-wrap items-center gap-4 px-2">
      <!-- TODO  Back Button -->
      <button
        v-if="
          !showFacultyTable && Object.keys(filteredGroupedSchedule).length === 1
        "
        @click="backToFacultyTable"
        class="flex items-center gap-2 px-4 py-2 border border-gray-400 rounded-xl shadow-sm hover:bg-gray-100 transition"
      >
        <icon name="arrow-left" class="w-4 h-4" />
        <span class="font-medium text-sm">Back to Table</span>
      </button>
    </div>

    <!-- TODO  Scrollable Content -->
    <div class="flex-1 overflow-y-auto">
      <!-- TODO  Faculty Table -->
      <div v-if="showFacultyTable">
        <div class="overflow-x-auto border p-3 rounded-xl bg-white">
          <div
            class="flex justify-between items-center flex-wrap gap-3 text-gray-700 bg-white"
          >
            <!-- TODO  Items per page -->
            <div class="flex items-center gap-2">
              <div class="relative">
                <select
                  v-model="itemsPerPage"
                  class="appearance-none rounded-full border border-green-600 bg-white px-3 py-1 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
                  @change="changePage(1)"
                >
                  <option value="10">10</option>
                  <option value="15">15</option>
                  <option value="20">20</option>
                </select>
                <div
                  class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-defaultGreen"
                >
                  <svg
                    class="w-4 h-4"
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
              <span class="text-sm font-medium text-gray-600">Per page</span>
            </div>

            <!-- TODO  Search -->
            <div class="relative w-full sm:w-64 md:w-72 lg:w-80">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search faculty..."
                class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
                @input="changePage(1)"
              />
              <div
                class="absolute inset-y-0 left-3 flex items-center text-defaultGreen pointer-events-none"
              >
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <circle cx="11" cy="11" r="8" />
                  <path d="M21 21l-4.35-4.35" />
                </svg>
              </div>
            </div>
          </div>

          <!-- TODO  Faculty Table -->
          <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
            <div class="max-h-[69vh] overflow-y-auto">
              <table class="min-w-full text-sm text-gray-700 border-collapse">
                <thead
                  class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
                >
                  <tr>
                    <th
                      class="px-5 py-3 text-left font-semibold whitespace-nowrap"
                    >
                      Faculty Name
                    </th>
                    <th
                      class="px-5 py-3 text-center font-semibold w-[150px] whitespace-nowrap"
                    >
                      Action
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(slots, instructor) in paginatedFaculty"
                    :key="instructor"
                    class="hover:bg-green-50 border-t transition-colors"
                  >
                    <td
                      class="px-5 py-3 font-medium text-gray-800 whitespace-nowrap"
                    >
                      {{ instructor }}
                    </td>
                    <td class="px-5 py-3 text-center">
                      <button
                        @click="viewFacultySchedule(instructor)"
                        class="flex items-center justify-center gap-1 mx-auto px-3 py-1.5 border border-blue-400 text-blue-700 hover:bg-blue-100 rounded-lg text-sm font-medium transition"
                      >
                        <icon name="eye" class="w-4 h-4" /> View
                      </button>
                    </td>
                  </tr>
                  <tr
                    v-if="!Object.keys(filteredGroupedSchedule).length"
                    class="text-center bg-gray-50"
                  >
                    <td colspan="2" class="py-5 text-gray-500">
                      No faculty found.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- TODO  Pagination -->
          <div class="flex justify-between items-center mt-4">
            <div class="text-gray-700 text-sm">
              Showing {{ startIndex }} to {{ endIndex }} of
              {{ Object.keys(filteredGroupedSchedule).length }} faculty
            </div>

            <div class="flex items-center gap-1">
              <!-- Previous -->
              <button
                @click="changePage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400 disabled:opacity-50"
              >
                &lt;
              </button>

              <!-- Page Numbers -->
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

              <!-- Next -->
              <button
                @click="changePage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400 disabled:opacity-50"
              >
                &gt;
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- TODO  Faculty Cards -->
      <div
        v-else
        :class="[
          'gap-3 grid p-2 h-auto',
          showCompareView
            ? 'grid-cols-1 md:grid-cols-2 h-[87vh] overflow-y-auto'
            : Object.keys(filteredGroupedSchedule).length === 1
            ? 'grid-cols-1'
            : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-2  overflow-y-auto',
        ]"
      >
        <div
          v-for="(records, instructor) in paginatedFacultyCards"
          :key="instructor"
          class="bg-white rounded-xl border flex flex-col shadow-sm overflow-hidden"
        >
          <!-- Header -->
          <div
            class="flex justify-between items-center bg-defaultGreen text-white px-4 py-3 font-semibold text-sm rounded-t-xl"
          >
            <div class="flex flex-col">
              <span class="text-lg font-bold">{{ instructor }}</span>

              <div v-if="facultyTotalUnits[instructor]">
                <p class="font-normal">
                  Total Units:
                  {{ facultyTotalUnits[instructor].totalUnits }}
                </p>
              </div>
            </div>

            <button
              @click="openEditInstructorModal(instructor)"
              class="border border-white hover:bg-white hover:text-defaultGreen text-white px-3 py-1 rounded-full text-xs transition"
            >
              Edit
            </button>
          </div>

          <!-- Table wrapper -->
          <div class="overflow-x-auto overflow-y-auto flex-1">
            <table class="w-full text-left border-collapse text-[11px]">
              <thead class="sticky top-0 bg-gray-100 z-10">
                <tr class="text-gray-700">
                  <th class="px-4 py-2 border border-gray-200 w-24 text-center">
                    Time
                  </th>
                  <th
                    v-for="day in days"
                    :key="day"
                    class="px-4 py-2 border border-gray-200 text-center w-28"
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
                  :style="{ height: timeSlotHeight + 'px' }"
                >
                  <!-- Time Column -->
                  <td
                    class="px-4 py-4 border text-center font-medium whitespace-nowrap"
                  >
                    {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                  </td>

                  <!-- Schedule Cells -->
                  <td
                    v-for="day in days"
                    :key="day"
                    class="relative border p-0 overflow-visible transition-colors"
                    :class="{
                      'bg-green-100':
                        isJoined &&
                        draggedRecord &&
                        getJoinableSchedules(draggedRecord).some(
                          (j) => j.day === day,
                        ),
                      'bg-red-100':
                        draggedRecord &&
                        getConflictsForDrag(
                          draggedRecord,
                          instructor,
                          day,
                          slot.start,
                        ).length,
                    }"
                    @dragover.prevent
                    @drop="onDrop($event, instructor, day, slot.start)"
                  >
                    <template
                      v-for="item in getScheduleForCell(slot, day, instructor)"
                      :key="
                        item.id ||
                        item.course_code + item.start_hour + item.room_name
                      "
                    >
                      <div
                        v-if="isStartingSlot(item, slot)"
                        :draggable="
                          !(isJoined && Number(item.class_size) >= 30)
                        "
                        @dblclick.stop="handleUnjoin(item)"
                        @dragstart="onDragStart($event, item)"
                        @mouseenter="showScheduleTooltip($event, item)"
                        @mouseleave="hideScheduleTooltip"
                        :class="[
                          'absolute inset-x-1 border rounded-lg text-[11px] p-1 shadow-sm cursor-pointer overflow-hidden transition-all duration-200 whitespace-nowrap',
                          item.id?.toString().startsWith('temp-')
                            ? 'bg-purple-200 border-purple-400 text-purple-900'
                            : getTypeColor(item.type),
                          hasRoomConflict(item) && !isJoined
                            ? 'bg-red-300 border-red-500 text-red-900'
                            : '',
                          swapSelection.includes(item)
                            ? 'border-yellow-500 bg-yellow-100'
                            : '',
                          item.is_joined ? 'bg-blue-100 border-blue-400' : '',
                          isJoined && Number(item.class_size) >= 30
                            ? 'opacity-50 pointer-events-none cursor-not-allowed'
                            : '',
                          'hover:bg-yellow-100',
                        ]"
                        :style="{
                          top: getBlockTop(item, slot.start) + 'px',
                          height: getBlockHeight(item) + 'px',
                          width: 'calc(100% - 0.5rem)',
                          zIndex: 10,
                        }"
                      >
                        <!-- Mode Badge -->
                        <span
                          v-if="item.mode"
                          :class="[
                            'absolute top-2 right-2 w-auto h-4 px-1 rounded-full text-[10px] font-bold flex items-center justify-center text-white',
                            item.mode === 'face to face' ? 'bg-orange-500' : '',
                            item.mode === 'online' ? 'bg-purple-500' : '',
                          ]"
                        >
                          {{ item.mode === "face to face" ? "F2F" : "OL" }}
                        </span>

                        <!-- Join Badge -->
                        <span
                          v-if="item.is_joined"
                          class="absolute bottom-2 right-2 px-2 h-5 flex items-center justify-center bg-blue-600 text-white text-[10px] font-bold rounded-full shadow"
                        >
                          J
                        </span>

                        <!-- Course Info -->
                        <div class="truncate font-semibold">
                          {{ item.course_code }}
                        </div>
                        <div class="truncate">{{ item.room_name }}</div>
                        <div class="truncate">
                          <template v-if="item.is_joined && item.join_group_id">
                            {{
                              finalSchedules
                                .filter(
                                  (s) => s.join_group_id === item.join_group_id,
                                )
                                .map((s) => s.set_name)
                                .join(" + ")
                            }}
                          </template>
                          <template v-else>
                            {{ item.program_name }}-{{ item.set_name }}
                          </template>
                        </div>

                        <!-- Conflict Button -->
                        <div class="w-full flex justify-center mt-1">
                          <button
                            v-if="hasRoomConflict(item) && !isJoined"
                            @click.stop="openConflictModal(item)"
                            class="px-2 h-5 text-[10px] bg-red-100 text-red-600 rounded"
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
            <!-- 🔍 Schedule Tooltip -->
            <div
              v-if="scheduleTooltipVisible && tooltipItem"
              class="fixed z-[9999] pointer-events-none"
              :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
            >
              <div
                class="bg-white border border-gray-300 rounded-xl p-3 scale-125 origin-top-left"
              >
                <div
                  class="flex items-center justify-between gap-2 mb-2 w-full"
                >
                  <!-- Course Code -->
                  <div class="text-sm font-bold text-defaultGreen leading-none">
                    {{ tooltipItem.course_code }}
                  </div>

                  <!-- Schedule Type Badge -->
                  <span
                    v-if="tooltipItem.mode"
                    class="inline-flex items-center justify-center px-2 py-1 text-[8px] leading-none rounded-full text-white"
                    :class="
                      tooltipItem.mode === 'face to face'
                        ? 'bg-orange-500'
                        : 'bg-purple-500'
                    "
                  >
                    {{
                      tooltipItem.mode === "face to face"
                        ? "Face to Face"
                        : "Online"
                    }}
                  </span>
                </div>

                <div class="text-[10px] text-gray-700 space-y-0.5">
                  <p>
                    <strong>Faculty:</strong> {{ tooltipItem.faculty_name }}
                  </p>

                  <p><strong>Year & Section:</strong></p>
                  <ul class="ml-2 list-disc">
                    <template
                      v-if="tooltipItem.is_joined && tooltipItem.join_group_id"
                    >
                      <li
                        v-for="s in finalSchedules.filter(
                          (s) => s.join_group_id === tooltipItem.join_group_id,
                        )"
                        :key="s.class_id"
                      >
                        {{ s.program_name }} - {{ s.set_name }} (Class Size:
                        {{ s.class_size }})
                      </li>
                    </template>
                    <template v-else>
                      <li>
                        {{ tooltipItem.program_name }} -
                        {{ tooltipItem.set_name }} (Class Size:
                        {{ tooltipItem.class_size }})
                      </li>
                    </template>
                  </ul>

                  <p><strong>Room:</strong> {{ tooltipItem.room_name }}</p>
                  <p><strong>Day:</strong> {{ tooltipItem.day }}</p>
                  <p>
                    <strong>Time:</strong>
                    {{ formatTime(tooltipItem.start_hour) }} –
                    {{
                      formatTime(
                        tooltipItem.start_hour + Number(tooltipItem.duration),
                      )
                    }}
                  </p>
                  <p><strong>Type:</strong> {{ tooltipItem.type }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-if="!showFacultyTable && totalCardPages > 1"
        class="flex justify-center items-center gap-2 mt-4 w-full"
      >
        <button
          @click="currentCardPage--"
          :disabled="currentCardPage === 1"
          class="px-3 py-1 rounded-lg bg-gray-200 disabled:opacity-50"
        >
          &lt;
        </button>

        <span class="text-sm font-medium text-gray-600">
          Page {{ currentCardPage }} of {{ totalCardPages }}
        </span>

        <button
          @click="currentCardPage++"
          :disabled="currentCardPage === totalCardPages"
          class="px-3 py-1 rounded-lg bg-gray-200 disabled:opacity-50"
        >
          &gt;
        </button>
      </div>
    </div>
  </div>
  <!-- Conflict Modal -->
  <ConflictModal
    :visible="conflictModalVisible"
    :schedule="selectedSchedule"
    :conflicts="conflictRecords"
    @close="conflictModalVisible = false"
  />
  <!-- JOIN VALIDATION MODAL -->
  <!-- JOIN VALIDATION MODAL -->
  <div
    v-if="joinValidationModalVisible"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
  >
    <div
      class="bg-white w-[480px] rounded-2xl shadow-2xl p-6 relative animate-slideUp"
    >
      <!-- Header -->
      <div class="flex items-center justify-between border-b pb-3 mb-4">
        <div class="flex items-center gap-2">
          <icon
            name="exclamation-circle"
            class="w-7 h-7 p-1 rounded-full bg-yellow-200 text-yellow-900 flex items-center justify-center"
          />
          <h3 class="text-lg font-semibold text-gray-800 leading-none">
            Verify Join Classes
          </h3>
        </div>
        <button
          @click="cancelJoin"
          class="text-gray-400 hover:text-gray-600 transition"
        >
          ✕
        </button>
      </div>

      <!-- Base Class Card -->
      <div class="border rounded-xl p-4 bg-gray-50 mb-4 relative">
        <div class="font-semibold text-gray-800 mb-1">
          {{ pendingJoinRecord?.course_code }}
        </div>
        <div class="text-sm text-gray-600">
          Type: {{ pendingJoinRecord?.type }}
        </div>
        <div class="text-sm text-gray-600">
          {{ pendingJoinRecord?.program_name }} -
          {{ pendingJoinRecord?.set_name }}
        </div>
        <div class="text-sm text-gray-600">
          Students: {{ pendingJoinRecord?.class_size }}
        </div>
        <div class="text-sm text-gray-600">
          Day: {{ pendingJoinRecord?.day }}
        </div>
        <div class="text-sm text-gray-600">
          Room: {{ pendingJoinRecord?.room_name || "No Room" }}
        </div>
        <div class="text-sm text-gray-600">
          Room Type: {{ pendingJoinRecord?.room_type || "No Room Type" }}
        </div>
      </div>

      <!-- Pending Join Targets -->
      <div class="space-y-3">
        <div
          v-for="target in pendingJoinTargets"
          :key="target.id"
          class="border rounded-xl p-4 bg-gray-50 relative hover:shadow-md transition-shadow"
        >
          <div class="font-semibold text-gray-800 mb-1">
            {{ target.course_code }}
          </div>
          <div class="text-sm text-gray-600">Type: {{ target.type }}</div>
          <div class="text-sm text-gray-600">
            {{ target.program_name }} - {{ target.set_name }}
          </div>
          <div class="text-sm text-gray-600">
            Students: {{ target.class_size }}
          </div>
          <div class="text-sm text-gray-600">Day: {{ target.day }}</div>
          <div class="text-sm text-gray-600">
            Room: {{ target?.room_name || "No Room" }}
          </div>
          <div class="text-sm text-gray-600">
            Room Type: {{ target?.room_type || "No Room Type" }}
          </div>
        </div>
      </div>

      <!-- Total Combined Students -->
      <div class="mt-4 text-sm font-medium text-gray-700">
        Total Combined Students:
        {{
          pendingJoinTargets.reduce(
            (sum, s) => sum + Number(s.class_size || 0),
            Number(pendingJoinRecord?.class_size || 0),
          )
        }}
      </div>

      <!-- Buttons -->
      <div class="flex justify-end mt-5 gap-3">
        <button
          @click="cancelJoin"
          class="bg-gray-200 p-2 px-3 rounded-lg text-gray-700 hover:bg-white border hover:border-gray-800 hover:text-gray-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
        >
          Cancel
        </button>

        <button
          @click="confirmJoin"
          class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-defaultGreen hover:text-defaultGreen hover:shadow-md transform transition-all duration-300 hover:scale-105"
        >
          Yes, Join
        </button>
      </div>
    </div>
  </div>

  <!-- Unjoin Confirmation Modal -->
  <UnjoinModal
    :visible="unjoinModalVisible"
    @close="cancelUnjoin"
    @confirm="confirmUnjoin"
  />

  <!-- TODO  Edit Instructor Modal -->
  <editSchedule
    :show="showEditModal"
    :instructorData="editInstructorData"
    @close="showEditModal = false"
    @saved="handleModalSaved"
    @deleted="handleDeletedSchedule"
  />
</template>

<script>
import axios from "axios";
import icon from "@/assets/icon.vue";
import { useFetchDataStore } from "@/store/fetch-data-store";
import editSchedule from "../modals/edit-schedule.vue";
import { toast } from "vue3-toastify";
import FacultyTopControls from "../faculty-components/faculty-top-controls.vue";
import ConflictModal from "../faculty-components/conflict-modal.vue";
import UnjoinModal from "../faculty-components/join-validation-modal.vue";
export default {
  name: "FacultySchedule",
  components: {
    icon,
    editSchedule,
    FacultyTopControls,
    ConflictModal,
    UnjoinModal,
  },
  data() {
    return {
      joinGroupCounter: 1,
      user: {},
      isJoined: false,
      groupedSchedule: {},
      filteredGroupedSchedule: {},
      finalSchedules: [],
      loading: false,
      error: null,
      showFacultyTable: false,
      selectedInstructor: null,
      selectedInstituteId: "",
      selectedProgramId: "",
      confirmSaveModal: false,
      days: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ],

      timeSlots: Array.from({ length: 14 }, (_, i) => ({
        start: 7 + i, // 7, 8, 9 ... 20
        end: 8 + i, // 8, 9, 10 ... 21
      })),

      progress: 0,
      progressInterval: null,

      currentPage: 1,
      itemsPerPage: 10,
      timeSlotHeight: 60,
      pageWindow: 3,
      schoolYears: [],
      swapSelection: [],
      showEditModal: false,
      editInstructorData: [],
      compareInstructorA: "",
      compareInstructorB: "",
      showCompareView: false,
      showCompareSelection: false,
      conflictModalVisible: false,
      scheduleTooltipVisible: false,
      tooltipItem: null,
      tooltipX: 0,
      tooltipY: 0,
      draggedRecord: null,
      selectedSchedule: null,
      conflictRecords: [],
      visibleCardCount: 6,
      currentCardPage: 1,
      cardsPerPage: 6,
      joinValidationModalVisible: false,
      joinTargetRecord: null,
      joinEligibleRecords: [],
      pendingJoinRecord: null,
      pendingJoinTargets: [],
      isDragging: false,
      unjoinModalVisible: false,
      unjoinTargetRecord: null,
    };
  },

  computed: {
    isDraggable(record) {
      // If Join is active and class size >= 30 → not draggable
      return !(this.isJoined && Number(record.class_size) >= 30);
    },
    paginatedFacultyCards() {
      const entries = Object.entries(this.filteredGroupedSchedule);

      // ✅ Always show both in compare mode
      if (this.showCompareView) {
        return Object.fromEntries(entries);
      }

      const start = (this.currentCardPage - 1) * this.cardsPerPage;
      const end = start + this.cardsPerPage;

      return Object.fromEntries(entries.slice(start, end));
    },
    totalCardPages() {
      return Math.ceil(
        Object.keys(this.filteredGroupedSchedule).length / this.cardsPerPage,
      );
    },
    paginatedSource() {
      if (!this.searchQuery) return this.filteredGroupedSchedule;

      const q = this.searchQuery.toLowerCase();
      return Object.fromEntries(
        Object.entries(this.filteredGroupedSchedule).filter(([name]) =>
          name.toLowerCase().includes(q),
        ),
      );
    },
    visibleFacultyCards() {
      return Object.entries(this.filteredGroupedSchedule).slice(
        0,
        this.visibleCardCount,
      );
    },

    hasMoreCards() {
      return (
        Object.keys(this.filteredGroupedSchedule).length > this.visibleCardCount
      );
    },
    coursesList() {
      const store = useFetchDataStore();
      return store.courses || [];
    }, // Total units per faculty
    facultyTotalUnits() {
      const result = {};

      Object.entries(this.filteredGroupedSchedule).forEach(
        ([faculty, schedules]) => {
          let totalLecture = 0;
          let totalLab = 0;

          schedules.forEach((sched) => {
            const course = this.coursesList.find(
              (c) => c.course_code === sched.course_code,
            );
            if (!course) return;

            const duration = Number(sched.duration || 0); // e.g., 1.5
            if (sched.type === "Lecture") {
              // Standard lecture assumed 3 hours
              const unitsPerSlot =
                (duration / 3) * Number(course.course_lec || 0);
              totalLecture += unitsPerSlot;
            } else if (sched.type === "Laboratory") {
              // Standard lab assumed 3 hours
              const unitsPerSlot =
                (duration / 3) * Number(course.course_lab || 0);
              totalLab += unitsPerSlot;
            }
          });

          result[faculty] = {
            lectureUnits: totalLecture,
            labUnits: totalLab,
            totalUnits: totalLecture + totalLab,
          };
        },
      );

      return result;
    },

    uniqueInstitutes() {
      const store = useFetchDataStore();
      const institutes = store.institutes || [];
      return Array.from(
        new Set(this.finalSchedules.map((s) => s.institute_id)),
      ).map((id) => {
        const inst = institutes.find((i) => i.institute_id === id);
        return inst
          ? { id, name: inst.institute_name }
          : { id, name: `Institute ${id}` };
      });
    },
    // Map program IDs to their names (filtered by selectedInstituteId if any)
    filteredPrograms() {
      const store = useFetchDataStore();
      const programs = store.programs || [];

      const programIds = Array.from(
        new Set(
          this.finalSchedules
            .filter((s) =>
              this.selectedInstituteId
                ? String(s.institute_id) === String(this.selectedInstituteId)
                : true,
            )
            .map((s) => s.program_id),
        ),
      );

      return programIds.map((id) => {
        const prog = programs.find((p) => String(p.program_id) === String(id));
        return prog
          ? { id, name: prog.program_name }
          : { id, name: `Program ${id}` };
      });
    },
    // Compute latest active school year dynamically
    latestActiveSchoolYear() {
      if (!this.schoolYears.length) return null;
      const activeYears = this.schoolYears.filter((y) => y.is_active);
      if (!activeYears.length) return null;
      return activeYears.reduce((latest, current) =>
        new Date(current.updated_at) > new Date(latest.updated_at)
          ? current
          : latest,
      );
    },
    totalPages() {
      return Math.ceil(
        Object.keys(this.filteredGroupedSchedule).length / this.itemsPerPage,
      );
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    endIndex() {
      return Math.min(
        this.currentPage * this.itemsPerPage,
        Object.keys(this.filteredGroupedSchedule).length,
      );
    },
    pageNumbers() {
      let pages = [];
      const halfWindow = Math.floor(this.pageWindow / 2);
      let start = Math.max(1, this.currentPage - halfWindow);
      let end = Math.min(this.totalPages, start + this.pageWindow - 1);

      // Adjust start if not enough pages at the end
      start = Math.max(1, end - this.pageWindow + 1);

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },

    paginatedFaculty() {
      const entries = Object.entries(this.paginatedSource);
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return Object.fromEntries(entries.slice(start, end));
    },

    searchedFaculty() {
      if (!this.searchQuery) return this.filteredGroupedSchedule;
      const query = this.searchQuery.toLowerCase();
      return Object.fromEntries(
        Object.entries(this.filteredGroupedSchedule).filter(([name]) =>
          name.toLowerCase().includes(query),
        ),
      );
    },
  },

  watch: {
    selectedInstituteId() {
      this.filterSchedules();
      this.selectedProgramId = "";
    },
    selectedProgramId() {
      this.filterSchedules();
    },
  },

  methods: {
    handleUnjoin(record) {
      if (!record.is_joined || !record.join_group_id) return;

      // Show modal instead of alert
      this.unjoinTargetRecord = record;
      this.unjoinModalVisible = true;
    },

    async confirmUnjoin() {
      if (!this.unjoinTargetRecord) return;

      const record = this.unjoinTargetRecord;

      // Get all records in the same join group
      const groupRecords = this.finalSchedules.filter(
        (r) => r.join_group_id === record.join_group_id,
      );

      try {
        await Promise.all(
          groupRecords.map((r) =>
            axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${r.id}`,
              {
                is_joined: false,
                join_group_id: null,
                joined_with: [],
              },
            ),
          ),
        );

        // Update local state
        this.finalSchedules = this.finalSchedules.map((r) => {
          if (r.join_group_id === record.join_group_id) {
            return {
              ...r,
              is_joined: false,
              join_group_id: null,
              joined_with: [],
            };
          }
          return r;
        });

        this.groupedSchedule = this.groupByInstructor(this.finalSchedules);
        this.filteredGroupedSchedule = { ...this.groupedSchedule };

        toast.success("Schedules successfully unjoined!");
      } catch (err) {
        console.error(err);
        toast.error("Failed to unjoin schedules.");
      } finally {
        this.unjoinModalVisible = false;
        this.unjoinTargetRecord = null;
      }
    },

    cancelUnjoin() {
      this.unjoinModalVisible = false;
      this.unjoinTargetRecord = null;
    },
    async confirmJoin() {
      if (!this.pendingJoinRecord || !this.pendingJoinTargets.length) return;

      const baseRecord = this.pendingJoinRecord;

      // 🔥 STEP 1: Filter valid join targets
      const validTargets = this.pendingJoinTargets.filter((target) => {
        const baseSet = baseRecord.set_name?.split(" ")[0];
        const targetSet = target.set_name?.split(" ")[0];

        return (
          target.course_code === baseRecord.course_code &&
          target.type === baseRecord.type &&
          target.semester === baseRecord.semester &&
          targetSet === baseSet &&
          !target.is_joined
        );
      });

      if (!validTargets.length) {
        toast.error("No valid schedules to join based on the rules.");
        this.resetJoinState();
        return;
      }

      // 🔥 STEP 2: Combine schedules
      const allToJoin = [baseRecord, ...validTargets];

      // 🔥 STEP 3: Base schedule decides final mode
      const finalMode = baseRecord.mode?.toLowerCase();

      // 🔥 STEP 4: Calculate total students using class_size ONLY
      const totalStudents = allToJoin.reduce(
        (sum, s) => sum + Number(s.class_size || 0),
        0,
      );

      console.log("Total Combined Students:", totalStudents);

      // 🚫 NO ROOM CAPACITY CHECK
      // (Completely removed as per your requirement)

      // 🔥 STEP 5: Generate join group
      const joinGroupId = baseRecord.id;
      const joinedIds = allToJoin.map((s) => s.id);

      // 🔥 STEP 6: Apply updates
      allToJoin.forEach((s) => {
        // Copy time from base
        s.day = baseRecord.day;
        s.start_hour = baseRecord.start_hour;
        s.duration = baseRecord.duration;

        // Apply final mode
        s.mode = finalMode;

        if (finalMode === "face to face") {
          // Copy room FROM BASE RECORD
          s.room_id = baseRecord.room_id || null;
          s.room_name = baseRecord.room_name || null;
          s.room_capacity = baseRecord.room_capacity || null;
          s.room_type = baseRecord.room_type || null;
        } else {
          // ONLINE → clear room
          s.room_id = null;
          s.room_name = null;
          s.room_capacity = null;
          s.room_type = null;
        }

        s.join_group_id = joinGroupId;
        s.is_joined = true;
        s.joined_with = joinedIds.filter((id) => id !== s.id);
      });

      // 🔥 STEP 7: Save to backend
      try {
        await Promise.all(
          allToJoin.map((s) =>
            axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${s.id}`,
              {
                day: s.day,
                start_hour: s.start_hour,
                duration: s.duration,
                mode: s.mode,
                room_id: s.room_id,
                room_name: s.room_name,
                room_capacity: s.room_capacity,
                room_type: s.room_type,
                join_group_id: s.join_group_id,
                is_joined: s.is_joined,
                joined_with: s.joined_with,
              },
            ),
          ),
        );

        toast.success(
          `Classes successfully joined! Total students: ${totalStudents}`,
        );
        await this.fetchFinalSchedules();
      } catch (error) {
        console.error(error);
        toast.error("Failed to save joined schedules.");
      }

      this.resetJoinState();
    },
    cancelJoin() {
      this.resetJoinState();
    },
    resetJoinState() {
      this.pendingJoinRecord = null;
      this.pendingJoinTargets = [];
      this.joinValidationModalVisible = false;
    },
    async saveScheduleMove(record) {
      try {
        await axios.patch(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${record.id}`,
          {
            faculty_id: record.faculty_id,
            faculty_name: record.faculty_name,
            day: record.day,
            start_hour: record.start_hour,
            duration: record.duration,
            room_id: record.room_id,
            room_name: record.room_name,
            mode: record.mode,
            type: record.type,
          },
        );

        toast.success("Schedule moved successfully!");
        await this.fetchFinalSchedules();
      } catch (error) {
        console.error(error);
        toast.error("Failed to save schedule.");
      }
    },
    getJoinableSchedules(baseRecord) {
      if (!baseRecord) return [];

      const extractYearLevel = (setName) => {
        if (!setName) return "";
        return setName.split(" ")[0].trim();
      };

      const baseYear = extractYearLevel(baseRecord.set_name);

      return this.finalSchedules.filter((r) => {
        if (r.id === baseRecord.id) return false;
        if (r.is_joined) return false;

        const targetYear = extractYearLevel(r.set_name);

        const modeCompatible =
          ["online", "face to face"].includes(baseRecord.mode.toLowerCase()) &&
          ["online", "face to face"].includes(r.mode.toLowerCase());

        return (
          r.course_code === baseRecord.course_code &&
          r.type === baseRecord.type &&
          r.semester === baseRecord.semester &&
          baseYear === targetYear &&
          modeCompatible &&
          Number(r.class_size) < 30 &&
          Number(baseRecord.class_size) < 30
        );
      });
    },
    canJoin(recordA, recordB) {
      if (!recordA || !recordB) return false;

      const getSetPrefix = (set_name) => set_name?.split(" ")[0] || "";

      const baseSet = getSetPrefix(recordA.set_name);
      const targetSet = getSetPrefix(recordB.set_name);

      // Join only if both classes are below 30 students
      const classSizeCheck =
        Number(recordA.class_size) < 30 && Number(recordB.class_size) < 30;
      const modeCompatible =
        ["online", "face to face"].includes(recordA.mode.toLowerCase()) &&
        ["online", "face to face"].includes(recordB.mode.toLowerCase());

      return (
        recordA.id !== recordB.id &&
        recordA.course_code === recordB.course_code &&
        recordA.type === recordB.type && // Lecture ↔ Lecture, Lab ↔ Lab
        recordA.semester === recordB.semester &&
        baseSet === targetSet &&
        classSizeCheck &&
        modeCompatible &&
        !recordB.is_joined // cannot join already joined
      );
    },

    getConflictsForDrag(record, targetInstructor, targetDay, targetStartHour) {
      const clonedRecord = { ...record };
      clonedRecord.faculty_name = targetInstructor;
      clonedRecord.day = targetDay;
      clonedRecord.start_hour = targetStartHour;

      return this.getConflictingRecords(clonedRecord);
    },
    showScheduleTooltip(event, item) {
      // ✅ Don't show tooltip while dragging
      if (this.draggedRecord) return;

      const rect = event.currentTarget.getBoundingClientRect();

      if (item.is_joined && item.join_group_id) {
        const joinedItems = this.finalSchedules.filter(
          (s) => s.join_group_id === item.join_group_id,
        );

        this.tooltipItem = {
          ...item,
          joinedItems,
        };
      } else {
        this.tooltipItem = item;
      }

      this.scheduleTooltipVisible = true;
      this.tooltipX = rect.right + 12;
      this.tooltipY = rect.top;
    },

    hideScheduleTooltip() {
      this.scheduleTooltipVisible = false;
      this.tooltipItem = null;
    },

    getConflictingRecords(record) {
      const recordStart = this.normalizeHour(record.start_hour);
      const recordEnd = recordStart + Number(record.duration);

      return this.finalSchedules
        .filter((r) => {
          if (r.id === record.id) return false;
          if (r.day !== record.day) return false;

          // Same join group → ignore
          if (
            record.is_joined &&
            r.is_joined &&
            record.join_group_id &&
            r.join_group_id &&
            record.join_group_id === r.join_group_id
          )
            return false;

          const rStart = this.normalizeHour(r.start_hour);
          const rEnd = rStart + Number(r.duration);

          const overlaps =
            Math.max(rStart, recordStart) < Math.min(rEnd, recordEnd);
          if (!overlaps) return false;

          // Same room conflict only if NOT join mode or same faculty
          if (
            r.room_id &&
            record.room_id &&
            r.room_id === record.room_id &&
            r.mode === "face to face" &&
            record.mode === "face to face"
          ) {
            if (!this.isJoined || r.faculty_id === record.faculty_id)
              return true;
          }

          // Same faculty
          if (r.faculty_id === record.faculty_id) return true;

          // Same class/section
          if (r.class_id && record.class_id && r.class_id === record.class_id)
            return true;

          return false;
        })
        .map((r) => {
          let reason = "";
          if (
            r.room_id === record.room_id &&
            r.mode === "face to face" &&
            record.mode === "face to face" &&
            (!this.isJoined || r.faculty_id === record.faculty_id)
          )
            reason = "Same room, same day, and overlapping time (Face-to-Face)";
          else if (r.faculty_id === record.faculty_id)
            reason = "Same faculty assigned to overlapping schedules";
          else if (r.class_id === record.class_id)
            reason = "Same class/section has overlapping schedules";
          return { ...r, reason };
        });
    },

    hasRoomConflict(record) {
      return this.getConflictingRecords(record).length > 0;
    }, // Open the conflict modal for a record
    openConflictModal(record) {
      const conflicts = this.getConflictingRecords(record);

      if (!conflicts.length) return;

      this.selectedSchedule = record; // 👈 LEFT SIDE
      this.conflictRecords = conflicts; // 👉 RIGHT SIDE
      this.conflictModalVisible = true;
    },

    closeConflictModal() {
      this.conflictModalVisible = false;
      this.conflictRecords = [];
      this.selectedSchedule = null;
    },

    toggleShowCompareSelection() {
      this.showCompareSelection = !this.showCompareSelection;
    },
    backFromCompare() {
      this.filteredGroupedSchedule = { ...this.groupedSchedule };
      this.compareInstructorA = "";
      this.compareInstructorB = "";
      this.showCompareView = false;
      this.showFacultyTable = false;
      this.showCompareSelection = false;
    },
    showCompareFacultyCards() {
      if (!this.compareInstructorA || !this.compareInstructorB) return;

      this.filteredGroupedSchedule = {
        [this.compareInstructorA]:
          this.groupedSchedule[this.compareInstructorA] || [],
        [this.compareInstructorB]:
          this.groupedSchedule[this.compareInstructorB] || [],
      };

      this.showFacultyTable = false;
      this.showCompareView = true;

      // ✅ RESET CARD PAGINATION
      this.currentCardPage = 1;
    },
    openEditInstructorModal(instructor) {
      // Send fresh copies of schedules to modal
      this.editInstructorData = (this.groupedSchedule[instructor] || []).map(
        (r) => ({ ...r }),
      );
      this.showEditModal = true;
    },
    handleModalSaved(updatedInstructorSchedules) {
      if (!updatedInstructorSchedules.length) return;

      // 1️⃣ Merge updates into finalSchedules
      updatedInstructorSchedules.forEach((updated) => {
        const index = this.finalSchedules.findIndex((s) => s.id === updated.id);
        if (index > -1) {
          this.finalSchedules[index] = { ...updated };
        } else {
          this.finalSchedules.push({ ...updated });
        }
      });

      // 2️⃣ Rebuild grouped schedules
      this.groupedSchedule = this.groupByInstructor(this.finalSchedules);

      // 3️⃣ ✅ PRESERVE COMPARE VIEW
      if (
        this.showCompareView &&
        this.compareInstructorA &&
        this.compareInstructorB
      ) {
        this.filteredGroupedSchedule = {
          [this.compareInstructorA]:
            this.groupedSchedule[this.compareInstructorA] || [],
          [this.compareInstructorB]:
            this.groupedSchedule[this.compareInstructorB] || [],
        };
      } else {
        this.filteredGroupedSchedule = { ...this.groupedSchedule };
      }

      // 4️⃣ Reset pagination
      this.currentPage = 1;

      // 5️⃣ Keep modal data in sync (no view reset)
      if (this.showEditModal) {
        const instructorsInModal = Array.from(
          new Set(this.editInstructorData.map((item) => item.faculty_name)),
        );

        this.$nextTick(() => {
          this.editInstructorData = instructorsInModal.flatMap((instructor) => {
            return (this.groupedSchedule[instructor] || []).map((r) => ({
              ...r,
            }));
          });
        });
      }
    },
    handleDeletedSchedule(deletedId) {
      this.finalSchedules = this.finalSchedules.filter(
        (s) => s.id !== deletedId,
      );
      this.groupedSchedule = this.groupByInstructor(this.finalSchedules);
      this.filterSchedules();
    },
    closeEditInstructorModal() {
      this.showEditModal = false;
      this.editInstructorData = {};
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
      // Block large classes if Join is active
      if (this.isJoined && Number(record.class_size) >= 30) {
        toast.info(
          "Cannot move classes with 30 or more students when Join is active.",
        );
        event.preventDefault();
        return;
      }

      this.draggedRecord = { ...record };

      // ✅ Hide tooltip when dragging starts
      this.scheduleTooltipVisible = false;
      this.tooltipItem = null;

      event.dataTransfer.effectAllowed = "move";
    },

    async onDrop(event, targetInstructor, targetDay, targetStartHour) {
      if (!this.draggedRecord) return;

      const baseRecord = this.draggedRecord;

      // 🔥 Join mode
      if (this.isJoined) {
        const joinable = this.getJoinableSchedules(baseRecord);

        if (joinable.length) {
          this.pendingJoinRecord = baseRecord;
          this.pendingJoinTargets = joinable;
          this.joinValidationModalVisible = true;
          this.draggedRecord = null;
          return; // wait for user confirmation
        }
      }

      // Determine records to move (single or joined)
      const recordsToMove =
        baseRecord.is_joined && baseRecord.join_group_id
          ? this.finalSchedules.filter(
              (r) => r.join_group_id === baseRecord.join_group_id,
            )
          : [baseRecord];

      // Apply new position
      recordsToMove.forEach((r) => {
        r.faculty_name = targetInstructor;
        r.day = targetDay;
        r.start_hour = targetStartHour;
      });

      // Conflict check
      if (!this.isJoined) {
        for (const r of recordsToMove) {
          const conflicts = this.getConflictingRecords(r);
          if (conflicts.length) {
            this.selectedSchedule = r;
            this.conflictRecords = conflicts;
            this.conflictModalVisible = true;
            this.draggedRecord = null;
            return;
          }
        }
      }

      // Save
      try {
        await Promise.all(
          recordsToMove.map((r) =>
            axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${r.id}`,
              {
                faculty_id: r.faculty_id,
                faculty_name: r.faculty_name,
                day: r.day,
                start_hour: r.start_hour,
                duration: r.duration,
                room_id: r.room_id,
                room_name: r.room_name,
                mode: r.mode,
                type: r.type,
              },
            ),
          ),
        );
        toast.success("Schedule moved successfully!");
        await this.fetchFinalSchedules();
      } catch (err) {
        console.error(err);
        toast.error("Failed to move schedule.");
      }

      this.draggedRecord = null;
    },

    async loadFetchData() {
      const store = useFetchDataStore();
      await store.fetchPrograms();
      await store.fetchInstitutes();
      await store.fetchCourses();
    },

    backToFacultyTable() {
      this.filteredGroupedSchedule = this.groupedSchedule;
      this.showFacultyTable = true;
      this.currentPage = 1;
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
      if (!item || item.start_hour == null) return 0;

      const start = this.normalizeHour(Number(item.start_hour));
      return (start - slotStart) * this.timeSlotHeight;
    },

    getBlockHeight(item) {
      if (!item || !item.duration) return this.timeSlotHeight;

      return Number(item.duration) * this.timeSlotHeight - 1;
    },

    filterSchedules() {
      let filtered = { ...this.groupedSchedule };

      if (this.selectedInstituteId) {
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some(
              (s) =>
                String(s.institute_id) === String(this.selectedInstituteId),
            ),
          ),
        );
      }

      if (this.selectedProgramId) {
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some(
              (s) => String(s.program_id) === String(this.selectedProgramId),
            ),
          ),
        );
      }

      this.filteredGroupedSchedule = filtered;
      this.currentPage = 1;
    },
    getScheduleForCell(slot, day, instructor) {
      const schedules = this.filteredGroupedSchedule[instructor] || [];
      const renderedGroups = new Set();

      return schedules.filter((item) => {
        if (item.day !== day) return false;

        const start = this.normalizeHour(item.start_hour);
        const end = start + Number(item.duration);
        const overlaps = end > slot.start && start < slot.end;
        if (!overlaps) return false;

        // 🔥 If joined → render only first occurrence
        if (item.is_joined && item.join_group_id) {
          if (renderedGroups.has(item.join_group_id)) {
            return false;
          }
          renderedGroups.add(item.join_group_id);
        }

        return true;
      });
    },
    getTypeColor(room_type) {
      if (!room_type) return "bg-green-100 border-green-400";
      const normalized = room_type.toLowerCase();
      if (normalized === "laboratory" || normalized === "lab") {
        return "bg-blue-100 border-blue-400";
      }
      return "bg-green-100 border-green-400";
    },

    viewFacultySchedule(instructor) {
      this.filteredGroupedSchedule = {
        [instructor]: this.groupedSchedule[instructor],
      };
      this.showFacultyTable = false;
    },

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) this.currentPage = page;
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

    async fetchFinalSchedules() {
      this.loading = true;
      this.error = null;

      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/final-generated-class-schedule/get-all-final-schedules",
          { withCredentials: true },
        );

        let schedules = data || [];
        if (this.user.role === "Program Chairperson") {
          schedules = schedules.filter(
            (s) =>
              s.institute_id === this.user.institute_id &&
              s.program_id === this.user.program_id,
          );
        }

        this.finalSchedules = schedules;
        this.groupedSchedule = this.groupByInstructor(this.finalSchedules);
        this.filteredGroupedSchedule = { ...this.groupedSchedule };

        this.changePage(1);
      } catch (err) {
        this.error = err.message || "Failed to fetch final schedules";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    // Keep your existing groupByInstructor method
    groupByInstructor(schedules) {
      return schedules.reduce((acc, s) => {
        const instructor = s.faculty_name || "Unknown Faculty";
        if (!acc[instructor]) acc[instructor] = [];
        acc[instructor].push(s);
        return acc;
      }, {});
    },

    async fetchSchoolYears() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years",
        );
        this.schoolYears = res.data.map((y) => ({ ...y }));
      } catch (err) {
        console.error("Failed to fetch school years:", err);
      }
    },
  },
  async mounted() {
    await this.fetchUser();
    await this.loadFetchData();
    await this.fetchSchoolYears();
    await this.fetchFinalSchedules();
  },
};
</script>
