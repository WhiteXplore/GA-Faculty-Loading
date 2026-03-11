/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        defaultGreen: "#147452",
      },

      /* ✅ FONT SETUP */
      fontFamily: {
        poppins: ["Poppins", "sans-serif"],
        sans: ["Poppins", "sans-serif"], // make poppins default
      },

      /* ✅ OPTIONAL: semantic font weights */
      fontWeight: {
        light: "300",
        regular: "400",
        medium: "500",
        semibold: "600",
        bold: "700",
      },

      keyframes: {
        spinSlow: {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        fadeIn: {
          "0%": { opacity: 0 },
          "100%": { opacity: 1 },
        },
        slideUp: {
          "0%": { transform: "translateY(20px)", opacity: 0 },
          "100%": { transform: "translateY(0)", opacity: 1 },
        },
        slideDown: {
          "0%": { transform: "translateY(-20px)", opacity: 0 },
          "100%": { transform: "translateY(0)", opacity: 1 },
        },
        scaleUp: {
          "0%": { transform: "scale(0.95)", opacity: 0 },
          "100%": { transform: "scale(1)", opacity: 1 },
        },
      },

      animation: {
        spinSlow: "spinSlow 30s linear infinite",
        fadeIn: "fadeIn 0.6s ease-out forwards",
        slideUp: "slideUp 0.5s ease-out forwards",
        slideDown: "slideDown 0.5s ease-out forwards",
        scaleUp: "scaleUp 0.4s ease-out forwards",
      },
    },
  },
};
