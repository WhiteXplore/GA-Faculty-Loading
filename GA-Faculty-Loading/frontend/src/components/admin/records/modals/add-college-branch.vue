<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="branchForm"
      >
        <!-- HEADER -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon name="circle-add" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEditMode ? "Edit College Branch" : "Add College Branch" }}
            </h1>
          </div>

          <icon
            name="circle-close3"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- FORM -->
        <div class="p-5 w-[28vw] space-y-4">
          <!-- BRANCH NAME -->
          <div>
            <label class="font-bold">College Branch Name:</label>
            <input
              v-model="form.college_branch_name"
              type="text"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md"
              placeholder="Enter college branch name"
            />
          </div>

          <!-- BUTTONS -->
          <div class="tracking-wide flex justify-end gap-2 pt-3">
            <button
              type="button"
              @click="$emit('close')"
              class="bg-gray-400 p-2 px-4 rounded-lg text-white hover:bg-white border hover:border-gray-600 hover:text-gray-700 hover:shadow-md"
            >
              Cancel
            </button>

            <button
              type="submit"
              class="bg-defaultGreen p-2 px-4 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
            >
              {{ isEditMode ? "Save Changes" : "Submit" }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import axios from "axios";
import { toast } from "vue3-toastify";

export default {
  name: "CollegeBranchModal",

  components: {
    icon,
  },

  props: {
    branchData: {
      type: Object,
      default: null,
    },
  },

  data() {
    return {
      form: {
        college_branch_id: null,
        college_branch_name: "",
      },
    };
  },

  computed: {
    isEditMode() {
      return !!this.branchData;
    },
  },

  methods: {
    async submitData() {
      const form = this.$refs.branchForm;

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      try {
        if (this.isEditMode) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/college-branch/${this.form.college_branch_id}`,
            {
              college_branch_name: this.form.college_branch_name,
            },
            { withCredentials: true },
          );

          toast.success("College branch updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL +
              "/college-branch/add-college-branch",
            {
              college_branch_name: this.form.college_branch_name,
            },
            { withCredentials: true },
          );

          toast.success("College branch created successfully!");
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        toast.error(
          error?.response?.data?.message || "Failed to save college branch",
        );
      }
    },
  },

  mounted() {
    if (this.isEditMode) {
      this.form = {
        ...this.form,
        ...this.branchData,
      };
    }
  },
};
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    transform: translateY(40px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slideUp {
  animation: fadeInUp 0.3s ease-out;
}
</style>
