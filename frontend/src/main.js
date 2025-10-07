import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store"; // Vuex (if still used alongside Pinia)
import "./assets/tailwind.css";
import "@syncfusion/ej2-base/styles/material.css";
import "@syncfusion/ej2-vue-calendars/styles/material.css";

import { createPinia } from "pinia"; // ✅ Import Pinia

// ✅ Import vue3-toastify
import Vue3Toastify from "vue3-toastify";
import "vue3-toastify/dist/index.css";

// ✅ Import v-calendar and its styles
import VCalendar from "v-calendar";
import "v-calendar/dist/style.css";

const app = createApp(App);

const pinia = createPinia(); // ✅ Create Pinia instance

app
  .use(store) // Optional: if you're still using Vuex for other modules
  .use(router)
  .use(pinia) // ✅ Register Pinia
  .use(Vue3Toastify, {
    autoClose: 1000,
    position: "top-right",
    theme: "light",
  })
  .use(VCalendar, {})
  .mount("#app");
