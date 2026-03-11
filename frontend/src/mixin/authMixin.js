// src/mixins/authMixin.js
import axios from "axios";
import { toast } from "vue3-toastify";
export default {
  data() {
    return {
      email: "",
      password: "",
      showPassword: false,
      errorMessage: "",
    };
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    async login() {
      try {
        const response = await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/auth/login",
          {
            email: this.email,
            password: this.password,
          },
          { withCredentials: true }
        );
        const role = response.data.role;
        localStorage.setItem("role", role);

        if (role === "Admin") {
          this.$router.push("/admin-dashboard");
        } else if (role === "Program Chairperson") {
          this.$router.push("/progchair-dashboard");
        } else if (role === "Faculty") {
          this.$router.push("/faculty-dashboard");
        }
      } catch (error) {
        toast.error("Login failed. Please check your credentials.");
        setTimeout(() => {
          this.errorMessage = "";
        }, 3000); // Clear message after 3 seconds
      }
    },
  },
};
