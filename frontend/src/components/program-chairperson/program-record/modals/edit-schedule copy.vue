<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 px-2 gap-2"
  >
    <div class="flex justify-center gap-2 w-full">
      <!-- MAIN MODAL WRAPPER -->
      <div
        class="bg-white w-[60vw] h-[98vh] rounded-xl shadow-xl flex flex-col overflow-hidden p-1"
      >
        <!-- HEADER -->
        <div
          class="flex items-center justify-between bg-defaultGreen text-white px-6 py-3 rounded-t-lg"
        >
          <div class="flex items-center gap-2">
            <icon name="edit" />
            <h3 class="text-lg font-bold">Edit Schedules</h3>
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
            <div class="flex-1 overflow-auto bg-gray-50 h-full">
              <div
                v-for="(records, instructor) in groupedSchedule"
                :key="instructor"
                class="border rounded-lg shadow-sm bg-white"
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
                  <div
                    class="flex items-center gap-4 py-2 px-3 ml-2 rounded-full border w-max bg-gray-50 text-xs"
                  >
                    <span class="font-medium text-gray-700"
                      >Join Scheduled:</span
                    >

                    <div class="flex items-center gap-2">
                      <span
                        class="font-semibold"
                        :class="isJoined ? 'text-green-600' : 'text-gray-400'"
                      >
                        {{ isJoined ? "YES" : "NOT" }}
                      </span>

                      <button
                        @click="toggleJoin"
                        :class="[
                          'w-12 h-6 rounded-full p-1 flex items-center transition-colors duration-300 focus:outline-none',
                          isJoined ? 'bg-green-500' : 'bg-gray-300',
                        ]"
                      >
                        <span
                          class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300"
                          :class="isJoined ? 'translate-x-6' : 'translate-x-0'"
                        ></span>
                      </button>
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
                        <!-- Time Column -->
                        <td class="px-2 py-5 border text-center text-[10px]">
                          {{ formatTime(slot.start) }} -
                          {{ formatTime(slot.end) }}
                        </td>

                        <!-- Days Columns -->
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
                            :key="item.id || item.tempId"
                          >
                            <div
                              v-if="isStartingSlot(item, slot)"
                              :draggable="
                                !(isJoined && Number(item.class_size) >= 30)
                              "
                              @mouseenter="showScheduleTooltip($event, item)"
                              @mouseleave="hideScheduleTooltip"
                              @dragstart="onDragStart($event, item)"
                              @dblclick="attemptUnjoin(item)"
                              @click="highlightRow(item)"
                              :class="[
                                'absolute inset-x-1 border rounded-lg text-[11px] p-1 shadow-sm truncate transition cursor-pointer',
                                item.id?.toString().startsWith('temp-')
                                  ? 'bg-purple-200 border-purple-400 text-purple-900'
                                  : getTypeColor(item.type),
                                hasRoomConflict(item)
                                  ? 'bg-red-300 border-red-500 text-red-900'
                                  : '',
                                item.is_joined
                                  ? 'bg-blue-100 border-blue-400'
                                  : '',
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
                              <span
                                v-if="item.is_joined"
                                class="absolute bottom-2 right-2 px-2 h-5 flex items-center justify-center bg-blue-600 text-white text-[10px] font-bold rounded-full shadow"
                              >
                                J
                              </span>
                              <div class="truncate font-semibold">
                                {{ item.course_code }}
                              </div>
                              <div class="truncate">{{ item.room_name }}</div>
                              <div class="truncate">
                                {{ item.program_code }}-{{ item.set_name }}
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
      <div class="flex flex-col gap-2">
        <div
          v-if="showAddSchedulePanel"
          class="w-[45vw] max-h-[50vh] bg-white border shadow-xl transition-all duration-300 flex justify-start rounded-xl"
        >
          <div class="p-1 flex flex-col">
            <!-- Header -->
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

            <!-- Table Wrapper for Scroll -->
            <div class="overflow-y-auto max-h-[50vh] border-t">
              <table class="min-w-full divide-y divide-gray-200 text-xs">
                <!-- Table Head -->
                <thead class="bg-gray-100 sticky top-0 z-20">
                  <tr>
                    <th class="px-4 py-3 border w-[13%]">Section</th>
                    <th class="px-4 py-3 border w-[12%]">Course</th>
                    <th class="px-4 py-3 border w-[13%]">Room</th>
                    <th class="px-4 py-3 border w-[13%]">Day</th>
                    <th class="px-4 py-3 border w-[10%]">Start</th>
                    <th class="px-4 py-3 border w-[10%]">Hours</th>
                    <th class="px-4 py-3 border w-[18%]">Set Up</th>
                    <th class="px-4 py-3 border text-center">Action</th>
                  </tr>
                </thead>

                <!-- Table Body -->
                <tbody>
                  <tr
                    v-for="record in sortedLocalData"
                    :key="record.id || record.tempId"
                    :id="'row-' + (record.id || record.tempId)"
                    :class="[
                      'hover:bg-green-200 relative',
                      highlightedRecordId === (record.id || record.tempId)
                        ? 'bg-blue-100'
                        : '',
                      record.join_group_id
                        ? 'border-l-4 ' + getJoinColor(record.join_group_id)
                        : '',
                    ]"
                  >
                    <!-- Section Input -->
                    <td class="px-2 py-2 border relative">
                      <input
                        v-model="record.searchSectionQuery"
                        type="text"
                        placeholder="Select section..."
                        class="px-3 py-2 w-full rounded-md text-md"
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

                    <!-- Course Input -->
                    <td class="px-2 py-2 border relative">
                      <input
                        v-model="record.searchCourseQuery"
                        type="text"
                        placeholder="Select course..."
                        class="px-3 py-2 w-full rounded-md text-md"
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

                    <!-- Room Input -->
                    <td class="px-2 py-2 border relative">
                      <input
                        v-model="record.searchRoomQuery"
                        type="text"
                        placeholder="Select room..."
                        class="px-3 py-2 w-full rounded-md text-md"
                        @focus="record.showRoomDropdown = true"
                        @input="record.room_id = null"
                      />
                      <div
                        v-if="
                          record.showRoomDropdown &&
                          filteredRooms(record).length
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

                    <!-- Day -->
                    <td class="px-2 py-2 border">
                      <input
                        v-model="record.day"
                        class="w-full px-3 py-2 boder rounded-md text-center"
                      />
                    </td>

                    <!-- Start Hour -->
                    <td class="px-2 py-2 border text-center">
                      <input
                        v-model.number="record.start_hour"
                        type="number"
                        step="0.5"
                        min="8"
                        max="20"
                        class="w-full px-3 py-2 rounded-md text-center"
                      />
                    </td>

                    <!-- Duration -->
                    <td class="px-2 py-2 border text-center">
                      <input
                        v-model.number="record.duration"
                        type="number"
                        class="w-full px-3 py-2 rounded-md text-center"
                      />
                    </td>

                    <!-- Mode -->
                    <td class="px-2 py-2 border">
                      <select
                        v-model="record.mode"
                        @change="onModeChange(record)"
                        class="w-full rounded px-2 py-1 text-sm"
                      >
                        <option value="" disabled selected>Select mode</option>
                        <option value="face to face">Face to face</option>
                        <option value="online">Online</option>
                      </select>
                    </td>

                    <!-- Action -->
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
            </div>

            <!-- Footer Buttons -->
            <div class="flex justify-end gap-2 p-3 text-xs border-t">
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
        <div v-if="showAddSchedulePanel">
          <unscheduled />
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
                    {{ selectedSchedule.program_code }}-{{
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
          <div class="relative bg-white rounded-2xl p-4 border">
            <span
              class="absolute -top-3 left-4 bg-red-600 text-white text-xs px-3 py-1 rounded-full shadow"
            >
              Conflicting Schedules
            </span>

            <div class="mt-3 space-y-4 max-h-[420px] overflow-y-auto p-2">
              <div
                v-for="conflict in conflictRecords"
                :key="conflict.id"
                class="bg-white rounded-xl p-8 ring-1 ring-red-200"
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
                        {{ conflict.program_code }}-{{ conflict.set_name }}
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
  <!-- Schedule Tooltip -->
  <div
    v-if="scheduleTooltipVisible && tooltipItem"
    class="fixed z-[9999] pointer-events-none"
    :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
  >
    <div
      class="bg-white border border-gray-300 rounded-xl p-3 scale-125 origin-top-left shadow-lg w-[250px]"
    >
      <!-- Header -->
      <div class="flex items-center justify-between gap-2 mb-2 w-full">
        <div class="text-sm font-bold text-defaultGreen leading-none truncate">
          {{ tooltipItem.course_code }}
        </div>
        <div class="relative flex gap-1 items-center py-1 text-[8px]">
          <!-- Joined Badge -->
          <span
            v-if="tooltipItem.is_joined"
            class="inline-flex items-center justify-center px-2 py-1 bg-blue-600 text-white rounded-full shadow"
          >
            Joined
          </span>
          <!-- Mode Badge -->
          <span
            v-if="tooltipItem.mode"
            class="inline-flex items-center justify-center px-2 py-1 rounded-full text-white"
            :class="
              tooltipItem.mode === 'face to face'
                ? 'bg-orange-500'
                : 'bg-purple-500'
            "
          >
            {{
              tooltipItem.mode === "face to face" ? "Face to Face" : "Online"
            }}
          </span>
        </div>
      </div>

      <!-- Content -->
      <div class="text-[10px] text-gray-700 space-y-1">
        <p><strong>Faculty:</strong> {{ tooltipItem.faculty_name }}</p>

        <!-- Joined Sections -->
        <div>
          <p class="font-semibold">Year & Section:</p>
          <ul class="ml-3 list-disc space-y-0.5">
            <template v-if="tooltipItem.joinedItems?.length">
              <li v-for="s in tooltipItem.joinedItems" :key="s.id">
                {{ s.program_code }} - {{ s.set_name }} ({{ s.class_size }})
              </li>
            </template>
            <template v-else>
              <li>
                {{ tooltipItem.program_code }} - {{ tooltipItem.set_name }} ({{
                  tooltipItem.class_size
                }})
              </li>
            </template>
          </ul>
        </div>

        <p><strong>Room:</strong> {{ tooltipItem.room_name || "N/A" }}</p>
        <p><strong>Day:</strong> {{ tooltipItem.day }}</p>
        <p>
          <strong>Time:</strong>
          {{ formatTime(tooltipItem.start_hour) }} –
          {{
            formatTime(tooltipItem.start_hour + Number(tooltipItem.duration))
          }}
        </p>
        <p><strong>Type:</strong> {{ tooltipItem.type }}</p>
      </div>
    </div>
  </div>

  <!-- Unjoin Confirmation Modal -->
  <UnjoinModal
    :visible="unjoinModalVisible"
    @confirm="confirmUnjoin"
    @close="cancelUnjoin"
  />

  <editJoinValdiation
    :visible="joinValidationModalVisible"
    :baseRecord="pendingJoinRecord"
    :targets="pendingJoinTargets"
    @close="cancelJoin"
    @confirm="confirmJoin"
  />
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";
import icon from "@/assets/icon.vue";
import editJoinValdiation from "../faculty-components/edit-join-valdiation.vue";
import unscheduled from "../faculty-components/unscheduled.vue";
import UnjoinModal from "../faculty-components/unjoin-validation-modal.vue";
export default {
  components: { icon, editJoinValdiation, unscheduled, UnjoinModal },
  props: {
    show: Boolean,
    instructorData: { type: Array, default: () => [] },
  },
  data() {
    return {
      user: {},
      localData: [],
      saving: false,
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
      isJoined: false,
      joinValidationModalVisible: false,
      pendingJoinRecord: null,
      pendingJoinTargets: [],

      draggedGroup: [],
      scheduleTooltipVisible: false,
      tooltipItem: null,
      tooltipX: 0,
      tooltipY: 0,
      unjoinModalVisible: false,
      unjoinTarget: null,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rooms"]),
    isDraggable(record) {
      // If Join is active and class size >= 30 → not draggable
      return !(this.isJoined && Number(record.class_size) >= 30);
    },
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
    cancelJoin() {
      this.resetJoinState();
    },
    attemptUnjoin(item) {
      if (item.is_joined) {
        this.unjoinTarget = item;
        this.unjoinModalVisible = true;
      }
    },
    async confirmUnjoin() {
      if (!this.unjoinTarget) return;

      const record = this.unjoinTarget;
      const groupId = record.join_group_id;

      // Find all schedules in this join group
      const groupRecords = this.localData.filter(
        (r) => r.join_group_id === groupId,
      );

      // Reset join info for the entire group
      groupRecords.forEach((r) => {
        r.is_joined = false;
        r.join_group_id = null;
        r.joined_with = [];
      });

      // Clear global join modal state
      this.pendingJoinRecord = null;
      this.pendingJoinTargets = [];
      this.isJoined = false;

      // Optionally update backend
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
        toast.success("All schedules in the join group have been unjoined!");
      } catch (err) {
        console.error("Failed to unjoin schedules:", err);
        toast.error("Failed to unjoin schedules.");
        // Rollback if needed
        groupRecords.forEach((r) => {
          r.is_joined = true;
          r.join_group_id = groupId;
          r.joined_with = groupRecords
            .filter((x) => x.id !== r.id)
            .map((x) => x.id);
        });
      } finally {
        this.unjoinModalVisible = false;
        this.unjoinTarget = null;
      }
    },

    cancelUnjoin() {
      this.unjoinModalVisible = false;
      this.unjoinTarget = null;
    },
    onMouseMoveTooltip(event) {
      if (this.scheduleTooltipVisible) {
        // Slight offset so the tooltip doesn’t cover the cursor
        this.tooltipX = event.clientX + 10;
        this.tooltipY = event.clientY + 10;
      }
    },
    hideScheduleTooltip() {
      this.scheduleTooltipVisible = false;
      this.tooltipItem = null;
    },
    showScheduleTooltip(event, item) {
      if (this.draggedRecord) return;

      const rect = event.currentTarget.getBoundingClientRect();

      // ✅ SAFE fallback
      const schedules = this.finalSchedules || this.localData || [];

      let joinedItems = [];

      if (item.is_joined && item.join_group_id) {
        joinedItems = schedules.filter(
          (s) => s.join_group_id === item.join_group_id,
        );
      }

      this.tooltipItem = {
        ...item,
        joinedItems,
      };

      this.scheduleTooltipVisible = true;

      const tooltipWidth = 260;
      const tooltipHeight = 200;

      this.tooltipX = Math.min(
        rect.right + 12,
        window.innerWidth - tooltipWidth,
      );

      this.tooltipY = Math.min(rect.top, window.innerHeight - tooltipHeight);
    },
    toggleJoin() {
      this.isJoined = !this.isJoined;
    },
    getJoinColor(groupId) {
      if (!groupId) return null;

      const colors = [
        "border-blue-500",
        "border-green-500",
        "border-purple-500",
        "border-pink-500",
        "border-yellow-500",
        "border-indigo-500",
      ];

      const index = Math.abs(groupId) % colors.length;
      return colors[index];
    },
    canJoin(recordA, recordB) {
      if (!recordA || !recordB) return false;
      if (recordA.id === recordB.id) return false;
      if (recordB.is_joined) return false;

      const getSetPrefix = (set_name) => set_name?.split(" ")[0]?.trim() || "";

      const baseSet = getSetPrefix(recordA.set_name);
      const targetSet = getSetPrefix(recordB.set_name);

      const validModes = ["online", "face to face"];
      const modeA = recordA.mode?.toLowerCase();
      const modeB = recordB.mode?.toLowerCase();

      return (
        recordA.course_code === recordB.course_code &&
        recordA.type === recordB.type &&
        recordA.semester === recordB.semester &&
        baseSet === targetSet &&
        Number(recordA.class_size) < 30 &&
        Number(recordB.class_size) < 30 &&
        validModes.includes(modeA) &&
        validModes.includes(modeB) &&
        modeA === modeB // <-- make sure the modes match exactly
      );
    },
    getJoinableSchedules(record) {
      if (!this.localData || !Array.isArray(this.localData)) {
        return [];
      }

      return this.localData.filter((r) => this.canJoin(record, r));
    },
    resetJoinState() {
      this.pendingJoinRecord = null;
      this.pendingJoinTargets = [];
      this.joinValidationModalVisible = false;
    },
    cleanDropdownFields(payload) {
      delete payload.searchRoomQuery;
      delete payload.showRoomDropdown;
      delete payload.searchCourseQuery;
      delete payload.showCourseDropdown;
      delete payload.searchSectionQuery;
      delete payload.showSectionDropdown;
    },
    async confirmJoin() {
      if (!this.pendingJoinRecord || !this.pendingJoinTargets.length) return;

      const baseRecord = this.pendingJoinRecord;

      // Filter only valid join targets
      const validTargets = this.pendingJoinTargets.filter((target) =>
        this.canJoin(baseRecord, target),
      );

      if (!validTargets.length) {
        toast.error("No valid schedules to join based on the rules.");
        this.resetJoinState();
        return;
      }

      const allToJoin = [baseRecord, ...validTargets];
      const finalMode = baseRecord.mode?.toLowerCase();
      const joinGroupId = baseRecord.id;
      const joinedIds = allToJoin.map((s) => s.id);

      // ✅ Update UI instantly
      allToJoin.forEach((s) => {
        s.day = baseRecord.day;
        s.start_hour = baseRecord.start_hour;
        s.duration = baseRecord.duration;
        s.mode = finalMode;

        if (finalMode === "face to face") {
          s.room_id = baseRecord.room_id || null;
          s.room_name = baseRecord.room_name || null;
          s.room_capacity = baseRecord.room_capacity || null;
          s.room_type = baseRecord.room_type || null;
        } else {
          s.room_id = null;
          s.room_name = null;
          s.room_capacity = null;
          s.room_type = null;
        }

        s.join_group_id = joinGroupId;
        s.is_joined = true;
        s.joined_with = joinedIds.filter((id) => id !== s.id);
      });

      this.resetJoinState();

      // ✅ Send PATCH request in background (batch style)
      axios
        .patch(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/bulk-join`,
          allToJoin.map((s) => ({
            id: s.id,
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
          })),
        )
        .catch((err) => console.error("Failed to save joined schedules:", err));

      toast.success(
        `Classes joined! Total students: ${allToJoin.reduce(
          (a, s) => a + Number(s.class_size || 0),
          0,
        )}`,
      );
    },
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

        "is_joined",
        "join_group_id",
        "joined_with",
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
      return this.localData.filter((r) => {
        // 🚫 Skip self
        if (r.id === record.id) return false;

        // 🚫 Skip conflict if same join group
        if (
          record.join_group_id &&
          r.join_group_id &&
          record.join_group_id === r.join_group_id
        ) {
          return false;
        }

        const recordEnd = record.start_hour + (record.duration || 0);
        const rEnd = r.start_hour + (r.duration || 0);

        // ⏰ Time overlap check
        const timeOverlap =
          record.start_hour < rEnd && recordEnd > r.start_hour;

        if (!timeOverlap) return false;

        // 👩‍🏫 Same faculty conflict
        const sameFaculty =
          r.faculty_name === record.faculty_name && r.day === record.day;

        // 🏫 Same room conflict (only for face-to-face)
        const sameRoom =
          record.mode === "face to face" &&
          r.mode === "face to face" &&
          r.room_name &&
          record.room_name &&
          r.room_name === record.room_name &&
          r.day === record.day;

        return sameFaculty || sameRoom;
      });
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
      event.dataTransfer.effectAllowed = "move";
      this.draggedRecord = record;

      // Drag whole group if joined
      if (record.join_group_id) {
        this.draggedGroup = this.localData.filter(
          (r) => r.join_group_id === record.join_group_id,
        );
      } else {
        this.draggedGroup = [record];
      }
    },
    async onDrop(event, targetInstructor, targetDay, targetStartHour) {
      if (!this.draggedRecord) return;

      const group = this.draggedGroup?.length
        ? this.draggedGroup
        : [this.draggedRecord];

      /* ===============================
     STEP 1: JOIN MODE CHECK
  =============================== */

      if (this.isJoined && group.length === 1) {
        const tempRecord = {
          ...this.draggedRecord,
          faculty_name: targetInstructor,
          day: targetDay,
          start_hour: targetStartHour,
        };

        const joinables = this.getJoinableSchedules(tempRecord);

        if (joinables.length) {
          this.pendingJoinRecord = this.draggedRecord;
          this.pendingJoinTargets = joinables;
          this.joinValidationModalVisible = true;
          return;
        }
      }

      /* ===============================
     STEP 2: GROUP CONFLICT CHECK
  =============================== */

      const groupConflicts = [];

      for (const rec of group) {
        const tempRecord = {
          ...rec,
          faculty_name: targetInstructor,
          day: targetDay,
          start_hour: targetStartHour,
        };

        const conflicts = this.getConflictingRecords(tempRecord).filter(
          (c) => !group.some((g) => g.id === c.id),
        );

        groupConflicts.push(...conflicts);
      }

      if (groupConflicts.length) {
        this.selectedSchedule = {
          ...this.draggedRecord,
          time_start: targetStartHour ?? 0,
          time_end: (targetStartHour ?? 0) + (this.draggedRecord.duration ?? 0),
          faculty_name: targetInstructor,
          day: targetDay,
        };

        this.conflictRecords = groupConflicts;
        this.conflictModalVisible = true;

        this.draggedRecord = null;
        this.draggedGroup = [];
        return;
      }

      /* ===============================
     STEP 3: MOVE ENTIRE GROUP
  =============================== */

      for (const rec of group) {
        Object.assign(rec, {
          faculty_name: targetInstructor,
          day: targetDay,
          start_hour: targetStartHour,
        });

        const payload = this.sanitizePayload(rec);
        this.cleanDropdownFields(payload);

        const id = rec.id || rec.schedule_id || rec.final_generated_id;

        if (!id) continue;

        try {
          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
            payload,
          );
        } catch (error) {
          console.error("Failed to update schedule:", error);
        }
      }

      /* ===============================
     RESET
  =============================== */

      this.draggedRecord = null;
      this.draggedGroup = [];
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
        const updatedRows = [];

        this.localData.forEach((record) => {
          const payload = this.sanitizePayload({
            ...record,
            mode:
              record.mode?.toLowerCase() === "online"
                ? "online"
                : "face to face",
          });

          const id =
            record.id || record.schedule_id || record.final_generated_id;

          if (id) updatedRows.push({ id, payload });
          else newRows.push(payload);
        });

        // 1️⃣ Create new schedules (bulk)
        if (newRows.length) {
          const { data } = await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/bulk`,
            newRows,
          );
          // assign returned IDs to localData
          data.forEach((row, idx) => {
            const tempRecord = this.localData.find(
              (r) => !r.id && r.tempId === newRows[idx].tempId,
            );
            if (tempRecord) tempRecord.id = row.id;
          });
        }

        // 2️⃣ Update existing schedules in parallel
        if (updatedRows.length) {
          await Promise.all(
            updatedRows.map(({ id, payload }) =>
              axios.patch(
                `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
                payload,
              ),
            ),
          );
        }

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
