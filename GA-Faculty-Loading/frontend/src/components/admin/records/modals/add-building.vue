<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="buildingForm"
      >
        <!-- HEADER -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon name="circle-add" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEditMode ? "Edit Building" : "Add Building" }}
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
          <!-- BUILDING NAME -->
          <div>
            <label class="font-bold">Building Name:</label>
            <input
              v-model="form.building_name"
              type="text"
              required
              class="w-full border px-3 py-3 border-gray-600 rounded-md"
              placeholder="Enter building name"
            />
          </div>

          <!-- BUILDING AREA -->
          <div class="flex flex-col space-y-2 w-full relative">
            <label class="font-bold">Building Area :</label>

            <input
              v-model="searchAreaQuery"
              type="text"
              placeholder="Search building area..."
              class="px-3 py-3 border border-gray-600 rounded-md"
              @focus="showAreaDropdown = true"
            />

            <div
              v-if="showAreaDropdown && filteredAreas.length"
              class="absolute top-[75px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
              @mouseleave="showAreaDropdown = false"
            >
              <div
                v-for="area in filteredAreas"
                :key="area.building_area_id"
                class="px-3 py-3 hover:bg-gray-100 cursor-pointer"
                @mousedown="selectArea(area)"
              >
                {{ area.area_name }} -
                {{ area?.collegeBranch?.college_branch_name }}
              </div>
            </div>
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
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "BuildingModal",

  components: { icon },

  props: {
    buildingData: {
      type: Object,
      default: null,
    },
  },

  data() {
    return {
      form: {
        building_id: null,
        building_name: "",
        building_area_id: "",
      },

      searchAreaQuery: "",
      showAreaDropdown: false,
    };
  },

  computed: {
    isEditMode() {
      return !!this.buildingData;
    },

    ...mapState(useFetchDataStore, ["building_areas"]),

    filteredAreas() {
      const query = this.searchAreaQuery?.toLowerCase() || "";

      return this.building_areas
        .filter((a) => a.area_name.toLowerCase().includes(query))
        .sort((a, b) => a.area_name.localeCompare(b.area_name));
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchBuildingAreas"]),

    selectArea(area) {
      this.form.building_area_id = area.building_area_id;

      // what appears in the input
      this.searchAreaQuery =
        area.area_name + " - " + area?.collegeBranch?.college_branch_name;

      this.showAreaDropdown = false;
    },

    async submitData() {
      const form = this.$refs.buildingForm;

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      try {
        const payload = {
          building_name: this.form.building_name,
          building_area_id: Number(this.form.building_area_id),
        };

        if (this.isEditMode) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/buildings/${this.form.building_id}`,
            payload,
            { withCredentials: true },
          );

          toast.success("Building updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/buildings",
            payload,
            { withCredentials: true },
          );

          toast.success("Building created successfully!");
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        toast.error(
          error?.response?.data?.message || "Failed to save building",
        );
      }
    },
  },

  mounted() {
    this.fetchBuildingAreas();

    if (this.isEditMode) {
      this.form = {
        ...this.form,
        ...this.buildingData,
      };

      this.searchAreaQuery =
        this.buildingData?.buildingArea?.area_name +
          " - " +
          this.buildingData?.buildingArea?.collegeBranch?.college_branch_name ||
        "";
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
