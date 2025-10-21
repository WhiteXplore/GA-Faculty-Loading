import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/views/LoginView.vue";
import globalSidebar from "../components/global-dashboard-layout/navigation/sidebar.vue";
// import ProgramChairSidebar from "../components/program-chairperson/navigation/sidebar.vue";
import landingPage from "../components/global/landing-page.vue";
import NotFound from "@/views/404.vue";

const routes = [
  {
    path: "/",
    name: "lading-page",
    component: landingPage,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },

  // Admin View
  {
    path: "/navigation",
    name: "navigation",
    component: globalSidebar,
    children: [
      {
        path: "/profile-view",
        name: "profile-view",
        component: () =>
          import(
            "../components/global-dashboard-layout/navigation/profile/view-profile.vue"
          ),
      },
      {
        path: "/admin-dashboard",
        name: "admin-dashboard",
        component: () =>
          import(
            "../components/global-dashboard-layout/dashboard/dashboard.vue"
          ),
        meta: { requiresAuth: true, role: "Admin" },
      },
      {
        path: "/instructors",
        name: "instructors",
        component: () => import("@/components/admin/records/instructor.vue"),
        meta: { requiresAuth: true, role: "Admin" },
      },
      {
        path: "/institutes",
        name: "instituts",
        component: () => import("@/components/admin/records/institutes.vue"),
        meta: { requiresAuth: true, role: "Admin" },
      },
      {
        path: "/courses",
        name: "courses",
        component: () => import("@/components/admin/records/courses.vue"),
        meta: { requiresAuth: true, roles: ["Admin"] },
        children: [],
      },
      {
        path: "/curriculums",
        name: "curriculums",
        component: () => import("@/components/admin/records/curriculum.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },
      {
        path: "/programs",
        name: "programs",
        component: () => import("@/components/admin/records/programs.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },

      {
        path: "/rooms",
        name: "rooms",
        component: () => import("@/components/admin/records/rooms.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },
      {
        path: "/school-years",
        name: "school-years",
        component: () => import("@/components/admin/records/school-year.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },
      {
        path: "/system-overview",
        name: "system-overview",
        component: () =>
          import("@/components/admin/records/system-overview.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },
      {
        path: "/admin-assign-classes",
        name: "admin-assign-classes",
        component: () =>
          import("@/components/admin/records/assign-classes.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },
      {
        path: "/admin-assigned-courses",
        name: "admin-assigned-courses",
        component: () =>
          import("@/components/admin/records/assigned-course.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },
      {
        path: "/faculty-loads",
        name: "faculty-loads",
        component: () => import("@/components/admin/records/faculty-loads.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },

      {
        path: "/class-list",
        name: "class-list",
        component: () => import("@/components/admin/records/class-list.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },
      {
        path: "/classes",
        name: "classes",
        component: () => import("@/components/admin/records/classes.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },

      {
        path: "/user-accounts",
        name: "user-accounts",
        component: () => import("@/components/admin/records/users.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },

      {
        path: "/report-curriculum-offers",
        name: "report-curriculum-offers",
        component: () =>
          import("@/components/admin/records/report-curriculum-offers.vue"),
        meta: { requiresAuth: true, role: "Admin" },
      },
      {
        path: "/view-curriculum-offers/:institute_id",
        name: "view-curriculum-offers",
        component: () =>
          import("@/components/admin/records/view-report-curriculum-offer.vue"),
        meta: { requiresAuth: true, role: "Admin" },
      },
      {
        path: "/view-faculty-loads",
        name: "view-faculty-loads",
        component: () =>
          import("@/components/admin/records/view-faculty-loads.vue"),
        meta: { requiresAuth: true, role: "Admin" },
        children: [],
      },
    ],
  },
  // Program Chair
  {
    path: "/progchair-navigation",
    name: "progchair-navigation",
    component: globalSidebar,
    children: [
      {
        path: "/progchair-dashboard",
        name: "progchair-dashboard",
        component: () =>
          import(
            "../components/global-dashboard-layout/dashboard/dashboard.vue"
          ),
        meta: { requiresAuth: true, role: "Program Chairperson" },
      },
      {
        path: "/program-courses",
        name: "program-courses",
        component: () => import("@/components/admin/records/courses.vue"),
        meta: { requiresAuth: true, roles: ["Program Chairperson"] },
        children: [],
      },
      {
        path: "/program-programs",
        name: "program-programs",
        component: () => import("@/components/admin/records/programs.vue"),
        meta: { requiresAuth: true, roles: ["Program Chairperson"] },
        children: [],
      },
      {
        path: "/year-section",
        name: "year-section",
        component: () =>
          import(
            "@/components/program-chairperson/program-record/year-section.vue"
          ),
        meta: { requiresAuth: true, role: "Program Chairperson" },
        children: [],
      },
      {
        path: "/assigned-course",
        name: "assigned-course",
        component: () =>
          import(
            "@/components/program-chairperson/program-record/assigned-course.vue"
          ),
        meta: { requiresAuth: true, role: "Program Chairperson" },
        children: [],
      },
      {
        path: "/program-chairperson-assign-classes",
        name: "program-chairperson-assign-classes",
        component: () =>
          import("@/components/admin/records/assign-classes.vue"),
        meta: { requiresAuth: true, role: "Program Chairperson" },
        children: [],
      },
      {
        path: "/program-chairperson-faculty-list",
        name: "program-chairperson-faculty-list",
        component: () => import("@/components/admin/records/instructor.vue"),
        meta: { requiresAuth: true, role: "Program Chairperson" },
      },
      {
        path: "/program-chair-faculty-loads",
        name: "program-chair-faculty-loads",
        component: () => import("@/components/admin/records/faculty-loads.vue"),
        meta: { requiresAuth: true, role: "Program Chairperson" },
        children: [],
      },
      {
        path: "/program-faculty-loading",
        name: "program-faculty-loading",
        component: () =>
          import(
            "@/components/program-chairperson/program-record/faculty-loads.vue"
          ),
        meta: { requiresAuth: true, role: "Program Chairperson" },
      },
      {
        path: "/faculty-expertise",
        name: "faculty-expertise",
        component: () =>
          import(
            "@/components/program-chairperson/program-record/faculty-expertise.vue"
          ),
        meta: { requiresAuth: true, role: "Program Chairperson" },
      },
    ],
  },
  {
    path: "/faculty-navigation",
    name: "faculty-navigation",
    component: globalSidebar,
    children: [
      {
        path: "/faculty-dashboard",
        name: "faculty-dashboard",
        component: () =>
          import(
            "../components/global-dashboard-layout/dashboard/dashboard.vue"
          ),
        meta: { requiresAuth: true, role: "Faculty" },
      },
      {
        path: "/profile-view",
        name: "profile-view",
        component: () =>
          import(
            "../components/global-dashboard-layout/navigation/profile/view-profile.vue"
          ),
      },
    ],
  },

  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// 🔒 Navigation Guard
router.beforeEach((to, from, next) => {
  const role = localStorage.getItem("role");

  if (to.meta.requiresAuth) {
    if (!role) return next({ name: "login" });

    // Check if route has single role or multiple roles
    if (to.meta.role && to.meta.role !== role) {
      return next({ name: "NotFound" });
    }

    if (to.meta.roles && !to.meta.roles.includes(role)) {
      return next({ name: "NotFound" });
    }
  }

  next();
});

export default router;
