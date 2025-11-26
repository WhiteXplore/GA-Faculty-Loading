<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="programForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit " : "Add " }} Program
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
          <!-- Institute -->
          <div class="flex flex-col space-y-2 w-full relative">
            <label class="font-bold">Institute :</label>
            <input
              v-model="searchInstituteQuery"
              type="text"
              placeholder="Search institute..."
              class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
              @focus="showInstituteDropdown = true"
            />
            <div
              v-if="showInstituteDropdown && filteredInstitutes.length"
              class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
              @mouseleave="showInstituteDropdown = false"
            >
              <div
                v-for="inst in filteredInstitutes"
                :key="inst.institute_id"
                class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                @mousedown="selectInstitute(inst)"
              >
                {{ inst.institute_name }}
              </div>
            </div>
          </div>

          <!-- Program Code -->
          <div class="w-full space-y-2">
            <label for="program_code" class="font-bold">Program Code:</label>
            <input
              v-model="form.program_code"
              type="text"
              id="program_code"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="e.g., BSCS, BSIT, BSBA"
            />
          </div>

          <!-- Program Name -->
          <div class="w-full space-y-2">
            <label for="program_name" class="font-bold">Program Name:</label>
            <input
              v-model="form.program_name"
              type="text"
              id="program_name"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="e.g., Bachelor of Science in Computer Science"
            />
          </div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2 mt-4">
            <button
              type="button"
              class="bg-gray-100 text-gray-600 p-2 px-3 rounded-lg hover:bg-white border hover:border-gray-800 hover:text-gray-800"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800"
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
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "ProgramFormModal",
  components: { icon },
  props: {
    programData: { type: Object, default: null },
  },
  data() {
    return {
      form: {
        institute_id: "",
        program_code: "",
        program_name: "",
      },
      searchInstituteQuery: "",
      showInstituteDropdown: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["institutes"]),
    isEdit() {
      return !!this.programData;
    },
    filteredInstitutes() {
      if (!this.searchInstituteQuery) return this.institutes;
      const q = this.searchInstituteQuery.toLowerCase();
      return this.institutes.filter((inst) =>
        inst.institute_name?.toLowerCase().includes(q)
      );
    },
  },
  methods: {
    ...mapActions(useFetchDataStore, ["fetchInstitutes"]),
    selectInstitute(inst) {
      this.form.institute_id = inst.institute_id;
      this.searchInstituteQuery = inst.institute_name;
      this.showInstituteDropdown = false;
    },

    async submitData() {
      try {
        const payload = { ...this.form };

        if (this.isEdit) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/programs/update-program/${this.programData.program_id}`,
            payload
          );
          toast.success("Program updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/programs/add-programs",
            payload
          );
          toast.success("Program added successfully!");
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
          this.isEdit ? "Failed to update program." : "Failed to add program."
        );
      }
    },
  },
  async mounted() {
    await this.fetchInstitutes();

    // if editing, fill the form
    if (this.isEdit) {
      this.form = {
        institute_id: this.programData.institute_id,
        program_code: this.programData.program_code,
        program_name: this.programData.program_name,
      };
      this.searchInstituteQuery =
        this.programData.institute?.institute_name || "";
    }
  },
};
</script>
