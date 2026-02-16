<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="programsForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit" : "Add" }} Institute
            </h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <div class="p-5 w-[25vw] space-y-3">
          <!-- Institute Fields -->
          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="institute_code" class="font-bold"
              >Institute Code:</label
            >
            <input
              v-model="form.institute_code"
              type="text"
              id="institute_code"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="Enter institute code"
            />
          </div>
          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="institute_name" class="font-bold"
              >Institute Name:</label
            >
            <input
              v-model="form.institute_name"
              type="text"
              id="institute_name"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="Enter institute name"
            />
          </div>

          <!-- Program Fields -->
          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="program_code" class="font-bold">Program Code:</label>
            <input
              v-model="form.program_code"
              type="text"
              id="program_code"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="Enter program code"
            />
          </div>
          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="program_name" class="font-bold">Program Name:</label>
            <input
              v-model="form.program_name"
              type="text"
              id="program_name"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="Enter program name"
            />
          </div>

          <!-- Divider -->
          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <!-- Buttons -->
          <div class="tracking-wide flex justify-end gap-2 mt-4">
            <button
              class="bg-gray-200 p-2 px-3 rounded-lg text-gray-700 hover:bg-white border hover:border-gray-800 hover:text-gray-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
              type="submit"
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

export default {
  name: "AddInstitutePage",
  components: { icon },
  props: {
    editData: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      form: {
        institute_name: "",
        institute_code: "",
        program_code: "",
        program_name: "",
      },
    };
  },
  computed: {
    isEdit() {
      return !!this.editData;
    },
  },
  watch: {
    editData: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.form.institute_name = newVal.institute?.institute_name || "";
          this.form.institute_code = newVal.institute?.institute_code || "";
          this.form.program_name = newVal.program_name || "";
          this.form.program_code = newVal.program_code || "";
        }
      },
    },
  },

  methods: {
    async submitData() {
      const form = this.$refs.programsForm;
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      try {
        let instituteId;

        if (this.isEdit) {
          // Update Institute
          const instituteResponse = await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/institute/update-institute/${this.editData.institute_id}`,
            {
              institute_name: this.form.institute_name,
              institute_code: this.form.institute_code,
            },
          );
          instituteId = instituteResponse.data.institute_id;

          // Update Program
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/programs/update-program/${this.editData.program_id}`,
            {
              program_name: this.form.program_name,
              program_code: this.form.program_code,
              institute_id: instituteId,
            },
          );

          toast.success("Institute and Program updated successfully!");
        } else {
          // Add Institute
          const instituteResponse = await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/institute/add-institute",
            {
              institute_name: this.form.institute_name,
              institute_code: this.form.institute_code,
            },
          );
          instituteId = instituteResponse.data.institute_id;

          // Add Program
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/programs/add-programs",
            {
              program_name: this.form.program_name,
              program_code: this.form.program_code,
              institute_id: instituteId,
            },
          );

          toast.success("Institute and Program added successfully!");
        }

        const audio = new Audio(require("@/assets/add.mp3"));
        audio.play();

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error(error);
        toast.error("Failed to save institute or program.");
      }
    },
  },
  mounted() {
    if (this.isEdit && this.editData) {
      // populate form with editData
      this.form.institute_name = this.editData.institute?.institute_name || "";
      this.form.institute_code = this.editData.institute?.institute_code || "";
      this.form.program_name = this.editData.program_name || "";
      this.form.program_code = this.editData.program_code || "";
    }
  },
};
</script>
