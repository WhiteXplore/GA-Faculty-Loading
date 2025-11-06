<template>
  <!-- Top Bar -->
  <div
    class="bg-white shadow-md px-4 py-2 flex justify-between items-center rounded-t-lg"
  >
    <!-- Left Section: Title -->
    <div class="text-green-900 font-bold text-lg tracking-wide">
      Faculty Loading & Exam Scheduler
    </div>

    <!-- Center Section: Date, Time -->
    <div class="flex flex-col items-center">
      <div class="text-center">
        <div class="text-sm font-medium text-gray-600">
          {{ formattedDate }}
        </div>
        <div class="text-sm text-gray-500">
          {{ formattedTime }}
        </div>
      </div>
    </div>

    <!-- Right Section -->
    <div class="flex items-center gap-5">
      <!-- Dropdown if more than one active year -->
      <div
        v-if="activeYears.length > 1"
        class="relative flex items-center gap-2"
      >
        <!-- Select Container -->
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

        <!-- Arrow Icon Outside -->
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
            alt="Profile Picture"
            class="w-full h-full rounded-full object-cover"
          />
        </div>

        <div class="text-left leading-tight">
          <h1 class="text-sm font-semibold text-gray-800">
            {{ user.last_name }}, {{ user.first_name || "Guest" }}
          </h1>
          <h2 class="text-xs text-gray-500">{{ user.role || "No Role" }}</h2>
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

export default {
  name: "TopBarPage",
  components: { Profile },
  data() {
    return {
      isOpenProfile: false,
      user: {},
      activeYears: [],
      selectedSchoolYearId: "",
      currentTime: new Date(),
      lastUpdatedAt: null,
      yearCheckInterval: null,
      activeYear: null,
      isDropdownOpen: false,
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
  },

  methods: {
    toggleOpenProfile() {
      this.isOpenProfile = !this.isOpenProfile;
    },

    handleClickOutside(event) {
      const dropdown = this.$refs.profileDropdown;
      const icon = this.$refs.profileIcon;
      if (
        this.isOpenProfile &&
        dropdown &&
        !dropdown.contains(event.target) &&
        icon &&
        !icon.contains(event.target)
      ) {
        this.isOpenProfile = false;
      }
    },

    async fetchUser() {
      try {
        const response = await axios.get("http://localhost:8000/auth/me", {
          withCredentials: true,
        });
        if (response.data) {
          this.user = response.data;
        } else {
          this.$router.push("/");
          location.reload();
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },

    async fetchActiveYears() {
      try {
        const response = await axios.get(
          "http://localhost:8000/school-year/get-school-years"
        );
        const allYears = response.data;
        this.activeYears = allYears.filter((sy) => sy.is_active);

        if (this.activeYears.length === 0) {
          this.activeYear = null;
          return;
        }

        // Sort by updated_at descending
        this.activeYears.sort(
          (a, b) => new Date(b.updated_at) - new Date(a.updated_at)
        );

        const latest = this.activeYears[0];

        if (
          !this.activeYear ||
          this.activeYear.school_year_id !== latest.school_year_id ||
          this.activeYear.updated_at !== latest.updated_at
        ) {
          this.activeYear = latest;
          this.selectedSchoolYearId = latest.school_year_id;
          this.lastUpdatedAt = new Date(latest.updated_at);

          // Reload courses for this active year
          this.loadCoursesForActiveYear();
        }
      } catch (error) {
        console.error("❌ Failed to fetch school years:", error);
      }
    },

    async updateSchoolYear() {
      try {
        const selectedSY = this.activeYears.find(
          (sy) => sy.school_year_id === this.selectedSchoolYearId
        );
        if (!selectedSY) return;

        await axios.patch(
          `http://localhost:8000/school-year/update-timestamp/${selectedSY.school_year_id}`
        );

        console.log(
          "✅ Updated timestamp for school year:",
          selectedSY.school_year_name
        );

        const prevSelected = this.selectedSchoolYearId;
        await this.fetchActiveYears();
        this.selectedSchoolYearId = prevSelected;
      } catch (error) {
        console.error("❌ Failed to update school year timestamp:", error);
      }
    },

    getSemesterLabel(semester) {
      if (semester === 1) return "1st Semester";
      if (semester === 2) return "2nd Semester";
      return "";
    },
  },

  mounted() {
    this.fetchUser();
    this.fetchActiveYears();
  },
};
</script>
