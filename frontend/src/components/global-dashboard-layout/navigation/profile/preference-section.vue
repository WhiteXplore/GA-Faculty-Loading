<template>
  <div
    v-if="user.role !== 'Admin'"
    class="w-full lg:flex-1 bg-white rounded-2xl"
  >
    <div class="text-left">
      <div class="flex justify-end items-center mb-6">
        <button
          class="gap-1 flex items-center cursor-pointer border border-green-600 text-green-600 px-2 py-1 rounded-lg hover:bg-green-50 transition"
          @click="$emit('add')"
        >
          <icon :name="'circle-add'" />
          <span>Add</span>
        </button>
      </div>
      <div class="h-auto overflow-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Expertise -->
          <div
            class="bg-white rounded-2xl p-4 border border-gray-200 transition-shadow duration-300"
          >
            <h2
              class="text-xl font-semibold text-gray-800 mb-4 border-b border-gray-200 pb-3"
            >
              My Expertise
            </h2>
            <ul class="flex flex-col gap-5">
              <li
                v-for="(item, idx) in user.expertise"
                :key="'expdb-' + idx"
                class="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center px-4 py-3 text-green-800 rounded-md"
              >
                <div class="flex items-center gap-3">
                  <!-- Green check circle -->
                  <span
                    class="flex items-center justify-center w-6 h-6 rounded-full bg-green-600 text-white text-xs font-bold border-2 border-spacing-1 border-green-500"
                  >
                    ✓
                  </span>

                  <!-- Course info -->
                  <div class="flex flex-col">
                    <span class="font-semibold text-sm">
                      {{ item.course?.course_code || "N/A" }}
                    </span>
                    <span class="text-xs text-gray-600">
                      {{ item.course?.course_description || "No Description" }}
                    </span>
                  </div>
                </div>
              </li>
            </ul>
            <p
              v-if="!user.expertise || user.expertise.length === 0"
              class="text-sm text-gray-400 mt-3 italic"
            >
              No expertise saved in database.
            </p>
          </div>

          <!-- Other Expertise -->
          <div
            class="bg-white rounded-2xl p-4 border border-gray-200 transition-shadow duration-300"
          >
            <h2
              class="text-xl font-semibold text-gray-800 mb-4 border-b border-gray-200 pb-3"
            >
              My Other Expertise
            </h2>
            <ul class="flex flex-col gap-3">
              <li
                v-for="(item, idx) in user.other_expertise"
                :key="'othdb-' + idx"
                class="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center px-4 py-3 text-blue-800 rounded-md"
              >
                <div class="flex items-center gap-5">
                  <!-- Blue check circle -->
                  <span
                    class="flex items-center justify-center w-6 h-6 rounded-full bg-blue-600 text-white text-xs font-bold border-2 border-spacing-1 border-blue-500"
                  >
                    ✓
                  </span>

                  <!-- Course info -->
                  <div class="flex flex-col">
                    <span class="font-semibold text-sm">
                      {{ item.course?.course_code || "N/A" }}
                    </span>
                    <span class="text-xs text-gray-600">
                      {{ item.course?.course_description || "No Description" }}
                    </span>
                  </div>
                </div>
              </li>
            </ul>

            <!-- Empty State -->
            <p
              v-if="!user.other_expertise || user.other_expertise.length === 0"
              class="text-sm text-gray-400 mt-3 italic"
            >
              No other expertise saved in database.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";

export default {
  name: "PreferenceSection",
  components: { icon },
  props: {
    user: { type: Object, required: true },
  },
};
</script>
