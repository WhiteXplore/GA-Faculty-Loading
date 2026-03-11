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
            <icon :name="'edit'" />
            <h1 class="font-bold tracking-wide text-lg">Edit Expertise</h1>
          </div>
          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div>

        <!-- Form Content -->
        <div class="p-5 w-[32vw] space-y-6">
          <!-- Semester Tabs -->
          <!-- Semester Dropdown -->
          <div class="w-full mx-auto space-y-1">
            <label class="font-bold text-sm">Select Semester:</label>
            <select
              v-model="selectedSemester"
              class="w-full border px-3 py-2.5 border-gray-600 rounded-md text-sm text-gray-800 focus:ring-2 focus:ring-defaultGreen outline-none"
            >
              <option v-for="sem in [1, 2, 3]" :key="sem" :value="sem">
                {{ getSemesterName(sem) }}
              </option>
            </select>
          </div>

          <!-- Semester View -->
          <transition name="fade" mode="out-in">
            <div
              v-if="selectedSemester"
              :key="selectedSemester"
              class="space-y-5"
            >
              <!-- Expertise -->
              <div class="relative space-y-2">
                <label class="font-bold"
                  >Field of Expertise ({{
                    getSemesterName(selectedSemester)
                  }}):</label
                >

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
                      currentSemesterData.expertise.some(
                        (c) => c.course_id === course.course_id
                      )
                        ? 'text-gray-400 cursor-not-allowed'
                        : 'text-gray-800 hover:bg-green-100',
                    ]"
                    @click="
                      !currentSemesterData.expertise.some(
                        (c) => c.course_id === course.course_id
                      ) && addCourse(course)
                    "
                  >
                    <span
                      >{{ course.course_code }} -
                      {{ course.course_title }}</span
                    >
                    <span
                      v-if="
                        currentSemesterData.expertise.some(
                          (c) => c.course_id === course.course_id
                        )
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
                  v-if="currentSemesterData.expertise.length"
                  class="mt-3 border border-gray-200 rounded-md divide-y shadow-sm"
                >
                  <div
                    v-for="(item, index) in currentSemesterData.expertise"
                    :key="index"
                    class="flex justify-between items-center px-3 py-3 bg-green-50 hover:bg-gray-100 transition cursor-pointer"
                  >
                    <span class="text-gray-700 text-sm font-medium">
                      {{ item.course_code }} - {{ item.course_title }}
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

              <!-- Non-specialized Subjects -->
              <div class="relative space-y-2">
                <label class="font-bold"
                  >Non-specialized Subjects ({{
                    getSemesterName(selectedSemester)
                  }}):</label
                >

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
                      currentSemesterData.other_expertise.some(
                        (c) => c.course_id === course.course_id
                      )
                        ? 'text-gray-400 cursor-not-allowed'
                        : 'text-gray-800 hover:bg-green-100 cursor-pointer',
                    ]"
                    @click="
                      !currentSemesterData.other_expertise.some(
                        (c) => c.course_id === course.course_id
                      ) && addOtherCourse(course)
                    "
                  >
                    <span
                      >{{ course.course_code }} -
                      {{ course.course_title }}</span
                    >
                    <span
                      v-if="
                        currentSemesterData.other_expertise.some(
                          (c) => c.course_id === course.course_id
                        )
                      "
                      class="text-xs text-red-500"
                    >
                      (Already Selected)
                    </span>
                  </li>
                </ul>

                <!-- Selected list -->
                <div
                  v-if="currentSemesterData.other_expertise.length"
                  class="mt-3 border border-gray-200 rounded-md divide-y shadow-sm"
                >
                  <div
                    v-for="(item, index) in currentSemesterData.other_expertise"
                    :key="index"
                    class="flex justify-between items-center px-3 py-3 bg-green-50 hover:bg-gray-100 transition cursor-pointer"
                  >
                    <span class="text-gray-700 text-sm font-medium">
                      {{ item.course_code }} - {{ item.course_title }}
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
            </div>
          </transition>

          <!-- Save -->
          <div class="flex justify-end pt-4">
            <button
              class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transition tracking-wider"
              type="submit"
            >
              Save Changes
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
  name: "EditExpertiseModal",
  components: { icon },
  props: {
    userData: { type: Object, required: true },
  },
  data() {
    return {
      form: {
        semesters: {
          1: { expertise: [], other_expertise: [] },
          2: { expertise: [], other_expertise: [] },
          3: { expertise: [], other_expertise: [] },
        },
      },
      selectedSemester: 1,
      searchQuery: "",
      dropdownOpen: false,
      otherSearchQuery: "",
      otherDropdownOpen: false,
      isLoadingCourses: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["courses"]),
    currentSemesterData() {
      return this.form.semesters[this.selectedSemester];
    },
    filteredCourses() {
      if (!this.courses?.length) return [];
      return this.courses.filter(
        (c) =>
          c.course_semester === this.selectedSemester &&
          c.curriculum?.program?.institute_id ===
            this.userData?.institute?.institute_id &&
          c.curriculum?.program_id === this.userData?.program?.program_id &&
          !this.currentSemesterData.other_expertise.some(
            (e) => e.course_id === c.course_id
          ) &&
          ((c.course_code?.toLowerCase() || "").includes(
            this.searchQuery.toLowerCase()
          ) ||
            (c.course_title?.toLowerCase() || "").includes(
              this.searchQuery.toLowerCase()
            ))
      );
    },
    filteredOtherCourses() {
      if (!this.courses?.length) return [];
      return this.courses.filter(
        (c) =>
          c.course_semester === this.selectedSemester &&
          c.curriculum?.program?.institute_id ===
            this.userData?.institute?.institute_id &&
          !this.currentSemesterData.expertise.some(
            (e) => e.course_id === c.course_id
          ) &&
          ((c.course_code?.toLowerCase() || "").includes(
            this.otherSearchQuery.toLowerCase()
          ) ||
            (c.course_title?.toLowerCase() || "").includes(
              this.otherSearchQuery.toLowerCase()
            ))
      );
    },
  },
  methods: {
    getSemesterName(sem) {
      if (sem === 1) return "1st Semester";
      if (sem === 2) return "2nd Semester";
      if (sem === 3) return "Summer";
      return "N/A";
    },
    addCourse(course) {
      this.currentSemesterData.expertise.push(course);
      this.searchQuery = "";
      this.dropdownOpen = false;
    },
    addOtherCourse(course) {
      this.currentSemesterData.other_expertise.push(course);
      this.otherSearchQuery = "";
      this.otherDropdownOpen = false;
    },
    removeCourse(index) {
      this.currentSemesterData.expertise.splice(index, 1);
    },
    removeOtherCourse(index) {
      this.currentSemesterData.other_expertise.splice(index, 1);
    },
    async submitExpertise() {
      try {
        const allExpertise = Object.values(this.form.semesters)
          .flatMap((s) => s.expertise)
          .map((c) => c.course_id);
        const allOther = Object.values(this.form.semesters)
          .flatMap((s) => s.other_expertise)
          .map((c) => c.course_id);

        const payload = { expertise: allExpertise, other_expertise: allOther };

        await axios.patch(
          process.env.VUE_APP_API_BASE_URL + `/auth/update/${this.userData.id}`,
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

    // ✅ FIXED METHOD
    loadExistingExpertise() {
      if (!this.courses.length) return;

      const mapCourse = (id) =>
        this.courses.find((c) => c.course_id === id) || null;

      // ✅ Load regular expertise
      this.userData.expertise?.forEach((ex) => {
        const courseData = ex.course || ex; // handle nested 'course'
        const matched = mapCourse(courseData.course_id);

        const courseObj = matched
          ? matched
          : {
              course_id: courseData.course_id,
              course_code: courseData.course_code,
              course_title: courseData.course_title,
              course_semester: courseData.course_semester || 1,
            };

        const sem = courseObj.course_semester || 1;
        this.form.semesters[sem].expertise.push(courseObj);
      });

      // ✅ Load "other expertise"
      this.userData.other_expertise?.forEach((ex) => {
        const courseData = ex.course || ex;
        const matched = mapCourse(courseData.course_id);

        const courseObj = matched
          ? matched
          : {
              course_id: courseData.course_id,
              course_code: courseData.course_code,
              course_title: courseData.course_title,
              course_semester: courseData.course_semester || 1,
            };

        const sem = courseObj.course_semester || 1;
        this.form.semesters[sem].other_expertise.push(courseObj);
      });
    },
  },
  async mounted() {
    await this.ensureCoursesLoaded();
    this.loadExistingExpertise();
  },
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
