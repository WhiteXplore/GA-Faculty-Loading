<template>
  <div
    v-if="visible"
    class="fixed inset-0 flex items-center justify-center bg-black/30 z-50"
  >
    <div class="bg-white rounded-2xl shadow-2xl p-6 w-96">
      <!-- Header -->
      <div class="flex items-center justify-between border-b pb-3 mb-4">
        <div class="flex items-center gap-2">
          <icon
            name="exclamation-circle"
            class="w-7 h-7 p-1 rounded-full bg-orange-200 text-orange-900 flex items-center justify-center"
          />
          <h3 class="text-lg font-semibold text-gray-800 leading-none">
            Confirm Unjoin
          </h3>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition leading-none"
        >
          ✕
        </button>
      </div>

      <!-- Message -->
      <p class="text-gray-600 mb-6">
        Are you sure you want to unjoin this schedule group?
      </p>

      <!-- Buttons -->
      <div class="flex justify-center gap-2 text-sm">
        <button
          @click="$emit('close')"
          class="bg-gray-200 p-2 px-3 rounded-lg text-gray-700 hover:bg-white border hover:border-gray-800 hover:text-gray-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
        >
          Cancel
        </button>
        <button
          @click="$emit('confirm')"
          class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-defaultGreen hover:text-defaultGreen hover:shadow-md transform transition-all duration-300 hover:scale-105"
        >
          Yes, Unjoin
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";

export default {
  name: "UnjoinModal",
  components: { icon },
  props: {
    visible: { type: Boolean, default: false },
  },
};
</script>
