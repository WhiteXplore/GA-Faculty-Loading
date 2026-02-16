<template>
  <div
    class="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-100 to-gray-200"
  >
    <div
      class="bg-white shadow-lg rounded-2xl p-10 text-center max-w-md w-full"
    >
      <h1 class="text-7xl font-extrabold text-defaultGreen">404</h1>
      <p class="text-xl font-semibold text-gray-800 mt-4">Page Not Found</p>
      <p class="text-gray-500 mt-2">
        Oops! The page you’re looking for doesn’t exist or has been moved.
      </p>
      <router-link
        to="/"
        class="inline-block mt-6 px-6 py-3 bg-green-600 text-white font-medium rounded-xl shadow-md hover:bg-defaultGreen transition-all duration-300"
      >
        Return to Login
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "NotFoundPage",
};
</script>
