import { reactive, watch } from "vue";
export const eventBus = reactive({
  value: null,

  emit(payload) {
    this.value = payload;
  },

  on(callback) {
    return watch(
      () => this.value,
      (newVal) => {
        if (newVal != null) callback(newVal);
      },
    );
  },
});
