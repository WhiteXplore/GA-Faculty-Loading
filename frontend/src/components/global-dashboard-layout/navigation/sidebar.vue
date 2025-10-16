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
            'text-[12px] font-medium tracking-wider': isExpanded,
            hidden: !isExpanded,
          }"
        >
          {{ user.email }}
        </p>
      </div>

      <div v-if="isExpanded" class="w-full h-0.5 bg-[#fbfbfb] mt-4"></div>

      <!-- Dynamic Menu -->
      <div class="flex flex-col mt-6 gap-2 tracking-wide text-[12px] w-full overflow-y-auto max-h-[calc(100vh-200px)] pr-2 scrollbar-thin">
        <template v-for="section in roleMenuSections" :key="section.title">
          <div v-if="isExpanded" class="text-md text-white mt-1 text-left">
            {{ section.title }}
          </div>
          <div v-for="item in section.items" :key="item.name" class="w-full">
            <!-- Non-children router-link -->
            <router-link
              v-if="!item.children"
              :to="item.route"
              class="flex items-center w-full gap-5 p-2 rounded-md transition-all duration-200"
              :class="[
                $route.path.startsWith(item.route)
                  ? 'bg-white text-green-700'
                  : 'text-white hover:bg-white hover:text-gray-800',
                !isExpanded ? 'justify-center' : 'justify-start',
              ]"
            >
              <icon :name="item.icon" />
              <span v-show="isExpanded">{{ item.name }}</span>
            </router-link>

            <!-- Collapsible Parent -->
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
                    class="block w-full py-2 px-[60px] text-[12px] transition-all duration-200 text-left border border-white"
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
        'ml-16': !isExpanded,
        'ml-64': isExpanded,
      }"
      class="flex-grow transition-all pt-2 min-h-screen rounded-t-xl overflow-y-auto z-50"
    >
      <slot>
        <div class="bg-white w-auto min-h-screen shadow mr-2 rounded-t-xl">
          <adminTopbar />
          <div class="p-2">
            <router-view></router-view>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import adminTopbar from "../../../components/global-dashboard-layout/navigation/topbar.vue";
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
            title: "Records",
            items: [
              {
                name: "Setup",
                icon: "setting",
                children: [
                  // { name: "Instructors", route: "/instructors" },
                  { name: "Institutes", route: "/institutes" },
                  { name: "Curriculum", route: "/curriculums" },
                  { name: "Courses", route: "/courses" },
                  { name: "Specializations", route: "/specializations" },
                  { name: "Rooms", route: "/rooms" },
                  { name: "School Years", route: "/school-years" },
                  { name: "System Overview", route: "/system-overview" },
                ],
              },
              { name: "Faculty List", icon: "users", route: "/instructors" },
              {
                name: "Class List",
                icon: "folder",
                route: "/admin-assign-classes",
              },
              {
                name: "Classes",
                icon: "folder",
                route: "/classes",
              },
            ],
          },
          {
            title: "Generation",
            items: [
              {
                icon: "arrow-path",
                name: "Faculty Loading",
                route: "/faculty-loads",
              },
              {
                icon: "folder",
                name: "Exam Scheduling",
                route: "/exam-loading",
              },
            ],
          },
          {
            title: "Documents",
            items: [
              {
                name: "Reports",
                icon: "reports",
                children: [
                  { name: "Prospectus", route: "/report-curriculum-offers" },
                ],
              },
            ],
          },
          {
            title: "Accounts",
            items: [
              {
                name: "User Management",
                icon: "users",
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
                name: "Courses",
                icon: "setting",
                route: "/program-courses",
              },
              {
                name: "Specializations",
                icon: "setting",
                route: "/program-specializations",
              },
              {
                name: "Programs",
                icon: "setting",
                route: "/program-programs",
              },
              {
                name: "Add Year/Section",
                icon: "add-students",
                route: "/add-year-section",
              },
              {
                name: "Assign Classes",
                icon: "reports",
                route: "/program-chairperson-assign-classes",
              },
            ],
          },

          {
            title: "Load Management",
            items: [
              {
                name: "Load Generation",
                icon: "arrow-path",
                route: "/load-generation",
              },
              {
                name: "Faculty Loading",
                icon: "users",
                route: "/program-faculty-loading",
              },
            ],
          },
          {
            title: "Documents",
            items: [
              {
                name: "Prospectus",
                icon: "reports",
                route: "/report-curriculum-offers",
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
        const response = await axios.get("http://localhost:8000/auth/me", {
          withCredentials: true,
        });
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

/* Custom scrollbar for dropdown menus */
.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* For Firefox */
.scrollbar-thin {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}
</style>
