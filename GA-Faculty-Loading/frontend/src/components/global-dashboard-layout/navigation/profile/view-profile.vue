<template>
  <div
    v-if="currentUser"
    class="p-6 text-gray-800 w-full min-h-[70vh] bg-[#F4F6F8] rounded-t-xl"
  >
    <!-- Header -->
    <div class="flex justify-between items-center pr-5">
      <div>
        <h1 class="text-2xl font-bold text-left mb-1">Account Settings</h1>
        <p class="text-sm text-gray-500 mb-5 text-left">
          Manage your personal details and security preferences here.
        </p>
      </div>
    </div>

    <!-- Main Layout with Sidebar -->
    <div class="flex h-[80vh] overflow-hidden rounded-xl bg-white">
      <!-- Sidebar -->
      <div class="w-64 border-r bg-white p-4">
        <ul class="space-y-2">
          <li>
            <button
              @click="activeTab = 'profile'"
              :class="[
                'w-full text-left px-3 py-2 rounded-lg',
                activeTab === 'profile'
                  ? 'bg-defaultGreen text-white font-semibold'
                  : 'hover:bg-gray-100',
              ]"
            >
              My Profile
            </button>
          </li>
          <li>
            <button
              @click="activeTab = 'preference'"
              :class="[
                'w-full text-left px-3 py-2 rounded-lg',
                activeTab === 'preference'
                  ? 'bg-defaultGreen text-white font-semibold'
                  : 'hover:bg-gray-100',
              ]"
            >
              Preference
            </button>
          </li>
        </ul>
      </div>

      <!-- Content Area -->
      <div class="flex-1 p-6 overflow-auto">
        <!-- Profile Info Section -->
        <div v-if="activeTab === 'profile'">
          <h2 class="text-xl font-semibold mb-4">My Profile</h2>
          <div class="space-y-3">
            <personalInformation :user="currentUser" @edit="openEditModal" />
          </div>
        </div>

        <!-- Preference Section -->
        <div v-if="activeTab === 'preference'">
          <h2 class="text-xl font-semibold">Preferences</h2>
          <p class="text-gray-600">
            This is where you can manage your system preferences and settings.
          </p>
          <preferenceSection :user="currentUser" @add="openAddModal" />
        </div>
      </div>
    </div>

    <!-- Modals -->
    <addExpertise
      :userData="currentUser"
      v-if="showAddModal"
      @close="showAddModal = false"
      @updated="fetchRawUsers"
    />
    <addInstructor
      v-if="showEditModal"
      :isEdit="true"
      :userData="currentUser"
      @close="showEditModal = false"
      @updated="fetchRawUsers"
    />
  </div>

  <!-- Loading State -->
  <div v-else class="flex justify-center items-center h-screen">
    <p class="text-gray-500">Loading profile...</p>
  </div>
</template>

<script>
// import icon from "@/assets/icon.vue";
import axios from "axios";
import addInstructor from "@/components/faculty/faculty-records/modals/add-users.vue";
import addExpertise from "@/components/faculty/faculty-records/modals/add-expertise.vue";
import personalInformation from "./personal-information.vue";
import preferenceSection from "./preference-section.vue";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "ProfileContentPage",
  components: {
    // icon,
    addInstructor,
    addExpertise,
    personalInformation,
    preferenceSection,
  },
  data() {
    return {
      subId: null,
      showEditModal: false,
      showAddModal: false,
      activeTab: "profile", // default tab
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rawusers"]),
    currentUser() {
      if (!this.subId || !this.rawusers) return null;
      return this.rawusers.find((u) => u.id === this.subId) || null;
    },
  },
  methods: {
    ...mapActions(useFetchDataStore, ["fetchRawUsers"]),
    async getSubId() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          }
        );
        if (response.data && response.data.sub) {
          this.subId = response.data.sub;
          await this.fetchRawUsers();
        } else {
          this.$router.push("/");
          location.reload();
        }
      } catch (error) {
        console.error("Failed to fetch logged user:", error);
        this.$router.push("/");
      }
    },
    openAddModal() {
      this.showAddModal = true;
    },
    openEditModal() {
      this.showEditModal = true;
    },
  },
  async mounted() {
    await this.getSubId();
  },
};
</script>
