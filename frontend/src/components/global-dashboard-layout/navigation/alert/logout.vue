<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50 w-screen"
  >
    <div
      class="rounded-xl shadow-lg w-[19vw] h-[28vh] bg-white py-6 px-4 flex flex-col items-center animate-slideUp"
    >
      <!-- Icon -->
      <div
        class="rounded-full w-16 h-16 md:w-20 md:h-20 flex justify-center items-center bg-red-300 animate-pulse"
      >
        <icon
          name="question"
          class="w-8 h-8 md:w-10 md:h-10 text-white flex justify-center items-center"
        />
      </div>

      <!-- Title -->
      <h1 class="text-[14px] md:text-[16px] font-semibold mt-4">
        Log out Confirmation
      </h1>
      <p class="mt-2 text-[12px] md:text-[13px]">
        Are you sure you want to log out ?
      </p>

      <!-- Break Line -->
      <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

      <!-- Buttons -->
      <div class="tracking-wide flex gap-2 mt-4">
        <button
          class="bg-gray-100 p-2 px-3 text-[11px] md:text-[13px] rounded-md text-gray-500 hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md"
          @click="closeModal"
        >
          No, Cancel
        </button>
        <button
          class="bg-defaultGreen p-2 px-3 text-[11px] md:text-[13px] rounded-md text-white hover:bg-white border hover:border-defaultGreen hover:text-defaultGreen hover:shadow-md"
          @click="toggleLogout"
        >
          Yes, Signout
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import axios from "axios";

export default {
  name: "LogoutModal",
  components: {
    icon,
  },
  props: {
    isOpen: Boolean,
  },
  methods: {
    async toggleLogout() {
      try {
        await axios.post(process.env.VUE_APP_API_BASE_URL + "/auth/logout");
        this.$emit("close"); // Inform parent to close the modal
        localStorage.removeItem("role");
        localStorage.removeItem("studentData");
        localStorage.removeItem("transactionData");
        localStorage.removeItem("lastStudentId");
        this.$router.push("/");
      } catch (error) {
        console.error("Logout failed:", error);
      }
    },
    closeModal() {
      this.$emit("close");
    },
  },
};
</script>
