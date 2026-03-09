<template>
  <div class="min-h-screen bg-gray-100 p-4 rounded-md">
    <!-- Header -->
    <div class="mb-4 text-left">
      <h1 class="text-2xl font-semibold text-gray-800">
        Welcome, {{ user.first_name }} 👋
      </h1>
      <p class="text-sm text-gray-500">Here's what's happening today</p>
    </div>

    <!-- Main Content -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Calendar -->
      <div class="bg-white rounded-2xl shadow p-6 lg:col-span-2 h-[80vh]">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-700">Calendar</h2>
          <div class="flex gap-2">
            <button
              @click="prevMonth"
              class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 flex items-center gap-1"
            >
              <span><icon :name="'arrow-left'" /></span> Prev
            </button>
            <button
              @click="nextMonth"
              class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 flex items-center gap-1"
            >
              Next <span><icon :name="'arrow-right'" /></span>
            </button>
          </div>
        </div>

        <div class="text-lg font-semibold text-gray-700 mb-2">
          {{ monthYear }}
        </div>

        <!-- Weekdays -->
        <div
          class="grid grid-cols-7 text-center text-sm font-semibold text-gray-500 border-b pb-2"
        >
          <div v-for="day in weekDays" :key="day">{{ day }}</div>
        </div>

        <!-- Calendar Days -->
        <div class="grid grid-cols-7 gap-2 pt-2">
          <div
            v-for="(date, index) in calendarDays"
            :key="index"
            class="aspect-square rounded-xl h-[10vh] w-full cursor-pointer relative group p-2 text-right"
            :class="{
              'bg-defaultGreen text-white font-bold': isToday(date),
              'text-gray-400': date.month() !== currentMonth.month(),
              'hover:bg-blue-100': date.month() === currentMonth.month(),
            }"
            @click="selectDate(date)"
          >
            {{ date.date() }}

            <div v-if="hasEvent(date)" class="mt-1 flex flex-col gap-1">
              <div
                v-for="event in getEventsByDate(date)"
                :key="event.title + event.startDate"
                @click.stop="openEventDetails(event)"
                class="bg-defaultGreen text-white text-xs px-2 py-0.5 rounded hover:bg-green-300 cursor-pointer truncate"
              >
                {{ event.title }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Announcements -->
      <div class="bg-white rounded-2xl shadow p-6 h-[80vh] overflow-y-auto">
        <div
          class="flex justify-between items-center mb-4 border-b border-gray-100 pb-2"
        >
          <h2 class="text-xl font-semibold text-gray-700">Announcements</h2>
          <icon :name="'3dots'" />
        </div>

        <div v-if="todaysEvents.length">
          <h3 class="text-sm font-bold text-gray-600 mb-2">Today</h3>
          <div
            v-for="(event, idx) in todaysEvents"
            :key="'today-' + idx"
            class="bg-green-50 border border-green-200 rounded-xl p-4 mb-3 shadow-sm cursor-pointer hover:bg-green-100"
            @click="openEventDetails(event)"
          >
            <div class="flex items-center justify-between">
              <div>
                <div class="text-xs text-gray-500 mb-1">
                  {{ formatDate(event) }}
                </div>
                <div class="text-sm font-medium text-gray-800">
                  {{ event.title }}
                </div>
              </div>
              <div
                class="w-9 h-9 bg-green-400 rounded-full flex items-center justify-center"
              >
                <icon :name="'calendar'" class="text-white w-5 h-5" />
              </div>
            </div>
          </div>
        </div>

        <div v-if="upcomingEvents.length">
          <h3 class="text-sm font-bold text-gray-600 mt-4 mb-2">Upcoming</h3>
          <div
            v-for="(event, idx) in upcomingEvents"
            :key="'upcoming-' + idx"
            class="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-3 shadow-sm cursor-pointer hover:bg-blue-100"
            @click="openEventDetails(event)"
          >
            <div class="flex items-center justify-between">
              <div>
                <div class="text-xs text-gray-500 mb-1">
                  {{ formatDate(event) }}
                </div>
                <div class="text-sm font-medium text-gray-800">
                  {{ event.title }}
                </div>
              </div>
              <div
                class="w-9 h-9 bg-blue-400 rounded-full flex items-center justify-center"
              >
                <icon :name="'noticeBell'" class="text-white w-5 h-5" />
              </div>
            </div>
          </div>
        </div>

        <div v-if="pastEvents.length">
          <h3 class="text-sm font-bold text-gray-600 mt-4 mb-2">Completed</h3>
          <div
            v-for="(event, idx) in pastEvents"
            :key="'past-' + idx"
            class="bg-gray-50 border border-gray-200 rounded-xl p-4 mb-3 shadow-sm cursor-pointer hover:bg-gray-100"
            @click="openEventDetails(event)"
          >
            <div class="flex items-center justify-between">
              <div>
                <div class="text-xs text-gray-500 mb-1">
                  {{ formatDate(event) }}
                </div>
                <div class="text-sm font-medium text-gray-800">
                  {{ event.title }}
                </div>
              </div>
              <div
                class="w-9 h-9 bg-gray-400 rounded-full flex items-center justify-center"
              >
                <icon :name="'check1'" class="text-white w-5 h-5" />
              </div>
            </div>
          </div>
        </div>

        <p
          v-if="
            !todaysEvents.length && !upcomingEvents.length && !pastEvents.length
          "
          class="text-sm text-gray-500"
        >
          No announcements to show.
        </p>
      </div>
    </div>

    <!-- View/Edit Modal -->
    <div
      v-if="selectedEvent"
      class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-xl p-6 shadow-xl w-[350px]">
        <h3 class="text-lg font-semibold mb-2">Edit Event</h3>
        <p class="text-xs text-gray-500 mb-2">Date: {{ formattedEventDate }}</p>
        <textarea
          v-model="selectedEvent.title"
          class="w-full border px-3 py-2 rounded mb-4 text-sm"
        />

        <div class="flex justify-between">
          <button class="text-red-500 hover:underline" @click="deleteEvent">
            Delete
          </button>
          <div class="flex gap-2">
            <button
              @click="closeEventModal"
              class="text-gray-600 hover:underline"
            >
              Cancel
            </button>
            <button
              @click="saveEvent"
              class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
            >
              Save
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Event Modal -->
    <AddEventModal
      v-if="showEventModal"
      :selectedDate="selectedDate"
      @add="addEvent"
      @cancel="cancelEvent"
    />
  </div>
</template>

<script>
import AddEventModal from "@/components/global-dashboard-layout/dashboard/modals/add-event.vue";
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import dayjs from "dayjs";
import isBetween from "dayjs/plugin/isBetween";
import { mapStores } from "pinia";
import { useFetchDataStore } from "../../../store/fetch-data-store";
import axios from "axios";

dayjs.extend(isBetween);

export default {
  name: "EmployeeDashboard",
  components: {
    icon,
    AddEventModal,
  },
  data() {
    return {
      user: {
        first_name: "John",
      },
      currentMonth: dayjs().startOf("month"),
      weekDays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
      selectedDate: null,
      showEventModal: false,
      selectedEvent: null,
    };
  },
  computed: {
    ...mapStores(useFetchDataStore),
    events() {
      return this.fetchDataStore.calendarEvents || [];
    },
    monthYear() {
      return this.currentMonth.format("MMMM YYYY");
    },
    calendarDays() {
      const startOfMonth = this.currentMonth.startOf("month");
      const endOfMonth = this.currentMonth.endOf("month");
      const startDay = startOfMonth.day();
      const days = [];

      for (let i = 0; i < startDay; i++) {
        days.push(startOfMonth.subtract(startDay - i, "day"));
      }

      for (let i = 1; i <= endOfMonth.date(); i++) {
        days.push(
          dayjs(
            `${this.currentMonth.format("YYYY-MM")}-${String(i).padStart(
              2,
              "0"
            )}`
          )
        );
      }

      while (days.length < 42) {
        days.push(days[days.length - 1].add(1, "day"));
      }

      return days;
    },
    formattedEventDate() {
      return this.selectedEvent ? this.formatDate(this.selectedEvent) : "";
    },
    todaysEvents() {
      return this.events.filter((e) =>
        dayjs(e.startDate).isSame(dayjs(), "day")
      );
    },
    upcomingEvents() {
      return this.events
        .filter((e) => dayjs(e.startDate).isAfter(dayjs(), "day"))
        .sort((a, b) => dayjs(a.startDate).diff(dayjs(b.startDate)));
    },
    pastEvents() {
      return this.events
        .filter((e) => dayjs(e.startDate).isBefore(dayjs(), "day"))
        .sort((a, b) => dayjs(b.startDate).diff(dayjs(a.startDate)));
    },
  },
  created() {
    this.fetchDataStore.fetchCalendarEvents();
  },
  methods: {
    formatDate(event) {
      const start = dayjs(event.startDate);
      const end = dayjs(event.endDate);
      if (event.isAllDay) {
        return start.isSame(end, "day")
          ? start.format("MMM D, YYYY")
          : `${start.format("MMM D, YYYY")} - ${end.format("MMM D, YYYY")}`;
      }
      return `${start.format("MMM D, YYYY")} ${event.timeStart} - ${end.format(
        "MMM D, YYYY"
      )} ${event.timeEnd}`;
    },
    prevMonth() {
      this.currentMonth = this.currentMonth.subtract(1, "month");
    },
    nextMonth() {
      this.currentMonth = this.currentMonth.add(1, "month");
    },
    isToday(date) {
      return date.isSame(dayjs(), "day");
    },
    hasEvent(date) {
      return this.getEventsByDate(date).length > 0;
    },
    getEventsByDate(date) {
      const day = dayjs(date);
      return this.events.filter((e) =>
        day.isBetween(dayjs(e.startDate), dayjs(e.endDate), "day", "[]")
      );
    },
    selectDate(date) {
      this.selectedDate = date;
      this.showEventModal = true;
    },
    async addEvent(event) {
      try {
        await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/calendar/add-calendar-event",
          event
        );
        await this.fetchDataStore.fetchCalendarEvents();
        this.showEventModal = false;
        toast.success("Event added successfully!");
      } catch (err) {
        toast.error("Failed to add event");
      }
    },
    cancelEvent() {
      this.showEventModal = false;
    },
    openEventDetails(event) {
      this.selectedEvent = { ...event };
    },
    closeEventModal() {
      this.selectedEvent = null;
    },
    async saveEvent() {
      try {
        await axios.patch(
          process.env.VUE_APP_API_BASE_URL +
            `/calendar/update-calendar-event/${this.selectedEvent.id}`,
          this.selectedEvent
        );
        await this.fetchDataStore.fetchCalendarEvents();
        this.closeEventModal();
        toast.success("Event updated successfully!");
      } catch (err) {
        toast.error("Failed to update event");
      }
    },
    async deleteEvent() {
      try {
        await axios.delete(
          process.env.VUE_APP_API_BASE_URL +
            `/calendar/delete-calendar-event/${this.selectedEvent.id}`
        );
        await this.fetchDataStore.fetchCalendarEvents();
        this.closeEventModal();
        toast.success("Event deleted successfully!");
      } catch (err) {
        toast.error("Failed to delete event");
      }
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap");
</style>
