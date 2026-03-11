<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
        ref="roomsForm"
      >
        <!-- HEADER -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEditMode ? "Edit " : "Add " }}Room
            </h1>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- BODY -->
        <div class="p-5 w-[27vw]">
          <div class="w-full text-left gap-3 flex flex-col space-y-1">
            <!-- Room Name -->
            <div class="w-full space-y-2">
              <label class="font-bold">Room Name:</label>

              <input
                v-model="form.room_name"
                type="text"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                placeholder="Enter room name"
              />
            </div>

            <!-- Room Type -->
            <div class="w-full space-y-2">
              <label class="font-bold">Room Type:</label>

              <select
                v-model="form.room_type"
                required
                class="w-full border px-2 py-3 border-gray-600 rounded-md text-md text-gray-800"
              >
                <option disabled value="">Select Room Type</option>
                <option value="Lecture">Lecture</option>
                <option value="Laboratory">Laboratory</option>
              </select>
            </div>

            <!-- Room Capacity -->
            <div class="w-full space-y-2">
              <label class="font-bold">Room Capacity:</label>

              <input
                v-model="form.room_capacity"
                type="number"
                required
                class="w-full border px-3 py-3 border-gray-600 rounded-md text-md text-gray-800"
                placeholder="Enter room capacity"
              />
            </div>
            <!-- Institute -->
            <div class="flex flex-col space-y-2 w-full relative">
              <label class="font-bold">Institute :</label>

              <input
                v-model="searchInstituteQuery"
                type="text"
                placeholder="Search institute..."
                class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
                @focus="showInstituteDropdown = true"
                :disabled="form.room_type === 'Lecture'"
              />

              <div
                v-if="showInstituteDropdown && filteredInstitutes.length"
                class="absolute top-[60px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
                @mouseleave="showInstituteDropdown = false"
              >
                <div
                  v-for="institute in filteredInstitutes"
                  :key="institute.institute_id"
                  class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                  @mousedown="selectInstitute(institute)"
                >
                  {{ institute.institute_code }} -
                  {{ institute.institute_name }}
                </div>
              </div>
            </div>

            <!-- Building -->
            <div class="flex flex-col space-y-2 w-full relative">
              <label class="font-bold">Building :</label>

              <input
                v-model="searchBuildingQuery"
                type="text"
                placeholder="Search building..."
                class="px-3 py-3 border w-full border-gray-600 rounded-md text-md text-gray-800"
                @focus="showBuildingDropdown = true"
              />

              <div
                v-if="showBuildingDropdown && filteredBuildings.length"
                class="absolute top-[60px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
                @mouseleave="showBuildingDropdown = false"
              >
                <div
                  v-for="building in filteredBuildings"
                  :key="building.building_id"
                  class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                  @mousedown="selectBuilding(building)"
                >
                  {{
                    building.buildingArea?.collegeBranch?.college_branch_name
                  }}
                  -
                  {{ building.buildingArea?.area_name }}
                  -
                  {{ building.building_name }}
                </div>
              </div>
            </div>
          </div>

          <!-- Divider -->
          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <!-- Buttons -->
          <div class="tracking-wide flex justify-end gap-2 mt-4">
            <button
              type="button"
              class="bg-gray-200 p-2 px-3 rounded-lg text-gray-700 hover:bg-white border hover:border-gray-800 hover:text-gray-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
              @click="$emit('close')"
            >
              Cancel
            </button>

            <button
              type="submit"
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
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
import { toast } from "vue3-toastify";
import axios from "axios";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "RoomFormModal",

  props: {
    roomData: {
      type: Object,
      default: null,
    },
  },

  components: { icon },
  watch: {
    "form.room_type"(newType) {
      if (newType === "Lecture") {
        this.form.institute_id = null;
        this.searchInstituteQuery = "";
      }

      if (newType === "Laboratory") {
        this.form.building_id = null;
        this.searchBuildingQuery = "";
      }
    },
  },
  computed: {
    ...mapState(useFetchDataStore, ["institutes", "buildings"]),

    filteredInstitutes() {
      if (!this.searchInstituteQuery) return this.institutes;

      return this.institutes.filter((institute) =>
        institute.institute_name
          .toLowerCase()
          .includes(this.searchInstituteQuery.toLowerCase()),
      );
    },

    filteredBuildings() {
      let filtered = this.buildings;

      if (this.searchBuildingQuery) {
        filtered = filtered.filter((building) =>
          building.building_name
            .toLowerCase()
            .includes(this.searchBuildingQuery.toLowerCase()),
        );
      }

      // Sort by Area number (Area 1 → Area 7)
      return filtered.sort((a, b) => {
        const areaA =
          parseInt(a.buildingArea?.area_name?.replace("Area ", "")) || 0;
        const areaB =
          parseInt(b.buildingArea?.area_name?.replace("Area ", "")) || 0;

        return areaA - areaB;
      });
    },
    isEditMode() {
      return !!this.roomData;
    },
  },

  data() {
    return {
      form: {
        institute_id: "",
        building_id: "",
        room_name: "",
        room_type: "",
        room_capacity: "",
      },

      searchInstituteQuery: "",
      showInstituteDropdown: false,

      searchBuildingQuery: "",
      showBuildingDropdown: false,
    };
  },
  methods: {
    ...mapActions(useFetchDataStore, ["fetchInstitutes", "fetchBuildings"]),

    selectInstitute(institute) {
      this.form.institute_id = institute.institute_id;
      this.searchInstituteQuery = institute.institute_name;
      this.showInstituteDropdown = false;
    },
    selectBuilding(building) {
      this.form.building_id = building.building_id;

      this.searchBuildingQuery =
        building.buildingArea?.collegeBranch?.college_branch_name +
        " - " +
        building.buildingArea?.area_name +
        " - " +
        building.building_name;

      this.showBuildingDropdown = false;
    },

    async submitData() {
      const form = this.$refs.roomsForm;

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      try {
        const payload = {
          ...this.form,
          room_capacity: Number(this.form.room_capacity),
          institute_id: this.form.institute_id
            ? Number(this.form.institute_id)
            : null,
          building_id: this.form.building_id
            ? Number(this.form.building_id)
            : null,
        };

        if (this.isEditMode) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/rooms/update-room/${this.roomData.room_id}`,
            payload,
          );

          toast.success("Room updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/rooms/add-rooms",
            payload,
          );

          toast.success("Room added successfully!");
        }

        const audio = new Audio(require("@/assets/add.mp3"));
        audio.play();

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        toast.error(
          this.isEditMode ? "Failed to update room" : "Failed to add room",
        );
      }
    },
  },

  mounted() {
    this.fetchInstitutes();
    this.fetchBuildings();

    if (this.isEditMode) {
      this.form = {
        institute_id: this.roomData.institute?.institute_id || "",
        building_id: this.roomData.building?.building_id || "",
        room_name: this.roomData.room_name,
        room_type: this.roomData.room_type,
        room_capacity: this.roomData.room_capacity,
      };

      this.searchInstituteQuery = this.roomData.institute?.institute_name || "";
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
