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
    <div class="flex items-center gap-3">
      <!-- Year Selector -->
      <div class="relative w-26">
        <select
          id="year"
          v-model="selectedYear"
          @change="updateYear"
          class="w-full appearance-none rounded-full border border-green-600 bg-white px-4 py-1.5 pr-10 text-green-900 text-sm font-semibold shadow-md cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 focus:outline-none hover:shadow-lg"
        >
          <option
            v-for="year in years"
            :key="year"
            :value="year"
            class="text-sm"
          >
            {{ year }}
          </option>
        </select>

        <!-- Custom Dropdown Icon -->
        <div
          class="pointer-events-none absolute inset-y-0 right-3 flex items-center text-green-700"
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

      <!-- Profile -->
      <div class="flex items-center gap-2">
        <!-- Profile Picture -->
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

        <!-- User Info -->
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
import { useFetchDataStore } from "@/store/fetch-data-store";

export default {
  name: "TopBarPage",
  components: { Profile },
  data() {
    const currentYear = new Date().getFullYear();
    return {
      isOpenProfile: false,
      user: {},
      selectedYear: currentYear,
      years: Array.from({ length: 10 }, (_, i) => currentYear - i),
      currentTime: new Date(),
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
  mounted() {
    this.fetchUser();
    this.fetchActiveYear();

    this.timer = setInterval(() => {
      this.currentTime = new Date();
    }, 1000);

    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    clearInterval(this.timer);
    document.removeEventListener("click", this.handleClickOutside);
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

    async fetchActiveYear() {
      try {
        const res = await axios.get("http://localhost:8000/active-year/active");
        if (res.data) {
          this.selectedYear = res.data.year;

          // 👇 sync to store so TableCourses reacts
          const store = useFetchDataStore();
          store.year = res.data.year;
        }
      } catch (error) {
        console.error("Failed to fetch active year:", error);
      }
    },

    async updateYear() {
      try {
        const res = await axios.post("http://localhost:8000/active-year", {
          year: this.selectedYear,
        });
        if (res.data?.year) {
          this.selectedYear = res.data.year;

          // 👇 sync to store so TableCourses refreshes
          const store = useFetchDataStore();
          store.year = res.data.year;
        }
      } catch (error) {
        console.error("Failed to update active year:", error);
      }
    },
  },
};
</script>
