<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitExpertise"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
      >
        <!-- Header -->
        <div
          class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center border-b shadow"
        >
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEditMode ? "Edit Expertise" : "Add Expertise" }}
            </h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- Form Content -->
        <div class="p-5 w-[30vw] space-y-6">
          <!-- Expertise -->
          <div class="relative space-y-2">
            <label class="font-bold">Expertise:</label>

            <!-- Searchable input -->
            <input
              v-model="searchQuery"
              @focus="dropdownOpen = true"
              type="text"
              placeholder="Search courses..."
              class="w-full border px-3 py-2.5 border-gray-600 rounded-md text-sm text-gray-800 focus:ring-2 focus:ring-defaultGreen outline-none"
            />

            <!-- Dropdown -->
            <ul
              v-if="dropdownOpen && filteredCourses.length"
              @mouseleave="dropdownOpen = false"
              class="animate-slideUp absolute z-50 w-full bg-white border border-gray-300 rounded-md mt-1 max-h-40 overflow-y-auto shadow-md"
            >
              <li
                v-for="course in filteredCourses"
                :key="course.course_id"
                :class="[
                  'px-3 py-2 text-sm flex justify-between items-center cursor-pointer transition',
                  form.expertise.some((c) => c.course_id === course.course_id)
                    ? 'text-gray-400 cursor-not-allowed'
                    : 'text-gray-800 hover:bg-green-100',
                ]"
                @click="
                  !form.expertise.some(
                    (c) => c.course_id === course.course_id
                  ) && addCourse(course)
                "
              >
                <span>
                  {{ course.course_code }} - {{ course.course_description }}
                </span>
                <span
                  v-if="
                    form.expertise.some((c) => c.course_id === course.course_id)
                  "
                  class="text-xs text-red-500"
                >
                  (Already selected)
                </span>
              </li>
            </ul>

            <!-- No results -->
            <div
              v-if="dropdownOpen && !filteredCourses.length && searchQuery"
              class="absolute z-50 w-full bg-white border border-gray-300 rounded-md mt-1 px-3 py-2 text-gray-500 text-sm"
            >
              No results found
            </div>

            <!-- Selected list -->
            <div
              v-if="form.expertise.length"
              class="mt-3 border border-gray-200 rounded-md divide-y shadow-sm"
            >
              <div
                v-for="(item, index) in form.expertise"
                :key="index"
                class="flex justify-between items-center px-3 py-3 bg-green-50 hover:bg-gray-100 transition cursor-pointer"
              >
                <span class="text-gray-700 text-sm font-medium">
                  {{ item.course_code }} - {{ item.course_description }}
                </span>
                <button
                  type="button"
                  @click="removeCourse(index)"
                  class="text-red-500 hover:text-red-700 hover:scale-125 duration-200 leading-none"
                >
                  <icon :name="'delete'" />
                </button>
              </div>
            </div>
          </div>

          <!-- Other Expertise -->
          <div class="relative space-y-2">
            <label class="font-bold">Other Expertise:</label>

            <!-- Searchable input -->
            <input
              v-model="otherSearchQuery"
              @focus="otherDropdownOpen = true"
              type="text"
              placeholder="Search other courses..."
              class="w-full border px-3 py-2.5 border-gray-600 rounded-md text-sm text-gray-800 focus:ring-2 focus:ring-defaultGreen outline-none"
            />

            <!-- Dropdown -->
            <ul
              v-if="otherDropdownOpen && filteredOtherCourses.length"
              @mouseleave="otherDropdownOpen = false"
              class="animate-slideUp absolute z-50 w-full bg-white border border-gray-300 rounded-md mt-1 max-h-40 overflow-y-auto shadow-md"
            >
              <li
                v-for="course in filteredOtherCourses"
                :key="course.course_id"
                :class="[
                  'px-3 py-2 text-sm flex justify-between items-center transition',
                  form.expertise.some((c) => c.course_id === course.course_id)
                    ? 'text-gray-400 cursor-not-allowed'
                    : 'text-gray-800 hover:bg-green-100 cursor-pointer',
                ]"
                @click="
                  !form.expertise.some(
                    (c) => c.course_id === course.course_id
                  ) && addOtherCourse(course)
                "
              >
                <span>
                  {{ course.course_code }} - {{ course.course_description }}
                </span>
                <span
                  v-if="
                    form.expertise.some((c) => c.course_id === course.course_id)
                  "
                  class="text-xs text-red-500"
                >
                  (Already in Expertise)
                </span>
              </li>
            </ul>

            <!-- Selected list -->
            <div
              v-if="form.other_expertise.length"
              class="mt-3 border border-gray-200 rounded-md divide-y shadow-sm"
            >
              <div
                v-for="(item, index) in form.other_expertise"
                :key="index"
                class="flex justify-between items-center px-3 py-3 bg-green-50 hover:bg-gray-100 transition cursor-pointer"
              >
                <span class="text-gray-700 text-sm font-medium">
                  {{ item.course_code }} - {{ item.course_description }}
                </span>
                <button
                  type="button"
                  @click="removeOtherCourse(index)"
                  class="text-red-500 hover:text-red-700 hover:scale-125 duration-200 leading-none"
                >
                  <icon :name="'delete'" />
                </button>
              </div>
            </div>
          </div>

          <!-- Submit -->
          <div class="flex justify-end pt-4">
            <button
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transition tracking-woder"
              type="submit"
            >
              {{ isEditMode ? "Save Changes" : "Save" }}
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
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";

export default {
  name: "AddExpertiseModal",
  components: { icon },
  props: {
    userData: { type: Object, required: true },
  },
  data() {
    return {
      form: {
        expertise: [],
        other_expertise: [],
      },
      searchQuery: "",
      dropdownOpen: false,
      otherSearchQuery: "",
      otherDropdownOpen: false,
      isLoadingCourses: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["courses"]),
    isEditMode() {
      return (
        this.userData?.expertise?.length > 0 ||
        this.userData?.other_expertise?.length > 0
      );
    },
    filteredCourses() {
      if (!this.courses?.length) return [];
      return this.courses.filter(
        (c) =>
          c.curriculum?.program?.institute_id ===
            this.userData?.institute?.institute_id &&
          c.curriculum?.program_id === this.userData?.program?.program_id &&
          (c.course_code
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase()) ||
            c.course_description
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase()))
      );
    },
    filteredOtherCourses() {
      if (!this.courses?.length) return [];
      return this.courses.filter(
        (c) =>
          c.curriculum?.program?.institute_id ===
            this.userData?.institute?.institute_id &&
          (c.course_code
            .toLowerCase()
            .includes(this.otherSearchQuery.toLowerCase()) ||
            c.course_description
              .toLowerCase()
              .includes(this.otherSearchQuery.toLowerCase()))
      );
    },
  },
  methods: {
    initializeForm() {
      if (this.userData?.expertise?.length) {
        this.form.expertise = this.userData.expertise.map((e) => ({
          course_id: e.course.course_id,
          course_code: e.course.course_code,
          course_description: e.course.course_description,
          course_credit: e.course.course_credit,
          course_lec: e.course.course_lec,
          course_lab: e.course.course_lab,
        }));
      }
      if (this.userData?.other_expertise?.length) {
        this.form.other_expertise = this.userData.other_expertise.map((e) => ({
          course_id: e.course.course_id,
          course_code: e.course.course_code,
          course_description: e.course.course_description,
          course_credit: e.course.course_credit,
          course_lec: e.course.course_lec,
          course_lab: e.course.course_lab,
        }));
      }
    },
    addCourse(course) {
      if (!this.form.expertise.some((c) => c.course_id === course.course_id)) {
        this.form.expertise.push({ ...course });
      }
      this.searchQuery = "";
      this.dropdownOpen = false;
    },
    removeCourse(index) {
      this.form.expertise.splice(index, 1);
    },
    addOtherCourse(course) {
      if (
        !this.form.other_expertise.some((c) => c.course_id === course.course_id)
      ) {
        this.form.other_expertise.push({ ...course });
      }
      this.otherSearchQuery = "";
      this.otherDropdownOpen = false;
    },
    removeOtherCourse(index) {
      this.form.other_expertise.splice(index, 1);
    },
    async submitExpertise() {
      try {
        const payload = {
          expertise: this.form.expertise.map((c) => c.course_id),
          other_expertise: this.form.other_expertise.map((c) => c.course_id),
        };
        await axios.patch(
          `http://localhost:8000/auth/update/${this.userData.id}`,
          payload,
          { withCredentials: true }
        );
        toast.success("Expertise updated successfully!");
        this.$emit("updated");

        this.$emit("close");
      } catch (error) {
        toast.error(
          error?.response?.data?.message || "Failed to update expertise"
        );
      }
    },
    async ensureCoursesLoaded() {
      const store = useFetchDataStore();
      if (!store.courses.length) {
        this.isLoadingCourses = true;
        await store.fetchCourses();
        this.isLoadingCourses = false;
      }
    },
  },
  watch: {
    userData: {
      immediate: true,
      handler() {
        this.initializeForm();
      },
    },
  },
  async mounted() {
    await this.ensureCoursesLoaded();
    this.initializeForm();
  },
};
</script>
