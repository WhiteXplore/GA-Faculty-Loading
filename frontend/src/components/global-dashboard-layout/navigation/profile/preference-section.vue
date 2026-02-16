<template>
  <div
    v-if="user.role !== 'Admin'"
    class="w-full lg:flex-1 bg-white rounded-2xl"
  >
    <!-- Header / Add Button -->
    <div class="flex justify-end mb-2">
      <div
        class="gap-1 flex cursor-pointer border border-green-600 text-defaultGreen px-2 py-1 rounded-lg hover:bg-green-50 transition"
        @click="$emit('add')"
      >
        <icon :name="'edit'" />
        <button>Edit Expertise</button>
      </div>
    </div>

    <div class="h-auto overflow-auto space-y-8">
      <!-- Loop through semesters -->
      <div
        v-for="sem in [1, 2, 3]"
        :key="sem"
        class="bg-white border border-gray-200 rounded-xl p-4 transition-shadow duration-300"
      >
        <!-- Semester Header -->
        <h2
          class="text-xl font-bold text-green-800 mb-4 flex items-center gap-2"
        >
          <span>{{ getSemesterName(sem) }}</span>
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Expertise -->
          <div class="border rounded-xl p-4">
            <h3
              class="text-lg font-semibold text-green-900 mb-3 border-b border-green-300 pb-2"
            >
              Expertise
            </h3>

            <ul class="flex flex-col gap-4">
              <li
                v-for="(item, idx) in filteredExpertiseBySemester(sem)"
                :key="'exp-' + sem + '-' + idx"
                class="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center px-3 py-2 bg-white rounded-md"
              >
                <div class="flex items-center gap-3">
                  <span
                    class="flex items-center justify-center w-6 h-6 rounded-full bg-green-600 text-white text-xs font-bold"
                  >
                    ✓
                  </span>
                  <div class="flex flex-col">
                    <span class="font-semibold text-sm">
                      {{ item.course?.course_code || "N/A" }}
                    </span>
                    <span class="text-xs text-gray-600">
                      {{ item.course?.course_title || "No Description" }}
                    </span>
                  </div>
                </div>
              </li>
            </ul>

            <p
              v-if="filteredExpertiseBySemester(sem).length === 0"
              class="text-sm text-gray-400 mt-3 italic text-center"
            >
              No expertise for this semester.
            </p>
          </div>

          <!-- Other Expertise -->
          <div class="border rounded-xl p-4">
            <h3
              class="text-lg font-semibold text-blue-900 mb-3 border-b border-blue-300 pb-2"
            >
              Other Expertise
            </h3>

            <ul class="flex flex-col gap-4">
              <li
                v-for="(item, idx) in filteredOtherBySemester(sem)"
                :key="'oth-' + sem + '-' + idx"
                class="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center px-3 py-2 bg-white rounded-md"
              >
                <div class="flex items-center gap-3">
                  <span
                    class="flex items-center justify-center w-6 h-6 rounded-full bg-blue-600 text-white text-xs font-bold"
                  >
                    ✓
                  </span>
                  <div class="flex flex-col">
                    <span class="font-semibold text-sm">
                      {{ item.course?.course_code || "N/A" }}
                    </span>
                    <span class="text-xs text-gray-600">
                      {{ item.course?.course_title || "No Description" }}
                    </span>
                  </div>
                </div>
              </li>
            </ul>

            <p
              v-if="filteredOtherBySemester(sem).length === 0"
              class="text-sm text-gray-400 mt-3 italic text-center"
            >
              No other expertise for this semester.
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
  methods: {
    getSemesterName(sem) {
      if (sem === 1) return "1st Semester";
      if (sem === 2) return "2nd Semester";
      if (sem === 3) return "Summer";
      return "N/A";
    },
    filteredExpertiseBySemester(sem) {
      if (!this.user?.expertise) return [];
      return this.user.expertise.filter(
        (e) => e.course?.course_semester === sem,
      );
    },
    filteredOtherBySemester(sem) {
      if (!this.user?.other_expertise) return [];
      return this.user.other_expertise.filter(
        (e) => e.course?.course_semester === sem,
      );
    },
  },
};
</script>
