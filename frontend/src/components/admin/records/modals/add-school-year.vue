<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="schoolYearForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit " : "Add " }} School Year
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
          <!-- School Year Name -->
          <div class="w-full space-y-2">
            <label for="school_year_name" class="font-bold"
              >School Year Name:</label
            >
            <input
              v-model="form.school_year_name"
              type="text"
              id="school_year_name"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="e.g., 2024-2025"
            />
          </div>

          <!-- Start Year + End Year -->
          <div class="w-full flex gap-3">
            <div class="w-full space-y-2">
              <label class="font-bold">Start Year:</label>
              <input
                v-model.number="form.start_year"
                type="number"
                required
                min="2000"
                max="2100"
                class="w-full border px-3 py-3 border-gray-600 rounded-md"
                placeholder="e.g., 2024"
              />
            </div>
            <div class="w-full space-y-2">
              <label class="font-bold">End Year:</label>
              <input
                v-model.number="form.end_year"
                type="number"
                required
                min="2000"
                max="2100"
                class="w-full border px-3 py-3 border-gray-600 rounded-md"
                placeholder="e.g., 2025"
              />
            </div>
          </div>

          <!-- Semester -->
          <div class="w-full space-y-2">
            <label class="font-bold">Semester:</label>
            <select
              v-model.number="form.semester"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
            >
              <option value="">Select Semester</option>
              <option value="1">1st Semester</option>
              <option value="2">2nd Semester</option>
            </select>
          </div>

          <!-- Active Status -->
          <div class="w-full space-y-2">
            <label class="font-bold flex items-center gap-2">
              <input
                v-model="form.is_active"
                type="checkbox"
                class="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
              />
              Set as Active School Year
            </label>
          </div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2 mt-4">
            <button
              type="button"
              class="bg-red-600 p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-red-800 hover:text-red-800"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800"
              type="submit"
            >
              {{ isEdit ? "Update" : "Submit" }}
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

export default {
  name: "SchoolYearFormModal",
  components: { icon },
  props: {
    schoolYearData: { type: Object, default: null },
  },
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
  },
  methods: {
    async submitData() {
      try {
        // Validation
        if (this.form.end_year <= this.form.start_year) {
          toast.error("End year must be greater than start year");
          return;
        }

        const payload = { ...this.form };

        if (this.isEdit) {
          await axios.patch(
            `http://localhost:8000/school-year/update-school-year/${this.schoolYearData.school_year_id}`,
            payload
          );
          toast.success("School Year updated successfully!");
        } else {
          await axios.post(
            "http://localhost:8000/school-year/add-school-year",
            payload
          );
          toast.success("School Year added successfully!");
        }

        this.$emit("refresh");
        this.$emit("close");

        // Play audio, but handle errors separately
        try {
          const audio = new Audio(
            require(`@/assets/${this.isEdit ? "update.mp3" : "add.mp3"}`)
          );
          await audio.play();
        } catch (audioErr) {
          console.warn("Audio failed to play:", audioErr);
        }
      } catch (err) {
        console.error(err);
        toast.error(
          this.isEdit
            ? "Failed to update school year."
            : "Failed to add school year."
        );
      }
    },
  },
  mounted() {
    // if editing, fill the form
    if (this.isEdit) {
      this.form = {
        school_year_name: this.schoolYearData.school_year_name,
        start_year: this.schoolYearData.start_year,
        end_year: this.schoolYearData.end_year,
        semester: this.schoolYearData.semester,
        is_active: this.schoolYearData.is_active,
      };
    }
  },
};
</script>

