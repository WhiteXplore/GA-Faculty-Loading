<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black/30 z-50">
    <div class="bg-white rounded-2xl shadow-2xl p-6 w-96 text-center">
      <h2 class="text-lg font-semibold mb-4">Confirm Save</h2>
      <p class="text-gray-600 mb-6">
        Are you sure you want to save this schedule?
      </p>
      <div class="flex justify-center gap-4">
        <button
          @click="$emit('confirm')"
          class="px-4 py-2 bg-defaultGreen text-white rounded-xl hover:bg-green-600 transition"
        >
          Yes, Save
        </button>
        <button
          @click="$emit('cancel')"
          class="px-4 py-2 border rounded-xl hover:bg-gray-100 transition"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfirmSaveModal",
};
</script>
