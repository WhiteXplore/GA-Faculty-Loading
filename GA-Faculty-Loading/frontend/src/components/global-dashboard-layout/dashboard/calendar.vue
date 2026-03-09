<template>
  <div class="max-w-full mx-auto p-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <button
        @click="prevMonth"
        class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
      >
        ‹
      </button>
      <h2 class="text-xl font-semibold text-gray-700">
        {{ currentMonthYear }}
      </h2>
      <button
        @click="nextMonth"
        class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
      >
        ›
      </button>
    </div>

    <!-- Weekday Headers -->
    <div
      class="grid grid-cols-7 text-sm text-center text-gray-500 font-medium mb-2"
    >
      <div v-for="day in weekdays" :key="day">{{ day }}</div>
    </div>

    <!-- Calendar Grid -->
    <div class="grid grid-cols-7 gap-1 text-sm">
      <div v-for="n in startDay" :key="'empty-' + n"></div>

      <div
        v-for="day in daysInMonth"
        :key="day"
        @click="selectDate(day)"
        :class="[
          'p-2 rounded-lg text-center cursor-pointer hover:bg-blue-100 transition',
          isToday(day)
            ? 'bg-blue-500 text-white font-bold'
            : 'bg-white text-gray-800',
          selectedDate === day ? 'ring-2 ring-blue-500' : '',
        ]"
      >
        {{ day }}
      </div>
    </div>
  </div>
</template>

<script>
import dayjs from "dayjs";

export default {
  name: "CalendarPage",
  data() {
    return {
      today: dayjs(),
      current: dayjs().startOf("month"),
      selectedDate: null,
      weekdays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    };
  },
  computed: {
    currentMonthYear() {
      return this.current.format("MMMM YYYY");
    },
    startDay() {
      return this.current.day();
    },
    daysInMonth() {
      return Array.from(
        { length: this.current.daysInMonth() },
        (_, i) => i + 1
      );
    },
  },
  methods: {
    prevMonth() {
      this.current = this.current.subtract(1, "month");
      this.selectedDate = null;
    },
    nextMonth() {
      this.current = this.current.add(1, "month");
      this.selectedDate = null;
    },
    isToday(day) {
      return (
        this.current.date(day).format("YYYY-MM-DD") ===
        this.today.format("YYYY-MM-DD")
      );
    },
    selectDate(day) {
      this.selectedDate = day;
    },
  },
};
</script>

<style scoped></style>
