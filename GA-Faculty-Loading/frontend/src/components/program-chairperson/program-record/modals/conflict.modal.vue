<template>
  <div
    v-if="conflicts && conflicts.length"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div
      class="bg-white rounded-xl shadow-lg w-[90%] max-w-3xl max-h-[80vh] overflow-y-auto p-6 relative"
    >
      <!-- Header -->
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold">Schedule Conflicts Detected</h2>
        <button
          @click="$emit('close')"
          class="text-gray-500 hover:text-gray-700"
        >
          ✕
        </button>
      </div>

      <!-- Conflict Table -->
      <table class="min-w-full border border-gray-200 text-sm text-gray-700">
        <thead class="bg-gray-100 sticky top-0 z-10">
          <tr>
            <th class="px-4 py-2 border">Course Code</th>
            <th class="px-4 py-2 border">Faculty</th>
            <th class="px-4 py-2 border">Day</th>
            <th class="px-4 py-2 border">Time</th>
            <th class="px-4 py-2 border">Room</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in conflicts"
            :key="item.id + item.start_hour"
            class="even:bg-gray-50"
          >
            <td class="px-4 py-2 border">{{ item.course_code }}</td>
            <td class="px-4 py-2 border">{{ item.faculty_name }}</td>
            <td class="px-4 py-2 border">{{ item.day }}</td>
            <td class="px-4 py-2 border">
              {{ formatTime(item.start_hour) }} -
              {{ formatTime(item.start_hour + Number(item.duration)) }}
            </td>
            <td class="px-4 py-2 border">{{ item.room_name }}</td>
          </tr>
        </tbody>
      </table>

      <div class="mt-4 flex justify-end">
        <button
          @click="$emit('close')"
          class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConflictModal",
  props: {
    conflicts: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    formatTime(hour) {
      const h = hour % 12 === 0 ? 12 : hour % 12;
      const period = hour >= 12 ? "PM" : "AM";
      return `${h}:00 ${period}`;
    },
  },
};
</script>
