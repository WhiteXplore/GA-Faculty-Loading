<template>
  <div class="relative w-full min-h-screen flex flex-col">
    <!-- Background Image -->
    <img
      src="@/assets/img/landing-layer-1.png"
      alt="Background"
      class="absolute inset-0 object-cover w-full h-full z-0 opacity-95"
    /><img
      src="@/assets/img/landing-layer 2.png"
      alt="Background"
      class="absolute inset-0 object-cover w-full h-full z-30 opacity-95"
    />
    <div class="flex justify-center items-center w-full min-h-screen relative">
      <!-- Main content container -->
      <div
        class="flex justify-between items-center w-[90vw] h-[200px] px-20 relative z-50"
      >
        <!-- Text on the left -->
        <div class="space-y-20 mb-20 font-poppins">
          <div
            class="text-white tracking-wide text-5xl font-extrabold flex flex-col justify-center space-y-3"
          >
            <h1>FACULTY LOADING</h1>
            <h1>AND <span class="text-[#FFE600]"> EXAM SCHEDULER</span></h1>
            <div class="text-xl italic">
              Automated Scheduling for Smarter Academic Management
            </div>
          </div>

          <router-link
            to="/login"
            class="text-md bg-white tracking-wide rounded-full text-[#147452] px-4 py-2.5 font-bold inline-block text-center hover:bg-[#147452] hover:text-white transition-colors duration-300"
          >
            Get Started
          </router-link>
        </div>
      </div>

      <!-- Background layer image (at the end, z-0) -->
      <!-- Logo Container -->
      <div class="relative flex justify-center items-center w-full">
        <!-- Background layer logo -->
        <img
          src="@/assets/img/landing-logo-layer-1.png"
          alt="Layer 1 Background"
          class="absolute w-[60%] max-w-[600px] h-auto object-contain animate-spinSlow"
        />

        <!-- Main logo -->
        <img
          src="@/assets/img/landing-logo.png"
          alt="Logo"
          class="relative w-[40%] max-w-[450px] h-auto z-50"
        />
      </div>
    </div>

    <div
      class="bg-gray-900 opacity-25 w-full min-h-screen z-10 absolute inset-0"
    ></div>
  </div>
</template>

<script>
import authMixin from "../../mixin/authMixin";
export default {
  name: "LandingPage",
  mixins: [authMixin],

  data() {
    return {
      showLogin: true,
      registrationStep: 1,
    };
  },
  methods: {
    toggleForm() {
      this.showLogin = !this.showLogin;
      this.registrationStep = 1;
      this.errorMessage = "";
    },
  },
};
</script>

<style scoped></style>
