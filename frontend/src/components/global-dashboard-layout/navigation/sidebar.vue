<template>
  <div class="bg-defaultGreen w-screen h-screen flex animate-scaleUp">
    <!-- Sidebar -->
    <div
      :class="{ 'w-16': !isExpanded, 'w-64': isExpanded }"
      class="h-full fixed left-0 top-0 bg-defaultGreen text-white p-3 transition-all duration-300 ease-in-out"
      v-if="user.role"
    >
      <!-- Toggle Sidebar -->
      <div @click="toggleSidebar" class="justify-end flex">
        <icon
          :name="'burger'"
          class="cursor-pointer"
          :class="{ 'mr-3 mt-1': !isExpanded }"
        />
      </div>

      <!-- Logo and user info -->
      <div class="flex flex-col items-center justify-center w-full">
        <img
          src="../../../assets/img/dnsc_logo.png"
          alt="Logo"
          :class="{
            'w-16 rounded-full border-white border ': isExpanded,
            hidden: !isExpanded,
          }"
          whitespace-nowrap
        />
        <p
          :class="{
            'text-sm font-medium mt-2': isExpanded,
            hidden: !isExpanded,
          }"
        >
          {{ user.first_name }}
        </p>
        <p
          :class="{
            'text-[13px] font-medium tracking-wider': isExpanded,
            hidden: !isExpanded,
          }"
        >
          {{ user.email }}
        </p>
      </div>

      <div v-if="isExpanded" class="w-full h-0.5 bg-[#fbfbfb] mt-4"></div>

      <!-- Dynamic Menu -->
      <div
        class="flex flex-col mt-6 gap-2 tracking-wide text-[13px] w-full overflow-auto max-h-[calc(100vh-200px)] pr-2 scrollbar-glass"
      >
        <template v-for="section in roleMenuSections" :key="section.title">
          <div v-if="isExpanded" class="text-md text-white mt-1 text-left">
            {{ section.title }}
          </div>
          <!-- Collapsible Parent / Non-children items -->
          <div v-for="item in section.items" :key="item.name" class="w-full">
            <!-- Special sync item for Program Chairperson -->
            <div
              v-if="item.name === 'Class & Assigned Courses'"
              @click="syncProgramYearCourses(item.route)"
              class="flex items-center w-full gap-5 rounded-md transition-all duration-200 cursor-pointer select-none"
              :class="[
                $route.path.startsWith(item.route)
                  ? 'bg-white text-green-700 p-2'
                  : 'text-white hover:bg-white hover:text-gray-800 p-2 hover:p-2',
                !isExpanded ? 'justify-center h-8' : 'justify-start p-2',
              ]"
            >
              <icon :name="item.icon" />
              <span v-show="isExpanded">{{ item.name }}</span>
            </div>

            <!-- Default router-link for all other non-children items -->
            <router-link
              v-else-if="!item.children"
              :to="item.route"
              class="flex items-center w-full gap-5 rounded-md transition-all duration-200"
              :class="[
                $route.path.startsWith(item.route)
                  ? 'bg-white text-green-700 p-2'
                  : 'text-white hover:bg-white hover:text-gray-800 p-2 hover:p-2',
                !isExpanded ? 'justify-center h-8' : 'justify-start p-2',
              ]"
            >
              <icon :name="item.icon" />
              <span v-show="isExpanded">{{ item.name }}</span>
            </router-link>

            <!-- Collapsible Parent items -->
            <div v-else>
              <div
                @click="toggleDropdown(item.name)"
                class="flex items-center justify-between w-full p-2 cursor-pointer transition-all duration-200"
                :class="[
                  isDropdownOpen === item.name
                    ? `bg-white text-gray-800 ${
                        !isExpanded ? 'rounded-md' : 'rounded-t-md'
                      }`
                    : 'text-white hover:bg-white hover:text-gray-800 hover:rounded-md',
                ]"
              >
                <div
                  :class="[
                    !isExpanded
                      ? 'justify-center w-full'
                      : 'justify-start gap-5',
                  ]"
                  class="flex items-center"
                >
                  <icon :name="item.icon" />
                  <span v-show="isExpanded">{{ item.name }}</span>
                </div>
                <icon
                  name="arrow-down"
                  v-show="isExpanded"
                  class="transition-transform"
                  :class="{ 'rotate-180': isDropdownOpen === item.name }"
                />
              </div>

              <transition name="slide">
                <div
                  v-show="isDropdownOpen === item.name && isExpanded"
                  class="max-h-[400px] overflow-y-auto scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-100"
                >
                  <router-link
                    v-for="(sub, index) in item.children"
                    :key="sub.name"
                    :to="sub.route"
                    class="block w-full py-2 px-[60px] text-[13px] transition-all duration-200 text-left border border-white"
                    :class="[
                      $route.path.startsWith(sub.route)
                        ? 'bg-defaultGreen text-white '
                        : 'bg-white text-gray-800 hover:bg-gray-200',
                      index === item.children.length - 1
                        ? 'rounded-b-md border border-white'
                        : '',
                    ]"
                  >
                    {{ sub.name }}
                  </router-link>
                </div>
              </transition>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Main Content -->
    <div
      :class="{
        'ml-[55px]': !isExpanded,
        'ml-[247px]': isExpanded,
      }"
      class="flex-grow transition-all pt-2 min-h-screen rounded-t-xl overflow-y-auto z-50"
    >
      <slot>
        <div class="bg-white w-auto min-h-screen shadow mr-2 rounded-t-xl">
          <adminTopbar />
          <div class="">
            <router-view></router-view>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import adminTopbar from "./Topbar.vue";
import axios from "axios";

export default {
  name: "AdminSidebar",
  components: { icon, adminTopbar },
  data() {
    return {
      isExpanded: false,
      isDropdownOpen: null,
      user: {},

      menuItemsByRole: {
        Admin: [
          {
            title: "Home",
            items: [
              {
                name: "Dashboard",
                icon: "dashboard",
                route: "/admin-dashboard",
              },
            ],
          },
          {
            title: "Records Management",
            items: [
              {
                name: "Setup",
                icon: "set-up",
                children: [
                  // { name: "Instructors", route: "/instructors" },
                  { name: "Institutes", route: "/institutes" },
                  { name: "Curriculum", route: "/curriculum" },
                  { name: "Courses", route: "/courses" },
                  { name: "Rooms", route: "/rooms" },
                  { name: "School Years", route: "/school-years" },
                  { name: "System Overview", route: "/system-overview" },
                ],
              },
              {
                name: "Faculty List",
                icon: "faculty-list",
                route: "/instructors",
              },

              // {
              //   name: "Assigned Course",
              //   icon: "class-list",
              //   route: "/admin-assigned-courses",
              // },
              {
                name: "Year & Section",
                icon: "class-list",
                route: "/year-section",
              },
            ],
          },
          {
            title: "Generation",
            items: [
              {
                icon: "faculty-loading",
                name: "Faculty Loading",
                route: "/faculty-loads",
              },
            ],
          },
          {
            title: "Documents",
            items: [
              {
                icon: "prospectus",
                name: "Prospectus",
                route: "/report-curriculum-offers",
              },
            ],
          },
          {
            title: "Accounts",
            items: [
              {
                name: "User Management",
                icon: "user-account",
                children: [{ name: "Users list", route: "/user-accounts" }],
              },
            ],
          },
        ],

        "Program Chairperson": [
          {
            title: "Home",
            items: [
              {
                name: "Dashboard",
                icon: "dashboard",
                route: "/progchair-dashboard",
              },
            ],
          },
          {
            title: "Record Management",
            items: [
              {
                name: "Setup",
                icon: "set-up",
                children: [
                  { name: "Courses", route: "/program-chair-courses" },
                  {
                    name: "Year & Section",
                    route: "/program-chair-year-section",
                  },
                  // {
                  //   name: "Assign Course",
                  //   route: "/program-chair-assigned-courses",
                  // },
                ],
              },

              {
                name: "Faculty List",
                icon: "faculty-list",
                route: "/program-chair-faculty-list",
              },
              {
                name: "Class & Assigned Courses",
                icon: "class-list",
                route: "/program-chair-class-assigned-classes",
              },
            ],
          },

          {
            title: "Load Management",
            items: [
              {
                name: "Generated Load",
                icon: "faculty-loading",
                route: "/load-generation",
              },
            ],
          },
          {
            title: "Documents",
            items: [
              {
                name: "Faculty Expertise Overview",
                icon: "expertise",
                route: "/faculty-expertise",
              },
            ],
          },
        ],

        Faculty: [
          {
            title: "Home",
            items: [
              {
                name: "Dashboard",
                icon: "dashboard",
                route: "/faculty-dashboard",
              },
            ],
          },
          {
            title: "My Load",
            items: [
              {
                name: "Loading",
                icon: "users",
                route: "/faculty-load",
              },
            ],
          },
          {
            title: "Setting",
            items: [
              {
                name: "Preference",
                icon: "setting",
                route: "/faculty-preference",
              },
            ],
          },
        ],
      },
    };
  },
  computed: {
    roleMenuSections() {
      return this.menuItemsByRole[this.user.role] || [];
    },
  },
  mounted() {
    this.fetchUser();
    this.expandDropdownForCurrentRoute(this.$route.path);
  },
  watch: {
    "$route.path"(newPath) {
      this.expandDropdownForCurrentRoute(newPath);
    },
  },
  methods: {
    async syncProgramYearCourses(route) {
      try {
        const response = await axios.post(
          process.env.VUE_APP_API_BASE_URL +
            "/program-year-courses/sync-from-classes",
          { withCredentials: true }
        );
        console.log("Sync successful:", response.data);
        this.$router.push(route);
      } catch (error) {
        console.error("Failed to sync:", error);
      }
    },
    toggleSidebar() {
      this.isExpanded = !this.isExpanded;
    },
    toggleDropdown(name) {
      this.isExpanded = true;
      this.isDropdownOpen = this.isDropdownOpen === name ? null : name;
    },
    expandDropdownForCurrentRoute(path) {
      const allDropdownItems = [];
      this.roleMenuSections.forEach((section) => {
        allDropdownItems.push(...section.items);
      });
      for (const item of allDropdownItems) {
        if (item.children) {
          const match = item.children.find((child) =>
            path.startsWith(child.route)
          );
          if (match || path.startsWith(item.route)) {
            this.isExpanded = true;
            this.isDropdownOpen = item.name;
            break;
          }
        }
      }
    },
    async fetchUser() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          }
        );
        if (response.data) {
          this.user = response.data;
          console.log("Authenticated User:", this.user);
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },
  },
};
</script>

<style scoped>
.transition-transform {
  transition: transform 0.1s ease;
}
.slide-enter-active,
.slide-leave-active {
  transition: all 0.1s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
.slide-enter-to,
.slide-leave-from {
  transform: translateY(0);
  opacity: 1;
}

/* 🌿 Glass Effect Scrollbar */
.scrollbar-glass::-webkit-scrollbar {
  width: 6px;
}

.scrollbar-glass::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(6px);
  border-radius: 10px;
}

.scrollbar-glass::-webkit-scrollbar-thumb {
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.35),
    rgba(255, 255, 255, 0.15)
  );
  border-radius: 10px;
  backdrop-filter: blur(4px);
  box-shadow: inset 0 0 6px rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.scrollbar-glass::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.45),
    rgba(255, 255, 255, 0.25)
  );
}

/* 🦊 Firefox Support */
.scrollbar-glass {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.4) rgba(255, 255, 255, 0.1);
}
</style>
