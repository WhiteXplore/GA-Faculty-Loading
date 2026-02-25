<template>
  <div
    v-if="visible"
    class="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50 p-4"
  >
    <div
      class="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl h-[380px] overflow-hidden"
    >
      <!-- HEADER -->
      <div
        class="flex justify-between items-center px-6 py-4 bg-defaultGreen text-white"
      >
        <div class="flex items-center gap-3">
          <div
            class="w-9 h-9 flex items-center justify-center bg-white/20 rounded-full"
          >
            <!-- Link SVG Icon -->
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
              class="w-4 h-4 text-white"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M13.828 10.172a4 4 0 010 5.656l-3.536 3.536a4 4 0 01-5.656-5.656l1.415-1.414M10.172 13.828a4 4 0 010-5.656l3.536-3.536a4 4 0 015.656 5.656l-1.415 1.414"
              />
            </svg>
          </div>

          <div>
            <h3 class="text-base font-semibold">Join Class Schedules</h3>
            <p class="text-xs opacity-80">Merge multiple sections into one</p>
          </div>
        </div>

        <button
          @click="$emit('close')"
          class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/20 transition"
        >
          ✕
        </button>
      </div>

      <!-- BODY -->
      <div
        class="relative h-[250px] overflow-hidden flex items-center justify-center"
      >
        <!-- BASE CARD -->
        <div
          v-if="localBaseRecord"
          class="absolute transition-all duration-700 ease-in-out"
          :class="baseCardClass"
        >
          <div
            class="w-[270px] min-h-[180px] p-4 rounded-xl border border-green-200 flex flex-col justify-between"
          >
            <p class="text-[11px] font-semibold text-green-700 mb-1">
              Base Schedule
            </p>

            <div>
              <div class="font-semibold text-gray-800 text-sm">
                {{ localBaseRecord.course_code }}
              </div>

              <div class="text-xs text-gray-600 mt-1">
                {{ localBaseRecord.program_name }}-{{
                  localBaseRecord.set_name
                }}
              </div>

              <div class="text-xs text-gray-500 mt-1">
                {{ localBaseRecord.day }} |
                {{ formatTime(localBaseRecord.start_hour) }} –
                {{
                  formatTime(
                    localBaseRecord.start_hour + localBaseRecord.duration,
                  )
                }}
              </div>
            </div>

            <div
              class="text-[11px] bg-white px-3 py-1 rounded-full border self-start"
            >
              👥 {{ localBaseRecord.class_size }}
            </div>
          </div>
        </div>

        <!-- TARGET CARDS -->
        <div
          v-for="(t, index) in localTargets"
          :key="t.id"
          class="absolute transition-all duration-700 ease-in-out"
          :class="targetCardClass(index)"
        >
          <div
            class="w-[270px] min-h-[180px] p-4 rounded-xl border border-blue-200 flex flex-col justify-between"
          >
            <p class="text-[11px] font-semibold text-blue-700 mb-1">
              Target Schedule
            </p>

            <div>
              <div class="font-semibold text-gray-800 text-sm">
                {{ t.course_code }}
              </div>

              <div class="text-xs text-gray-600 mt-1">
                {{ t.program_name }}-{{ t.set_name }}
              </div>

              <div class="text-xs text-gray-500 mt-1">
                {{ t.day }} | {{ formatTime(t.start_hour) }} –
                {{ formatTime(t.start_hour + t.duration) }}
              </div>
            </div>

            <div
              class="text-[11px] bg-white px-3 py-1 rounded-full border self-start"
            >
              👥 {{ t.class_size }}
            </div>
          </div>
        </div>

        <!-- ARROW -->
        <div
          v-if="showArrow"
          class="absolute transition-all duration-500 flex flex-col"
          :class="arrowClass"
        >
          <div
            class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-100"
          >
            →
          </div>
          <span class="text-[10px] text-gray-400 mt-1">Joining</span>
        </div>

        <!-- SUCCESS OVERLAY -->
        <transition name="success-fade">
          <div
            v-if="showSuccess"
            class="absolute inset-0 flex flex-col items-center justify-center bg-white/70 backdrop-blur-md z-50"
          >
            <!-- Soft glow ring -->
            <div class="relative flex items-center justify-center">
              <!-- Outer Glow -->
              <div
                class="absolute w-32 h-32 rounded-full bg-green-500/20 blur-2xl"
              ></div>

              <!-- Main Circle -->
              <div
                class="relative w-24 h-24 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-[0_10px_40px_rgba(16,185,129,0.4)] success-scale"
              >
                <svg
                  class="w-10 h-10 text-white"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="3"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
            </div>

            <!-- Success Text -->
            <p class="mt-6 text-lg font-semibold text-gray-800 tracking-wide">
              Successfully Joined
            </p>
            <p class="text-sm text-gray-500 mt-1">
              Sections merged successfully
            </p>
          </div>
        </transition>
      </div>

      <!-- FOOTER -->
      <div class="absolute bottom-5 right-6 flex gap-3">
        <button
          @click="$emit('close')"
          class="px-4 py-2 rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-100 transition text-sm"
        >
          Cancel
        </button>

        <button
          @click="handleConfirm"
          :disabled="isMerging"
          class="px-5 py-2 rounded-lg text-white text-sm font-medium bg-green-600 hover:bg-green-700 shadow transition disabled:opacity-50"
        >
          Confirm Join
        </button>
      </div>
    </div>
  </div>
</template>

<script>
// import icon from "@/assets/icon.vue";

export default {
  name: "EditJoinValidation",
  components: {},
  props: {
    visible: Boolean,
    baseRecord: Object,
    targets: Array,
  },
  data() {
    return {
      localBaseRecord: null,
      localTargets: [],
      isMerging: false,
      showSuccess: false,
      showArrow: true,
    };
  },
  watch: {
    baseRecord: {
      immediate: true,
      handler(val) {
        this.localBaseRecord = val ? { ...val } : null;
      },
    },
    targets: {
      immediate: true,
      handler(val) {
        this.localTargets = val ? [...val] : [];
      },
    },
    visible(val) {
      if (!val) this.resetModal();
    },
  },
  computed: {
    baseCardClass() {
      return this.isMerging
        ? "left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 scale-75 opacity-70 z-20"
        : "left-8 top-1/2 -translate-y-1/2";
    },

    arrowClass() {
      return this.isMerging
        ? "left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 scale-150 opacity-0"
        : "left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2";
    },
  },
  methods: {
    targetCardClass(index) {
      if (this.isMerging) {
        return `left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 scale-75 opacity-70 z-${
          10 - index
        }`;
      }

      return `right-8 top-[${80 + index * 200}px]`;
    },

    formatTime(h) {
      if (h == null) return "";
      const hour = Math.floor(h);
      const minutes = Math.round((h - hour) * 60);
      const period = hour >= 12 ? "PM" : "AM";
      const hour12 = hour % 12 || 12;
      return `${hour12}:${minutes.toString().padStart(2, "0")} ${period}`;
    },

    handleConfirm() {
      this.showArrow = false;
      this.isMerging = true;

      setTimeout(() => {
        this.showSuccess = true;
      }, 700);

      setTimeout(() => {
        this.$emit("confirm");
        this.$emit("close");
        this.resetModal();
      }, 1700);
    },

    resetModal() {
      this.isMerging = false;
      this.showSuccess = false;
      this.showArrow = true;
    },
  },
};
</script>

<style scoped>
.success-fade-enter-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}

.success-fade-enter-from {
  opacity: 0;
  transform: scale(0.95);
}

.success-fade-enter-to {
  opacity: 1;
  transform: scale(1);
}

.success-scale {
  animation: scalePop 0.35s ease-out;
}

@keyframes scalePop {
  0% {
    transform: scale(0.7);
  }
  60% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes bounceIn {
  0% {
    transform: scale(0.6);
  }
  60% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.animate-bounceIn {
  animation: bounceIn 0.4s ease-out;
}
</style>
