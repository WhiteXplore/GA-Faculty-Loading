<template>
  <div
    class="bg-white shadow-md px-4 py-2 flex justify-between items-center rounded-t-lg"
  >
    <!-- Left: Title -->
    <div class="text-green-900 font-bold text-lg tracking-wide">
      Faculty Loading & Exam Scheduler
    </div>

    <!-- Center: Date/Time -->
    <div class="flex flex-col items-center">
      <div class="text-sm font-medium text-gray-600">{{ formattedDate }}</div>
      <div class="text-sm text-gray-500">{{ formattedTime }}</div>
    </div>

    <!-- Right: Dropdown + Profile -->
    <div class="flex items-center gap-2">
      <!-- Dropdown -->
      <div
        v-if="activeYears.length > 1"
        class="relative flex items-center gap-2"
      >
        <select
          v-model="selectedSchoolYearId"
          @change="updateSchoolYear"
          @focus="isDropdownOpen = true"
          @blur="isDropdownOpen = false"
          class="appearance-none rounded-full border border-green-600 bg-white px-4 py-1.5 w-52 text-green-900 text-sm font-semibold shadow-md cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 focus:outline-none hover:shadow-lg"
        >
          <option value="" disabled>Select Active School Year</option>
          <option
            v-for="sy in activeYears"
            :key="sy.school_year_id"
            :value="sy.school_year_id"
          >
            {{ sy.school_year_name }} — {{ getSemesterLabel(sy.semester) }}
          </option>
        </select>

        <div
          class="transition-transform duration-300 text-green-700 cursor-pointer"
          :class="{ 'rotate-180': isDropdownOpen }"
        >
          <svg
            class="w-5 h-5"
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

      <!-- Static text if one or none -->
      <div
        v-else
        class="bg-green-50 border border-green-600 rounded-full px-5 py-1.5 shadow-md text-green-900 text-sm font-semibold flex items-center justify-center"
      >
        <span v-if="activeYears.length === 1">
          {{ activeYears[0].school_year_name }} —
          {{ getSemesterLabel(activeYears[0].semester) }}
        </span>
        <span v-else class="text-gray-500">No Active Year</span>
      </div>

      <!-- Profile -->
      <div class="flex items-center gap-2">
        <div
          ref="profileIcon"
          class="w-10 h-10 rounded-full border-2 border-transparent hover:border-green-500 cursor-pointer transition"
          @click.stop="toggleOpenProfile"
        >
          <img
            src="../../../assets/img/users.png"
            alt="Profile"
            class="w-full h-full rounded-full object-cover"
          />
        </div>

        <div class="text-left leading-tight">
          <h1 class="text-sm font-semibold text-gray-800">
            {{ user.last_name }}, {{ user.first_name || "Guest" }}
          </h1>
          <h2 class="text-xs text-gray-500">
            {{ user.role || "No Role" }}
          </h2>
        </div>
      </div>
    </div>
  </div>

  <!-- Profile Dropdown -->
  <div class="absolute top-[70px] right-6 z-50" ref="profileDropdown">
    <Profile v-if="isOpenProfile" />
  </div>
</template>

<script>
import axios from "axios";
import Profile from "./profile-setting.vue";
import { eventBus } from "@/bus/event-bus";

export default {
  name: "TopBarPage",
  components: { Profile },
  data() {
    return {
      isOpenProfile: false,
      user: {},
      schoolYears: [],
      selectedSchoolYearId: "",
      currentTime: new Date(),
      isDropdownOpen: false,
      stopBus: null,
    };
  },
  computed: {
    formattedDate() {
      return this.currentTime.toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "2-digit",
        year: "numeric",
      });
    },
    formattedTime() {
      return this.currentTime.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      });
    },
    activeYears() {
      return this.schoolYears.filter((y) => y.is_active);
    },
  },
  methods: {
    toggleOpenProfile() {
      this.isOpenProfile = !this.isOpenProfile;
    },
    async fetchUser() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          { withCredentials: true }
        );
        this.user = res.data || {};
      } catch {
        this.$router.push("/");
      }
    },
    async fetchSchoolYears() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years"
        );
        this.schoolYears = res.data.map((y) => ({ ...y }));

        // auto-select if no selection
        if (!this.selectedSchoolYearId) {
          this.autoSelectActiveYear();
        }
      } catch (err) {
        console.error(err);
      }
    },
    async updateSchoolYear() {
      const selectedSY = this.schoolYears.find(
        (y) => y.school_year_id === this.selectedSchoolYearId
      );
      if (!selectedSY) return;

      await axios.patch(
        process.env.VUE_APP_API_BASE_URL +
          `/school-year/update-timestamp/${selectedSY.school_year_id}`
      );

      // emit change to event bus
      eventBus.emit(selectedSY.school_year_id);

      // optionally refetch updated school years
      await this.fetchSchoolYears();
    },
    autoSelectActiveYear() {
      // Get all active school years
      const activeList = this.schoolYears
        .filter((y) => y.is_active)
        .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));

      // If there are active years, pick the most recent one
      if (activeList.length > 0) {
        this.selectedSchoolYearId = activeList[0].school_year_id;
        return;
      }

      // Fallback: pick most recently updated even if not active
      const fallback = [...this.schoolYears].sort(
        (a, b) => new Date(b.updated_at) - new Date(a.updated_at)
      )[0];

      this.selectedSchoolYearId = fallback?.school_year_id || "";
    },
    getSemesterLabel(sem) {
      return sem === 1 ? "1st Semester" : sem === 2 ? "2nd Semester" : "";
    },
  },
  mounted() {
    this.fetchUser();
    this.fetchSchoolYears();

    // Reactive event bus listener
    this.stopBus = eventBus.on(async (newSchoolYearId) => {
      await this.fetchSchoolYears();
      this.selectedSchoolYearId = newSchoolYearId;
    });
  },

  beforeUnmount() {
    if (this.stopBus) this.stopBus();
  },
};
</script>
