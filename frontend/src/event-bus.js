import { reactive, watch } from "vue";

export const eventBus = reactive({
  schoolYearChanged: null,

  emit(payload) {
    this.schoolYearChanged = payload;
  },

  on(callback) {
    const stop = watch(
      () => this.schoolYearChanged,
      (newVal) => {
        if (newVal !== null) callback(newVal);
      }
    );
    return stop; // call stop() to unwatch
  },
});
