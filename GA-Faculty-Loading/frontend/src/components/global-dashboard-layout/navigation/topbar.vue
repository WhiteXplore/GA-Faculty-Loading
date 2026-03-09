<template>
  <div
    class="bg-white shadow-md px-3 py-2 flex justify-between items-center rounded-t-lg"
  >
    <!-- Left: Title -->
    <div class="text-green-900 font-semibold text-md tracking-wide">
      Faculty Loading & Exam Scheduler
    </div>

    <!-- Center: Date/Time -->
    <div class="flex flex-col items-center">
      <div class="text-sm font-medium text-gray-600">{{ formattedDate }}</div>
      <!-- <div class="text-sm text-gray-500">{{ formattedTime }}</div> -->
    </div>

    <!-- Right: Dropdown + Profile -->
    <div class="flex items-center gap-2">
      <!-- Dropdown -->
      <div v-if="activeYears.length > 1" class="relative flex items-center">
        <select
          v-model="selectedSchoolYearId"
          @change="updateSchoolYear"
          @focus="isDropdownOpen = true"
          @blur="isDropdownOpen = false"
          class="appearance-none rounded-full border border-green-600 bg-white py-2 pl-4 pr-10 text-center text-green-900 text-sm font-semibold shadow-md cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-lg"
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

        <!-- Custom Dropdown Icon -->
        <div
          class="pointer-events-none absolute right-3 flex items-center transition-transform duration-300 text-green-700"
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
          { withCredentials: true },
        );
        this.user = res.data || {};
      } catch {
        this.$router.push("/");
      }
    },

    async fetchSchoolYears() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years",
        );
        this.schoolYears = res.data.map((y) => ({ ...y }));

        // Auto-select the most recent active year if nothing is selected
        if (!this.selectedSchoolYearId) {
          this.autoSelectActiveYear();
        }
      } catch (err) {
        console.error(err);
      }
    },

    autoSelectActiveYear() {
      const activeList = this.activeYears.sort(
        (a, b) => new Date(b.updated_at) - new Date(a.updated_at),
      );

      if (activeList.length > 0) {
        this.selectedSchoolYearId = activeList[0].school_year_id;

        // Emit full object to eventBus
        eventBus.emit(activeList[0]);
      }
    },

    getSemesterLabel(sem) {
      return sem === 1 ? "1st Semester" : sem === 2 ? "2nd Semester" : "";
    },

    async updateSchoolYear() {
      const selectedSY = this.schoolYears.find(
        (y) => y.school_year_id === this.selectedSchoolYearId,
      );
      if (!selectedSY) return;

      try {
        // Update timestamp (backend)
        await axios.patch(
          process.env.VUE_APP_API_BASE_URL +
            `/school-year/update-timestamp/${selectedSY.school_year_id}`,
        );

        // Emit the full school year object to eventBus for reactive listeners
        eventBus.emit(selectedSY);
      } catch (err) {
        console.error("Failed to update school year:", err);
      }
    },
  },

  mounted() {
    this.fetchUser();
    this.fetchSchoolYears();

    // Listen to eventBus for updates
    this.stopBus = eventBus.on(async (newSY) => {
      if (!newSY) return;

      // Refetch school years to get updated is_active status
      await this.fetchSchoolYears();

      // Select the new active year if it’s active
      if (newSY.is_active) {
        this.selectedSchoolYearId = newSY.school_year_id;
      }
    });
  },

  beforeUnmount() {
    if (this.stopBus) this.stopBus();
  },
};
</script>
