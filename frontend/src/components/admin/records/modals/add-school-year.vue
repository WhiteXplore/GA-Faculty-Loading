<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit" : "Add" }} School Year
            </h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- Body -->
        <div class="p-5 w-[35vw] space-y-5">
          <!-- <div class="w-full space-y-2">
            <label>School Year Name:</label>
            <input
              :value="schoolYearName"
              type="text"
              readonly
              class="w-full border px-3 py-3 rounded-md bg-gray-100"
            />
          </div> -->

          <div class="w-full flex gap-3">
            <div class="w-full space-y-2">
              <label>Start Year:</label>
              <input
                v-model.number="form.start_year"
                type="number"
                required
                min="2000"
                max="2100"
                class="w-full border px-3 py-3"
                placeholder="e.g., 2024"
              />
            </div>
            <div class="w-full space-y-2">
              <label>End Year:</label>
              <input
                v-model.number="form.end_year"
                type="number"
                required
                min="2000"
                max="2100"
                class="w-full border px-3 py-3"
                placeholder="e.g., 2025"
              />
            </div>
          </div>

          <div class="w-full space-y-2">
            <label>Semester:</label>
            <select
              v-model.number="form.semester"
              required
              class="w-full border px-3 py-3"
            >
              <option value="">Select Semester</option>
              <option value="1">1st Semester</option>
              <option value="2">2nd Semester</option>
            </select>
          </div>

          <div class="w-full space-y-2">
            <label class="flex items-center gap-2">
              <input
                type="checkbox"
                v-model="form.is_active"
                class="w-4 h-4 text-defaultGreen border-gray-300 rounded focus:ring-green-500"
              />
              Set as Active School Year
            </label>
          </div>

          <div class="flex justify-end gap-2 mt-4">
            <button
              type="button"
              @click="$emit('close')"
              class="bg-red-600 p-2 px-3 rounded-lg text-white"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white"
            >
              {{ isEdit ? "Save Changes" : "Submit" }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import axios from "axios";
import { eventBus } from "@/bus/event-bus";

export default {
  name: "SchoolYearFormModal",
  components: { icon },
  props: { schoolYearData: { type: Object, default: null } },
  data() {
    return {
      form: {
        school_year_name: "",
        start_year: new Date().getFullYear(),
        end_year: new Date().getFullYear() + 1,
        semester: "",
        is_active: false,
      },
    };
  },
  computed: {
    isEdit() {
      return !!this.schoolYearData;
    },
    schoolYearName() {
      if (!this.form.start_year || !this.form.end_year) return "";
      return `${this.form.start_year}-${this.form.end_year}`;
    },
  },
  mounted() {
    if (this.isEdit) this.form = { ...this.schoolYearData };
  },
  methods: {
    async submitData() {
      try {
        if (this.form.end_year <= this.form.start_year) {
          toast.error("End year must be greater than start year");
          return;
        }

        const payload = { ...this.form, school_year_name: this.schoolYearName };
        if (this.isEdit) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/school-year/update-school-year/${this.schoolYearData.school_year_id}`,
            payload,
          );
          toast.success("School Year updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/school-year/add-school-year",
            payload,
          );
          toast.success("School Year added successfully!");
        }

        // inside submitData()
        if (this.form.is_active) {
          // Only emit if this is now the active school year
          eventBus.emit({
            school_year_id: this.form.school_year_id,
            isActive: true,
          });
        } else {
          eventBus.emit({
            school_year_id: this.form.school_year_id,
            isActive: false,
          });
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (err) {
        toast.error(
          this.isEdit
            ? "Failed to update school year."
            : "Failed to add school year.",
        );
      }
    },
  },
};
</script>
