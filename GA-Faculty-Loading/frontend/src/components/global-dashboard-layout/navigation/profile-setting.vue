<template>
  <!-- Profile Menu -->
  <div
    v-if="isProfileMenuOpen"
    @mouseenter="isProfileMenuOpen = true"
    @mouseleave="isProfileMenuOpen = false"
    class="bg-white shadow border w-full h-full p-3 text-[13px] cursor-pointer rounded-lg inset-0 z-50"
    @click.stop
  >
    <div class="space-y-2 w-[140px]">
      <router-link to="/profile-view" @click="toggleCloseProfile">
        <div
          class="flex items-center hover:bg-blue-500 hover:text-white rounded-md w-auto py-1 px-2 gap-2"
        >
          <icon name="users" />
          <div>Profile</div>
        </div>
      </router-link>

      <div
        class="flex items-center hover:bg-red-500 hover:text-white rounded-md w-auto py-1 px-2 gap-2"
      >
        <icon name="logout" />
        <div @click="toggleOpenLogout">Logout</div>
      </div>
    </div>
  </div>

  <!-- Logout Modal -->
  <Logout :isOpen="isOpenLogout" @close="isOpenLogout = false" />
</template>

<script>
import Logout from "./alert/logout.vue";
import icon from "@/assets/icon.vue";
export default {
  name: "ProfilePage",
  components: {
    Logout,
    icon,
  },
  data() {
    return {
      isOpenLogout: false,
      isProfileMenuOpen: true,
    };
  },
  methods: {
    toggleCloseProfile() {
      this.isProfileMenuOpen = false;
    },
    toggleOpenLogout() {
      this.isOpenLogout = true; // Show the logout modal
    },
  },
  watch: {
    $route(to) {
      if (to.path === "/profile-view") {
        this.isProfileMenuOpen = false;
      }
    },
  },
  mounted() {
    if (this.$route.path === "/profile-view") {
      this.isProfileMenuOpen = false;
    }
  },
};
</script>
