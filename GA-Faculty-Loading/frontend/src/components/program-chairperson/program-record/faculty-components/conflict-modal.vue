<template>
  <div
    v-if="visible"
    class="fixed inset-0 z-50 bg-black/40 flex items-center justify-center"
  >
    <div class="bg-white w-[900px] rounded-2xl p-6 shadow-xl">
      <!-- Header -->
      <div class="flex items-center justify-between border-b pb-3 mb-4">
        <div class="flex items-center gap-2">
          <icon
            name="exclamation-circle"
            class="w-7 h-7 p-1 rounded-full bg-red-200 text-red-900 flex items-center justify-center"
          />
          <h3 class="text-lg font-semibold text-gray-800 leading-none">
            Scheduled Conflict Detected
          </h3>
        </div>
        <button
          @click="$emit('cancel')"
          class="text-gray-400 hover:text-gray-600 transition"
        >
          ✕
        </button>
      </div>

      <!-- Body -->
      <div class="grid grid-cols-2 gap-6 mt-6">
        <!-- Selected Schedule -->
        <div class="relative bg-white rounded-2xl p-5 border">
          <span
            class="absolute -top-3 left-4 bg-green-600 text-white text-xs px-3 py-1 rounded-full shadow"
          >
            Selected Schedule
          </span>
          <div class="mt-3 space-y-3 text-sm text-gray-800">
            <div class="flex justify-between items-center">
              <h4 class="font-semibold text-base">
                {{ schedule.course_code }}
              </h4>
              <span
                class="text-xs px-2 py-1 rounded-full font-medium"
                :class="{
                  'bg-orange-500 text-white': schedule.mode === 'face to face',
                  'bg-purple-700 text-white': schedule.mode === 'online',
                }"
              >
                {{
                  schedule.mode === "face to face" ? "Face to Face" : "Online"
                }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <p class="text-xs text-gray-500">Faculty</p>
                <p class="font-medium">{{ schedule.faculty_name }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">Section</p>
                <p class="font-medium">
                  {{ schedule.program_code }}-{{ schedule.set_name }}
                </p>
              </div>
              <div>
                <p class="text-xs text-gray-500">Room</p>
                <p class="font-medium">{{ schedule.room_name }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">Room Type</p>
                <p class="font-medium">{{ schedule.room_type }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">Day</p>
                <p class="font-medium">{{ schedule.day }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">Time</p>
                <p class="font-medium">
                  {{ formatTime(schedule.start_hour) }} –
                  {{ formatTime(schedule.start_hour + schedule.duration) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Conflicting Schedules -->
        <div class="relative bg-white rounded-2xl p-5 border">
          <span
            class="absolute -top-3 left-4 bg-red-600 text-white text-xs px-3 py-1 rounded-full shadow"
          >
            Conflicting Schedules
          </span>
          <div class="mt-3 space-y-4 max-h-[420px] overflow-y-auto pr-2 p-2">
            <div
              v-for="conflict in conflicts"
              :key="conflict.id"
              class="relative rounded-xl p-4 ring-1"
              :class="{
                'ring-red-200 bg-red-50':
                  conflict.reason !== 'Part of the joined schedule',
                'ring-yellow-200 bg-yellow-50':
                  conflict.reason === 'Part of the joined schedule',
              }"
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
                      {{ conflict.program_code }}-{{ conflict.set_name }}
                    </p>
                  </div>
                  <div>
                    <p class="text-xs text-gray-500">Room</p>
                    <p class="font-medium">{{ conflict.room_name }}</p>
                  </div>
                  <div>
                    <p class="text-xs text-gray-500">Room Type</p>
                    <p class="font-medium">{{ conflict.room_type }}</p>
                  </div>

                  <div>
                    <p class="text-xs text-gray-500">Day</p>
                    <p class="font-medium">{{ conflict.day }}</p>
                  </div>
                  <div>
                    <p class="text-xs text-gray-500">Time</p>
                    <p class="font-medium">
                      {{ formatTime(conflict.start_hour) }} –
                      {{ formatTime(conflict.start_hour + conflict.duration) }}
                    </p>
                  </div>
                </div>
                <div
                  class="flex items-start gap-2 mt-2 p-2 rounded-lg text-xs"
                  :class="{
                    'bg-red-50 text-red-700':
                      conflict.reason !== 'Part of the joined schedule',
                    'bg-yellow-50 text-yellow-800':
                      conflict.reason === 'Part of the joined schedule',
                  }"
                >
                  <span>⚠</span>
                  <span>{{
                    conflict.reason || "Schedule overlap detected"
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex justify-end mt-5">
        <button
          @click="$emit('close')"
          class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
export default {
  name: "ConflictModal",
  components: {
    icon,
  },
  props: {
    visible: Boolean,
    schedule: Object,
    conflicts: Array,
  },
  methods: {
    formatTime(hour) {
      const h = Math.floor(hour);
      const m = (hour % 1) * 60;
      return `${h.toString().padStart(2, "0")}:${m
        .toString()
        .padStart(2, "0")}`;
    },
  },
};
</script>
