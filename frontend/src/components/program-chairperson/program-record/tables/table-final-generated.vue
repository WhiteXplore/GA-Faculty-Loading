<template>
  <div class="flex flex-col gap-3 h-[87vh]">
    <!-- TODO  Top Controls -->
    <div class="flex flex-wrap justify-between items-center gap-3">
      <div class="text-sm text-gray-600 mt-2 font-medium">
        Pages / Faculty Loads
      </div>

      <div class="flex gap-3 flex-wrap">
        <!-- TODO  Toggle View Button -->
        <button
          @click="showFacultyTable = !showFacultyTable"
          class="group flex items-center gap-2 px-4 py-2 border border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white rounded-xl shadow-sm transition"
        >
          <div
            class="p-1 bg-blue-100 rounded-full flex items-center justify-center group-hover:bg-white transition"
          >
            <icon
              name="users"
              class="w-4 h-4 text-blue-600 group-hover:text-blue-600"
            />
          </div>
          <span class="font-medium text-sm">
            {{ showFacultyTable ? "View Cards" : "View Faculty" }}
          </span>
        </button>

        <!-- Compare & Swap Controls -->
        <div
          class="flex items-center gap-3 flex-wrap ml-auto"
          v-if="showCompareSelection"
        >
          <!-- Instructor Selects -->
          <div class="flex gap-2 items-center">
            <select
              v-model="compareInstructorA"
              class="rounded-xl border border-purple-600 px-2 py-2.5 text-sm text-purple-700 shadow-sm"
            >
              <option value="">Select Instructor</option>
              <option
                v-for="instructor in Object.keys(groupedSchedule)"
                :key="'a-' + instructor"
                :value="instructor"
              >
                {{ instructor }}
              </option>
            </select>

            <select
              v-model="compareInstructorB"
              class="rounded-xl border border-purple-600 px-2 py-2.5 text-sm text-purple-700 shadow-sm"
            >
              <option value="">Select Instructor</option>
              <option
                v-for="instructor in Object.keys(groupedSchedule)"
                :key="'b-' + instructor"
                :value="instructor"
              >
                {{ instructor }}
              </option>
            </select>

            <!-- Compare Button -->
            <button
              @click="showCompareFacultyCards"
              :disabled="
                !compareInstructorA ||
                !compareInstructorB ||
                compareInstructorA === compareInstructorB
              "
              class="bg-purple-600 text-white px-4 py-2.5 rounded-xl hover:bg-purple-700 transition"
            >
              Compare
            </button>
          </div>

          <!-- Close Compare -->
          <button
            @click="backFromCompare"
            class="flex items-center gap-2 p-1 border border-gray-400 rounded-full shadow-sm hover:bg-gray-100 transition"
          >
            <icon name="circle-close" class="w-5 h-5" />
          </button>
        </div>

        <button
          @click="toggleShowCompareSelection"
          v-if="!showCompareSelection"
          class="bg-purple-600 text-white px-4 py-1 rounded-xl hover:bg-purple-700 transition"
        >
          Compare
        </button>
      </div>
    </div>

    <div class="flex flex-wrap items-center gap-4">
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
                      v-for="item in getScheduleForCell(slot, day, instructor)"
                      :key="
                        item.id ||
                        item.course_code + item.start_hour + item.room_name
                      "
                    >
                      <div
                        v-if="isStartingSlot(item, slot)"
                        draggable="true"
                        @dragstart="onDragStart($event, item)"
                        @click="
                          toggleSwapSelection(item);
                          highlightRow(item);
                        "
                        @mouseenter="showScheduleTooltip($event, item)"
                        @mouseleave="hideScheduleTooltip"
                        :class="[
                          'absolute inset-x-1 border rounded-lg text-[11px] p-1 shadow-sm cursor-pointer overflow-hidden transition-all duration-200 whitespace-nowrap',
                          item.id?.toString().startsWith('temp-')
                            ? 'bg-purple-200 border-purple-400 text-purple-900'
                            : getTypeColor(item.type),
                          hasRoomConflict(item)
                            ? 'bg-red-300 border-red-500 text-red-900'
                            : '',
                          swapSelection.includes(item)
                            ? 'border-yellow-500 bg-yellow-100'
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

                        <!-- Course Info -->
                        <div class="truncate font-semibold">
                          {{ item.course_code }}
                        </div>
                        <div class="truncate">{{ item.room_name }}</div>
                        <div class="truncate">
                          {{ item.program_name }}-{{ item.set_name }}
                        </div>

                        <!-- Conflict Button -->
                        <div class="w-full flex justify-center mt-1">
                          <button
                            v-if="hasRoomConflict(item)"
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
          </div>

          <!-- 🔍 Schedule Tooltip -->
          <div
            v-if="scheduleTooltipVisible && tooltipItem"
            class="fixed z-[9999] pointer-events-none"
            :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
          >
            <div
              class="bg-white border border-gray-300 rounded-xl p-3 scale-125 origin-top-left"
            >
              <div class="flex items-center justify-between gap-2 mb-2 w-full">
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
                <p><strong>Faculty:</strong> {{ tooltipItem.faculty_name }}</p>
                <p>
                  <strong>Year & Section:</strong>
                  {{ tooltipItem.program_name }}-{{ tooltipItem.set_name }}
                </p>
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
          <!-- Badge -->
          <span
            class="absolute -top-3 left-4 bg-green-600 text-white text-xs px-3 py-1 rounded-full shadow"
          >
            Selected Schedule
          </span>

          <div class="mt-3 space-y-3 text-sm text-gray-800">
            <div class="flex justify-between items-center">
              <h4 class="font-semibold text-base">
                {{ selectedSchedule.course_code }}
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
                <p class="text-xs text-gray-500">Time</p>
                <p class="font-medium">
                  {{ formatTime(selectedSchedule.start_hour) }} –
                  {{
                    formatTime(
                      selectedSchedule.start_hour + selectedSchedule.duration,
                    )
                  }}
                </p>
              </div>
              <div>
                <p class="text-xs text-gray-500">Day</p>
                <p class="font-medium">{{ selectedSchedule.day }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT: Conflict Schedules -->
        <div class="relative bg-white rounded-2xl p-5 border">
          <!-- Badge -->
          <span
            class="absolute -top-3 left-4 bg-red-600 text-white text-xs px-3 py-1 rounded-full shadow"
          >
            Conflicting Schedules
          </span>

          <!-- Scrollable list -->
          <div class="mt-3 space-y-4 max-h-[420px] overflow-y-auto pr-2 p-2">
            <div
              v-for="conflict in conflictRecords"
              :key="conflict.id"
              class="relative bg-white rounded-xl p-4 ring-1 ring-red-200"
            >
              <div class="space-y-2 text-sm">
                <div class="flex justify-between items-center">
                  <h5 class="font-semibold text-gray-800">
                    {{ conflict.course_code }}
                  </h5>
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

                <div class="grid grid-cols-2 gap-2 text-gray-700">
                  <div>
                    <p class="text-xs text-gray-500">Faculty</p>
                    <p class="font-medium">{{ conflict.faculty_name }}</p>
                  </div>

                  <div>
                    <p class="text-xs text-gray-500">Section</p>
                    <p class="font-medium">
                      {{ conflict.program_name }}{{ conflict.set_name }}
                    </p>
                  </div>

                  <div>
                    <p class="text-xs text-gray-500">Room</p>
                    <p class="font-medium">{{ conflict.room_name }}</p>
                  </div>

                  <div>
                    <p class="text-xs text-gray-500">Time</p>
                    <p class="font-medium">
                      {{ formatTime(conflict.start_hour) }} –
                      {{ formatTime(conflict.start_hour + conflict.duration) }}
                    </p>
                  </div>
                  <div>
                    <p class="text-xs text-gray-500">Day</p>
                    <p class="font-medium">{{ conflict.day }}</p>
                  </div>
                </div>

                <!-- Reason -->
                <div
                  class="flex items-start gap-2 mt-2 p-2 rounded-lg bg-red-50 text-xs text-red-700"
                >
                  <span>⚠</span>
                  <span>
                    {{ conflict.reason || "Schedule overlap detected" }}
                  </span>
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

export default {
  name: "FacultySchedule",
  components: { icon, editSchedule },
  data() {
    return {
      user: {},

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
    };
  },

  computed: {
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
    getConflictsForDrag(record, targetInstructor, targetDay, targetStartHour) {
      const clonedRecord = { ...record };
      clonedRecord.faculty_name = targetInstructor;
      clonedRecord.day = targetDay;
      clonedRecord.start_hour = targetStartHour;

      return this.getConflictingRecords(clonedRecord);
    },
    showScheduleTooltip(event, item) {
      const rect = event.currentTarget.getBoundingClientRect();

      this.tooltipItem = item;
      this.scheduleTooltipVisible = true;

      // 👉 fixed position: right side of block
      this.tooltipX = rect.right + 12;
      this.tooltipY = rect.top;
    },

    hideScheduleTooltip() {
      this.scheduleTooltipVisible = false;
      this.tooltipItem = null;
    },
    highlightRow(item) {
      this.highlightedRecordId = item.id || item.tempId;
      // optional: scroll to the row
      this.$nextTick(() => {
        const el = document.getElementById(`row-${this.highlightedRecordId}`);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    },
    getConflictingRecords(record) {
      const recordStart = this.normalizeHour(record.start_hour);
      const recordEnd = recordStart + Number(record.duration);

      return this.finalSchedules
        .filter((r) => {
          if (r.id === record.id) return false;
          if (r.day !== record.day) return false;

          const rStart = this.normalizeHour(r.start_hour);
          const rEnd = rStart + Number(r.duration);

          // ⛔ NO TIME OVERLAP → NO CONFLICT
          const isOverlapping =
            Math.max(rStart, recordStart) < Math.min(rEnd, recordEnd);

          if (!isOverlapping) return false;

          // 🔴 RULE 1: SAME ROOM (Face-to-Face only)
          if (
            r.room_id &&
            record.room_id &&
            r.room_id === record.room_id &&
            r.mode === "face to face" &&
            record.mode === "face to face"
          ) {
            return true;
          }

          // 🔴 RULE 2: SAME FACULTY
          if (r.faculty_id === record.faculty_id) {
            return true;
          }

          // 🔴 RULE 3: SAME CLASS / SECTION
          if (r.class_id && record.class_id && r.class_id === record.class_id) {
            return true;
          }

          return false;
        })
        .map((r) => {
          let reason = "";

          if (
            r.room_id === record.room_id &&
            r.mode === "face to face" &&
            record.mode === "face to face"
          ) {
            reason = "Same room, same day, and overlapping time (Face-to-Face)";
          } else if (r.faculty_id === record.faculty_id) {
            reason = "Same faculty assigned to overlapping schedules";
          } else if (r.class_id === record.class_id) {
            reason = "Same class/section has overlapping schedules";
          }

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

    toggleSwapSelection(item) {
      const index = this.swapSelection.findIndex((s) => s.id === item.id);
      if (index > -1) {
        this.swapSelection.splice(index, 1);
      } else if (this.swapSelection.length < 2) {
        this.swapSelection.push(item);
      } else {
        toast.info("You can only swap 2 courses at a time.");
      }
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
      this.draggedRecord = { ...record }; // make a copy to prevent direct mutation
      event.dataTransfer.effectAllowed = "move";
    },
    async onDrop(event, targetInstructor, targetDay, targetStartHour) {
      if (!this.draggedRecord) return;

      // Create a copy of the dragged record and update its new instructor/day/start
      const record = { ...this.draggedRecord };
      record.faculty_name = targetInstructor;
      record.day = targetDay;
      record.start_hour = targetStartHour;

      // Check for conflicts
      const conflicts = this.getConflictingRecords(record);
      if (conflicts.length) {
        this.selectedSchedule = record;
        this.conflictRecords = conflicts;
        this.conflictModalVisible = true;
        this.draggedRecord = null;
        return;
      }

      // Update local UI
      this.finalSchedules = this.finalSchedules.map((s) =>
        s.id === record.id ? { ...record } : s,
      );

      // Re-group schedules by instructor
      this.groupedSchedule = this.groupByInstructor(this.finalSchedules);

      // ✅ Preserve Compare View if active
      if (this.showCompareView) {
        this.filteredGroupedSchedule = {
          [this.compareInstructorA]:
            this.groupedSchedule[this.compareInstructorA] || [],
          [this.compareInstructorB]:
            this.groupedSchedule[this.compareInstructorB] || [],
        };
      } else {
        this.filteredGroupedSchedule = { ...this.groupedSchedule };
      }

      // Reset dragged record
      this.draggedRecord = null;

      // Prepare payload for backend (only allowed fields)
      const allowedFields = [
        "faculty_id",
        "faculty_name",
        "day",
        "start_hour",
        "duration",
        "room_id",
        "room_name",
        "mode",
        "type",
      ];

      const payload = {};
      allowedFields.forEach((f) => (payload[f] = record[f]));

      // Save to backend
      try {
        await axios.patch(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${record.id}`,
          payload,
        );
        toast.success("Schedule moved successfully!");
        await this.fetchFinalSchedules(); // ✅ Preserve compare view if active
        if (this.showCompareView) {
          this.filteredGroupedSchedule = {
            [this.compareInstructorA]:
              this.groupedSchedule[this.compareInstructorA] || [],
            [this.compareInstructorB]:
              this.groupedSchedule[this.compareInstructorB] || [],
          };
        }
      } catch (error) {
        console.error(error);
        toast.error("Failed to save schedule.");
      }
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
      return schedules.filter((item) => {
        if (item.day !== day) return false;

        const start = this.normalizeHour(item.start_hour);
        const end = start + Number(item.duration);
        return end > slot.start && start < slot.end;
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
