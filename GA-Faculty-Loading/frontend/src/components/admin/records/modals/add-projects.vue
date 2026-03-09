<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="projectsForm"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">Add Projects</h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>
        <div class="p-5 w-[30vw] space-y-3">
          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="curriculum_id" class="font-bold">Curriculum:</label>
            <div>
              <select
                v-model="form.curriculum_id"
                required
                class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
              >
                <option disabled value="">Select Curriculum</option>
                <option
                  v-for="curriculum in curriculums"
                  :key="curriculum.curriculum_id"
                  :value="curriculum.curriculum_id"
                >
                  {{ curriculum.curriculum_name }}
                </option>
              </select>
            </div>
          </div>
          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="project_level" class="font-bold">Project Level:</label>
            <input
              v-model="form.project_level"
              type="text"
              id="project_level"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="Enter project level"
            />
          </div>

          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="project_section" class="font-bold"
              >Project Section:</label
            >
            <input
              v-model="form.project_section"
              type="text"
              id="project_section"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
              placeholder="Enter project section"
            />
          </div>

          <!-- Divider -->
          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <!-- Buttons -->
          <div class="tracking-wide flex justify-end gap-2 mt-4">
            <button
              class="bg-red-600 p-2 px-3 rounded-md text-white hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              class="bg-defaultGreen p-2 px-3 rounded-md text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
              type="submit"
            >
              Submit
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
import { useFetchDataStore } from "@/store/fetch-data-store"; // Adjust path if needed
import { mapState, mapActions } from "pinia";
export default {
  name: "AddProjectPage",
  components: {
    icon,
  },
  data() {
    return {
      form: {
        curriculum_id: "",
        project_level: "",
        project_section: "",
      },
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["curriculums"]),
  },
  methods: {
    ...mapActions(useFetchDataStore, ["fetchCurriculums"]),
    async submitData() {
      const form = this.$refs.projectsForm;
      if (!form.checkValidity()) {
        form.reportValidity(); // triggers browser validation messages
        return;
      }

      try {
        const response = await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/projected/add-projected",
          this.form
        );
        console.log(response.data);
        console.log("Submitting form:", this.form);
        toast.success("Projects added successfully!");
        // Play sound after successful delete
        const audio = new Audio(require("@/assets/add.mp3"));
        audio.play();

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        toast.error("Failed to add program.");
      }
    },
  },
  mounted() {
    this.fetchCurriculums();
  },
};
</script>
