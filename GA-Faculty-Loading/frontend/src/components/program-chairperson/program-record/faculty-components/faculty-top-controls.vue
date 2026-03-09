<template>
  <div class="flex justify-between items-center">
    <!-- LEFT: JOIN TOGGLE -->
    <div
      class="flex items-center gap-4 py-2 px-3 ml-2 rounded-full border w-max bg-white text-sm"
    >
      <span class="font-medium text-gray-700">Join Scheduled:</span>

      <div class="flex items-center gap-2">
        <span
          class="font-semibold"
          :class="isJoined ? 'text-green-600' : 'text-gray-400'"
        >
          {{ isJoined ? "YES" : "NOT" }}
        </span>

        <button
          @click="$emit('update:isJoined', !isJoined)"
          :class="[
            'w-12 h-6 rounded-full p-1 flex items-center transition-colors duration-300 focus:outline-none',
            isJoined ? 'bg-green-500' : 'bg-gray-300',
          ]"
        >
          <span
            class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300"
            :class="isJoined ? 'translate-x-6' : 'translate-x-0'"
          ></span>
        </button>
      </div>
    </div>

    <!-- RIGHT SIDE -->
    <div class="flex items-center gap-3 flex-wrap mr-4">
      <!-- VIEW TOGGLE -->
      <div
        @click="$emit('toggleFacultyTable')"
        class="flex items-center gap-2 px-3 py-2 border bg-blue-700 text-white border-blue-700 rounded-xl hover:bg-white hover:text-blue-700 hover:shadow-lg cursor-pointer transition duration-200"
      >
        <div
          class="p-1 bg-blue-500 bg-opacity-20 rounded-full flex items-center justify-center"
        >
          <icon name="users" />
        </div>
        <span class="font-medium text-sm">
          {{ showFacultyTable ? "View Cards" : "View Faculty" }}
        </span>
      </div>

      <!-- COMPARE BUTTON -->
      <div
        v-show="!showCompareSelection"
        @click="$emit('toggleCompareSelection')"
        class="flex items-center gap-2 px-3 py-2 border text-defaultGreen border-defaultGreen rounded-xl hover:bg-defaultGreen hover:text-white hover:shadow-lg cursor-pointer transition duration-200"
      >
        <div
          class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
        >
          <icon name="faculty-loading1" />
        </div>
        <span class="font-medium text-sm">Compare</span>
      </div>

      <!-- COMPARE SECTION -->
      <div
        v-show="showCompareSelection"
        class="flex items-center gap-3 flex-wrap"
      >
        <div class="flex gap-2 items-center">
          <!-- Instructor A -->
          <select
            :value="compareInstructorA"
            @change="$emit('update:compareInstructorA', $event.target.value)"
            class="rounded-xl border border-defaultGreen px-2 py-2.5 text-sm text-defaultGreen shadow-sm"
          >
            <option value="">Select Instructor</option>
            <option
              v-for="instructor in instructorList"
              :key="'a-' + instructor"
              :value="instructor"
            >
              {{ instructor }}
            </option>
          </select>

          <!-- Instructor B -->
          <select
            :value="compareInstructorB"
            @change="$emit('update:compareInstructorB', $event.target.value)"
            class="rounded-xl border border-defaultGreen px-2 py-2.5 text-sm text-defaultGreen shadow-sm"
          >
            <option value="">Select Instructor</option>
            <option
              v-for="instructor in instructorList"
              :key="'b-' + instructor"
              :value="instructor"
            >
              {{ instructor }}
            </option>
          </select>

          <!-- COMPARE BUTTON -->
          <div
            @click="emitCompare"
            :class="[
              'flex items-center gap-2 px-3 py-2 border rounded-xl transition duration-200',
              canCompare
                ? 'text-defaultGreen border-defaultGreen hover:bg-defaultGreen hover:text-white hover:shadow-lg cursor-pointer'
                : 'text-gray-400 border-gray-300 cursor-not-allowed',
            ]"
          >
            <div
              class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
            >
              <icon name="faculty-loading1" />
            </div>
            <span class="font-medium text-sm">Compare</span>
          </div>
        </div>

        <!-- CLOSE -->
        <button
          @click="$emit('backFromCompare')"
          class="flex items-center gap-2 p-1 border border-gray-400 rounded-full shadow-sm hover:bg-gray-100 transition"
        >
          <icon name="circle-close" class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
export default {
  name: "FacultyTopControls",
  components: {
    icon,
  },
  props: {
    isJoined: Boolean,
    showFacultyTable: Boolean,
    showCompareSelection: Boolean,
    compareInstructorA: String,
    compareInstructorB: String,
    instructorList: Array,
  },
  computed: {
    canCompare() {
      return (
        this.compareInstructorA &&
        this.compareInstructorB &&
        this.compareInstructorA !== this.compareInstructorB
      );
    },
  },
  methods: {
    emitCompare() {
      if (this.canCompare) {
        this.$emit("compare");
      }
    },
  },
};
</script>
