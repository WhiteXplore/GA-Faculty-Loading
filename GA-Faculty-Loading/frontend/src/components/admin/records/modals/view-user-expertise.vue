<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div
      class="rounded-[16px] shadow-lg justify-center animate-slideUp max-h-[90vh] overflow-y-auto"
    >
      <div class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5">
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-purple-600 text-white rounded-t-[16px] flex justify-between items-center border-b shadow sticky top-0 z-10"
        >
          <div class="flex gap-2 items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
            <h1 class="font-bold tracking-wide text-lg">Faculty Expertise</h1>
          </div>
          <button
            @click="$emit('close')"
            class="text-white hover:text-gray-200 cursor-pointer transition"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <!-- Content -->
        <div class="p-6 w-[50vw] space-y-6">
          <!-- Faculty Information Card -->
          <div
            class="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-5 border border-purple-200"
          >
            <div class="flex items-start justify-between mb-4">
              <div>
                <h2 class="text-2xl font-bold text-purple-900">
                  {{ userData.first_name }} {{ userData.last_name }}
                </h2>
                <p class="text-purple-700 font-medium">
                  {{ userData.role }}
                </p>
              </div>
              <div
                class="px-3 py-1 bg-purple-600 text-white rounded-full text-sm font-semibold"
              >
                Faculty Member
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4 mt-4">
              <div>
                <p class="text-gray-600 text-sm font-semibold mb-1">Email</p>
                <p class="text-gray-800 font-medium">{{ userData.email }}</p>
              </div>
              <div>
                <p class="text-gray-600 text-sm font-semibold mb-1">
                  Institute
                </p>
                <p class="text-gray-800 font-medium">
                  {{ userData.institute?.institute_name || "N/A" }}
                </p>
              </div>
              <div>
                <p class="text-gray-600 text-sm font-semibold mb-1">Program</p>
                <p class="text-gray-800 font-medium">
                  {{ userData.program?.program_name || "N/A" }}
                </p>
              </div>
              <div>
                <p class="text-gray-600 text-sm font-semibold mb-1">
                  Program Code
                </p>
                <p class="text-gray-800 font-medium">
                  {{ userData.program?.program_code || "N/A" }}
                </p>
              </div>
            </div>
          </div>

          <!-- Expertise Section -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3
                class="text-lg font-bold text-gray-800 flex items-center gap-2"
              >
                <span
                  class="px-2 py-1 bg-purple-100 text-purple-800 rounded text-sm"
                  >PRIMARY EXPERTISE</span
                >
                Courses Faculty Can Teach
              </h3>
              <span class="text-sm text-gray-600 font-semibold">
                {{ expertiseCount }} course{{ expertiseCount !== 1 ? "s" : "" }}
              </span>
            </div>

            <div
              v-if="userData.expertise && userData.expertise.length > 0"
              class="grid grid-cols-1 gap-3"
            >
              <div
                v-for="exp in userData.expertise"
                :key="exp.id"
                class="flex items-center justify-between p-4 bg-white border border-purple-200 rounded-lg hover:shadow-md transition-all"
              >
                <div class="flex items-center gap-3">
                  <div
                    class="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5 text-purple-600"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                      />
                    </svg>
                  </div>
                  <div>
                    <p class="font-bold text-purple-900">
                      {{ exp.course?.course_code || "N/A" }}
                    </p>
                    <p class="text-sm text-gray-600">
                      {{ exp.course?.course_title || "No description" }}
                    </p>
                  </div>
                </div>
                <div class="flex flex-col items-end gap-1">
                  <span
                    class="px-2 py-1 bg-purple-50 text-purple-700 rounded text-sm font-semibold"
                  >
                    Semester {{ exp.course?.course_semester || "N/A" }}
                  </span>
                  <span class="text-sm text-gray-500">
                    Level {{ exp.course?.course_level || "N/A" }}
                  </span>
                </div>
              </div>
            </div>

            <div
              v-else
              class="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-16 w-16 mx-auto text-gray-400 mb-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
              <p class="text-gray-500 font-medium">
                No course expertise assigned
              </p>
              <p class="text-gray-400 text-sm mt-1">
                This faculty member hasn't been assigned any courses yet
              </p>
            </div>
          </div>

          <!-- Other Expertise Section -->
          <div
            v-if="
              userData.other_expertise && userData.other_expertise.length > 0
            "
            class="space-y-4"
          >
            <div class="flex items-center justify-between">
              <h3
                class="text-lg font-bold text-gray-800 flex items-center gap-2"
              >
                <span
                  class="px-2 py-1 bg-indigo-100 text-indigo-800 rounded text-sm"
                  >OTHER EXPERTISE</span
                >
                Additional Courses
              </h3>
              <span class="text-sm text-gray-600 font-semibold">
                {{ otherExpertiseCount }} course{{
                  otherExpertiseCount !== 1 ? "s" : ""
                }}
              </span>
            </div>

            <div class="grid grid-cols-1 gap-3">
              <div
                v-for="exp in userData.other_expertise"
                :key="exp.id"
                class="flex items-center justify-between p-4 bg-white border border-indigo-200 rounded-lg hover:shadow-md transition-all"
              >
                <div class="flex items-center gap-3">
                  <div
                    class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5 text-indigo-600"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                      />
                    </svg>
                  </div>
                  <div>
                    <p class="font-bold text-indigo-900">
                      {{ exp.course?.course_code || "N/A" }}
                    </p>
                    <p class="text-sm text-gray-600">
                      {{ exp.course?.course_title || "No description" }}
                    </p>
                  </div>
                </div>
                <div class="flex flex-col items-end gap-1">
                  <span
                    class="px-2 py-1 bg-indigo-50 text-indigo-700 rounded text-sm font-semibold"
                  >
                    Semester {{ exp.course?.course_semester || "N/A" }}
                  </span>
                  <span class="text-sm text-gray-500">
                    Level {{ exp.course?.course_level || "N/A" }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-end gap-3 pt-4 border-t">
            <button
              type="button"
              @click="$emit('close')"
              class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition duration-200 font-medium"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ViewUserExpertise",
  props: {
    userData: {
      type: Object,
      required: true,
    },
  },
  computed: {
    expertiseCount() {
      return this.userData.expertise ? this.userData.expertise.length : 0;
    },
    otherExpertiseCount() {
      return this.userData.other_expertise
        ? this.userData.other_expertise.length
        : 0;
    },
  },
};
</script>

<style scoped>
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #9333ea;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #7e22ce;
}
</style>
