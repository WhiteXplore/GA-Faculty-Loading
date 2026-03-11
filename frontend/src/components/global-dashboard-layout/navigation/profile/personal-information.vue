<template>
  <div v-if="matchedUser" class="w-full space-y-4">
    <!-- Profile Header -->
    <div class="flex items-center gap-5 border rounded-2xl p-4">
      <img
        src="../../../../assets/img/employee_picture.png"
        alt="Profile Picture"
        class="w-16 h-16 rounded-full"
      />
      <div class="flex justify-between items-center w-full">
        <div class="text-left">
          <div class="flex items-center gap-2">
            <p class="text-lg font-semibold">
              {{ matchedUser.first_name }} {{ matchedUser.last_name }}
            </p>
            <p
              class="inline-block px-2 py-1 rounded-full text-white text-xs font-semibold"
              :class="employmentBadgeColor(matchedUser.employment_type)"
            >
              {{ matchedUser.employment_type || "-" }}
            </p>
          </div>

          <p class="text-sm text-gray-500">
            {{ matchedUser.role || "-" }}
          </p>
        </div>

        <div
          class="gap-1 flex cursor-pointer border border-green-600 text-defaultGreen px-2 py-1 rounded-lg hover:bg-green-50 transition"
          @click="$emit('edit')"
        >
          <icon :name="'edit'" />
          <button>Edit</button>
        </div>
      </div>
    </div>

    <!-- Personal Info -->
    <h2 class="text-lg font-semibold tracking-wide">Personal Information</h2>
    <div class="text-left p-4 space-y-5 border rounded-2xl">
      <div class="grid grid-cols-1 sm:grid-cols-2">
        <div class="space-y-6">
          <div>
            <label class="text-xs text-gray-500">First Name</label>
            <p class="font-medium">{{ matchedUser.first_name }}</p>
          </div>

          <div>
            <label class="text-xs text-gray-500">Email Address</label>
            <p class="font-medium">{{ matchedUser.email || "-" }}</p>
          </div>
        </div>

        <div class="space-y-6">
          <div>
            <label class="text-xs text-gray-500">Last Name</label>
            <p class="font-medium">{{ matchedUser.last_name }}</p>
          </div>

          <div>
            <label class="text-xs text-gray-500">Contact Number</label>
            <p class="font-medium">
              {{ matchedUser.contact || "-" }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Professional / Employment Info -->
    <h2 class="text-lg font-semibold tracking-wide">
      Professional / Employment Information
    </h2>
    <div class="text-left p-4 space-y-5 border rounded-2xl">
      <div class="grid grid-cols-1 sm:grid-cols-2">
        <div class="space-y-6">
          <div>
            <label class="text-xs text-gray-500">Designation</label>
            <p class="font-medium">
              {{ matchedUser.designation || "-" }}
            </p>
          </div>
          <div>
            <label class="text-xs text-gray-500">Institute</label>
            <p class="font-medium">
              {{ matchedUser.institute?.institute_name || "-" }}
            </p>
          </div>
        </div>

        <div class="space-y-6">
          <div>
            <label class="text-xs text-gray-500">Type of Employment</label>
            <p class="font-medium">
              {{ matchedUser.employment_type || "-" }}
            </p>
          </div>
          <div>
            <label class="text-xs text-gray-500">Program</label>
            <p class="font-medium">
              {{ matchedUser.program?.program_name || "-" }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <p v-else class="text-center text-gray-400">User not found.</p>
</template>

<script>
import icon from "@/assets/icon.vue";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState } from "pinia";

export default {
  name: "PersonalInfo",
  components: { icon },
  props: {
    user: { type: Object, required: true },
  },
  computed: {
    ...mapState(useFetchDataStore, ["users"]),

    // Filter the users from store and match with the prop user id
    matchedUser() {
      return this.users.find((u) => u.id === this.user.id) || null;
    },
  },
  methods: {
    employmentBadgeColor(type) {
      switch (type) {
        case "Full Time":
          return "bg-defaultGreen"; // green badge
        case "Part Time":
          return "bg-blue-400"; // blue badge
        default:
          return "bg-gray-400"; // default gray badge
      }
    },
  },

  mounted() {
    const store = useFetchDataStore();
    store.fetchUsers(); // Make sure you fetch users
  },
};
</script>
