<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="specializationForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit " : "Add " }} Specialization
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
          <!-- Program -->
          <div class="flex flex-col space-y-2 w-full relative">
            <label class="font-bold">Program :</label>
            <input
              v-model="searchProgramQuery"
              type="text"
              placeholder="Search program..."
              class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
              @focus="showProgramDropdown = true"
            />
            <div
              v-if="showProgramDropdown && filteredPrograms.length"
              class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
              @mouseleave="showProgramDropdown = false"
            >
              <div
                v-for="prog in filteredPrograms"
                :key="prog.program_id"
                class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                @mousedown="selectProgram(prog)"
              >
                {{ prog.program_name }}
              </div>
            </div>
          </div>

          <!-- Specialization Name -->
          <div class="w-full space-y-2">
            <label for="specialization_name" class="font-bold"
              >Specialization Name:</label
            >
            <input
              v-model="form.specialization_name"
              type="text"
              id="specialization_name"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="e.g., Web Development"
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
  name: "SpecializationFormModal",
  components: { icon },
  props: {
    specializationData: { type: Object, default: null },
  },
  data() {
    return {
      form: {
        program_id: "",
        specialization_name: "",
      },
      searchProgramQuery: "",
      showProgramDropdown: false,
      user: null,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["programs"]),
    isEdit() {
      return !!this.specializationData;
    },
    filteredPrograms() {
      let result = this.programs;

      // Filter by user role
      if (this.user?.role === "Program Chairperson") {
        result = result.filter(
          (p) =>
            String(p.institute?.institute_id) ===
              String(this.user.institute_id) &&
            String(p.program_id) === String(this.user.program_id)
        );
      }

      if (!this.searchProgramQuery) return result;
      const q = this.searchProgramQuery.toLowerCase();
      return result.filter((p) => p.program_name?.toLowerCase().includes(q));
    },
  },
  methods: {
    ...mapActions(useFetchDataStore, ["fetchPrograms"]),
    async fetchUser() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          }
        );
        if (response.data) {
          this.user = response.data;
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
      }
    },
    selectProgram(prog) {
      this.form.program_id = prog.program_id;
      this.searchProgramQuery = prog.program_name;
      this.showProgramDropdown = false;
    },

    async submitData() {
      try {
        if (!this.form.program_id) {
          toast.error("Please select a program");
          return;
        }

        const payload = { ...this.form };

        if (this.isEdit) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/specialization/update-specialization/${this.specializationData.specialization_id}`,
            payload
          );
          toast.success("Specialization updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL +
              "/specialization/add-specialization",
            payload
          );
          toast.success("Specialization added successfully!");
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
            ? "Failed to update specialization."
            : "Failed to add specialization."
        );
      }
    },
  },
  async mounted() {
    await this.fetchUser();
    await this.fetchPrograms();

    // if editing, fill the form
    if (this.isEdit) {
      this.form = {
        program_id: this.specializationData.program_id,
        specialization_name: this.specializationData.specialization_name,
      };
      this.searchProgramQuery =
        this.specializationData.program?.program_name || "";
    }
  },
};
</script>
