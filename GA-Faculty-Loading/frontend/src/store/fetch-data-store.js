// src/stores/fetch-data-store.js
import { defineStore } from "pinia";
import axios from "axios";

export const useFetchDataStore = defineStore("fetchData", {
  state: () => ({
    instructors: [],
    courses: [],
    curriculums: [],
    programs: [],
    sections: [],
    rooms: [],
    time: [],
    projects: [],
    schedulers: [],
    bachelors: [],
    masters: [],
    doctorates: [],
    institutes: [],
    detailedReportCurriculum: [],
    calendarEvents: [],
    users: [],
    rawusers: [],
    assignClass: [],
    faculty: [],
    final_schedules: [],
    class_sections: [],
    unscheduled_meetings: [],
    college_branch: [],
    faculty_branch: [],
    buildings: [],
    building_areas: [],
    year: null, // currently selected year
    activeYears: [],
    activeYear: null, // latest active year for table filtering
    lastUpdatedAt: null,
    loading: false,
    error: null,
    activeYearInterval: null, // for polling
  }),

  actions: {
    async fetchBuildingAreas() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/building-areas/get-all-building-areas",
        );
        this.building_areas = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch building_areas";
      } finally {
        this.loading = false;
      }
    },

    async fetchBuildings() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/buildings/get-all-buildings",
        );
        this.buildings = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch buildings";
      } finally {
        this.loading = false;
      }
    },

    async fetchFacultyBranch() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/faculty-branch/get-all-faculty-branch",
        );
        this.faculty_branch = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch faculty_branch";
      } finally {
        this.loading = false;
      }
    },

    async fetchCollegeBranch() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/college-branch/get-college-branch",
        );
        this.college_branch = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch college_branch";
      } finally {
        this.loading = false;
      }
    },

    async fetchUnscheduledMeetings() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/unscheduled-meetings/get-all-unscheduled-meetings",
        );
        this.unscheduled_meetings = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch unscheduled_meetings";
      } finally {
        this.loading = false;
      }
    },
    async fetchClassSections() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/class/get-classes",
        );
        this.sections = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch sections";
      } finally {
        this.loading = false;
      }
    },
    async fetchFinalSchedules() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/final-generated-class-schedule/get-all-final-schedules",
        );
        this.final_schedules = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch final schedules";
      } finally {
        this.loading = false;
      }
    },
    async fetchInstructors() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/instructors/get-instructors",
        );
        this.instructors = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch instructors";
      } finally {
        this.loading = false;
      }
    },

    async fetchCourses() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/courses/get-courses",
        );
        this.courses = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch courses";
      } finally {
        this.loading = false;
      }
    },

    async fetchCurriculums() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/curriculums/get-curriculums",
        );
        this.curriculums = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch curriculums";
      } finally {
        this.loading = false;
      }
    },

    async fetchPrograms() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/programs/get-programs",
        );
        this.programs = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch programs";
      } finally {
        this.loading = false;
      }
    },

    async fetchSections() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/sections/get-sections",
        );
        this.sections = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch sections";
      } finally {
        this.loading = false;
      }
    },

    async fetchRooms() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/rooms/get-rooms",
        );
        this.rooms = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch rooms";
      } finally {
        this.loading = false;
      }
    },

    async fetchTime() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/time/get-time",
        );
        this.time = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch time";
      } finally {
        this.loading = false;
      }
    },

    async fetchSchedulers() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/class-schedules/get-class-schedules",
        );
        this.schedulers = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch schedulers";
      } finally {
        this.loading = false;
      }
    },

    async fetchProjects() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/projected/get-projected",
        );
        this.projects = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch projects";
      } finally {
        this.loading = false;
      }
    },

    async fetchInstitutes() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/institute/get-institutes",
        );
        this.institutes = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch institutes";
      } finally {
        this.loading = false;
      }
    },

    async fetchReportCurriculum() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/courses/get-report-curriculum-offer",
        );
        this.detailedReportCurriculum = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch detailedReportCurriculum";
      } finally {
        this.loading = false;
      }
    },

    async fetchCalendarEvents() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/calendar/get-all-calendar-events",
        );
        this.calendarEvents = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch calendarEvents";
      } finally {
        this.loading = false;
      }
    },

    async fetchUsers() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/all-raw",
        );
        this.users = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch users";
      } finally {
        this.loading = false;
      }
    },

    async fetchRawUsers() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/users/get-users",
        );
        this.rawusers = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch rawusers";
      } finally {
        this.loading = false;
      }
    },

    async fetchAssignClass() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/assign-class/get-assign-class",
        );
        this.assignClass = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch assignClass";
      } finally {
        this.loading = false;
      }
    },

    async fetchFaculty() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/instructors/raw",
        );
        this.faculty = data;
      } catch (err) {
        this.error = err.message || "Failed to fetch faculty";
      } finally {
        this.loading = false;
      }
    },

    // 🔹 Active years (real-time reactive)
    async fetchActiveYears() {
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/latest-active",
        );

        // Ensure array
        const activeYearsArray = Array.isArray(data) ? data : [data];

        // Only active years
        this.activeYears = activeYearsArray.filter((year) => year.is_active);

        // Set the latest active year for table filtering
        const previousYearId = this.activeYear?.school_year_id;
        this.activeYear = this.activeYears[0] || null;

        // Update timestamp
        this.lastUpdatedAt =
          this.activeYears.length > 0
            ? new Date(this.activeYears[0].updated_at)
            : null;

        // Return true if year changed
        return previousYearId !== this.activeYear?.school_year_id;
      } catch (err) {
        console.error("❌ Failed to fetch school years:", err);
        this.activeYears = [];
        this.activeYear = null;
        this.lastUpdatedAt = null;
        return false;
      }
    },
  },
});
