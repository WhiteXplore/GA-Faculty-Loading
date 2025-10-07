<template>
  <div class="w-full bg-white rounded-xl space-y-4">
    <!-- Profile Header -->
    <div class="flex items-center gap-5 border rounded-2xl p-4">
      <img
        src="../../../../assets/img/employee_picture.png"
        alt="Profile Picture"
        class="w-16 h-16 rounded-full"
      />
      <div class="flex justify-between items-center w-full">
        <div class="text-left">
          <p class="text-lg font-semibold">
            {{ user.first_name }} {{ user.last_name }}
          </p>
          <p class="text-sm text-gray-500">{{ user.role || "No Role" }}</p>
        </div>

        <div
          class="gap-1 flex cursor-pointer border border-green-600 text-green-600 px-2 py-1 rounded-lg hover:bg-green-50 transition"
          @click="$emit('edit')"
        >
          <icon :name="'edit'" />
          <button>Edit</button>
        </div>
      </div>
    </div>

    <!-- Personal Info -->
    <div class="text-left p-4 space-y-5 border rounded-2xl">
      <h2 class="text-lg font-semibold tracking-wide">Personal Information</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2">
        <div class="space-y-6">
          <div>
            <label class="text-xs text-gray-500">First Name</label>
            <p class="font-medium">{{ user.first_name }}</p>
          </div>
          <div>
            <label class="text-xs text-gray-500">Institute</label>
            <p class="font-medium">
              {{ user.institute?.institute_name || "No Institute" }}
            </p>
          </div>
          <div>
            <label class="text-xs text-gray-500">Email Address</label>
            <p class="font-medium">{{ user.email || "No Email" }}</p>
          </div>
        </div>

        <div class="space-y-6">
          <div>
            <label class="text-xs text-gray-500">Last Name</label>
            <p class="font-medium">{{ user.last_name }}</p>
          </div>
          <div>
            <label class="text-xs text-gray-500">Program</label>
            <p class="font-medium">
              {{ user.program?.program_name || "No Program" }}
            </p>
          </div>
          <div>
            <label class="text-xs text-gray-500">Contact Number</label>
            <p class="font-medium">{{ user.contact || "No Contact Number" }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";

export default {
  name: "PersonalInfo",
  components: { icon },
  props: {
    user: { type: Object, required: true },
  },
};
</script>
