// simple reactive event bus
import { reactive, watch } from "vue";

export const eventBus = reactive({
  schoolYearChanged: null,

  emit(event, payload) {
    if (event === "schoolYearChanged") {
      this.schoolYearChanged = payload;
    }
  },

  on(event, callback) {
    if (event === "schoolYearChanged") {
      const stop = watch(
        () => this.schoolYearChanged,
        (newVal) => {
          if (newVal !== null) callback(newVal);
        }
      );
      return stop; // call stop() to unwatch
    }
  },
});
