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
    projecs: [],
    institutes: [],
    detailedReportCurriculum: [],
    calendarEvents: [],
    users: [],
    rawusers: [],
    assignClass: [],
    faculty: [],
    year: null,
    sem: null, // ✅ Added for active semester
    loading: false,
    error: null,
  }),

  actions: {
    async fetchInstructors() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(
          "http://localhost:8000/instructors/get-instructors"
        );
        this.instructors = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/courses/get-courses"
        );
        this.courses = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/curriculums/get-curriculums"
        );
        this.curriculums = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/programs/get-programs"
        );
        this.programs = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/sections/get-sections"
        );
        this.sections = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/rooms/get-rooms"
        );
        this.rooms = response.data;
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
        const response = await axios.get("http://localhost:8000/time/get-time");
        this.time = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/class-schedules/get-class-schedules"
        );
        this.schedulers = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/projected/get-projected"
        );
        this.projects = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/institute/get-institutes"
        );
        this.institutes = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/courses/get-report-curriculum-offer"
        );
        this.detailedReportCurriculum = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/calendar/get-all-calendar-events"
        );
        this.calendarEvents = response.data;
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
        const response = await axios.get("http://localhost:8000/auth/all");
        this.users = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/users/get-users"
        );
        this.rawusers = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/assign-class/get-assign-class"
        );
        this.assignClass = response.data;
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
        const response = await axios.get(
          "http://localhost:8000/instructors/raw"
        );
        this.faculty = response.data;
      } catch (err) {
        this.error = err.message || "Failed to fetch faculty";
      } finally {
        this.loading = false;
      }
    },

    // ✅ Active Year Fetcher
    async fetchActiveYear() {
      try {
        const res = await axios.get("http://localhost:8000/active-year/active");

        if (Array.isArray(res.data)) {
          const active = res.data.find((item) => item.isActive === true);
          this.year = active ? active.year : null;
        } else if (res.data && res.data.isActive) {
          this.year = res.data.year;
        } else {
          this.year = null;
        }
      } catch (err) {
        console.error("Failed to fetch active year:", err);
      }
    },

    async updateYear(newYear) {
      try {
        await axios.post("http://localhost:8000/active-year", {
          year: newYear,
        });
        this.year = newYear;
      } catch (err) {
        console.error("Failed to update active year:", err);
      }
    },

    // ✅ Active Semester Fetcher (Fixed)
    async fetchActiveSem() {
      try {
        const res = await axios.get(
          "http://localhost:8000/active-semester/active"
        );

        if (Array.isArray(res.data)) {
          // Handle array response (if API ever returns multiple)
          const active = res.data.find((item) => item.is_active === true);
          this.sem = active ? active.semester : null;
        } else if (res.data && res.data.is_active) {
          // Handle object response (your current case)
          this.sem = res.data.semester;
        } else {
          this.sem = null;
        }

        console.log("✅ Active semester fetched:", this.sem);
      } catch (err) {
        console.error("❌ Failed to fetch active semester:", err);
      }
    },

    async updateSem(newSem) {
      try {
        await axios.post("http://localhost:8000/active-semester", {
          semester: newSem,
        });
        this.sem = newSem; // ✅ instantly update local state
      } catch (err) {
        console.error("Failed to update active semester:", err);
      }
    },
  },
});
