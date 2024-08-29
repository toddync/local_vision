/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.{html,js}", "./!(build|dist|.*)/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        white: "#fff",
        "gray-500": "#718096",
        midnightblue: "#120f43",
        "gray-200": "#e2e8f0",
        darkslateblue: "#1b2559",
        ghostwhite: "#f4f7fe",
        gray1: "rgba(255, 255, 255, 0.14)",
        gainsboro: "rgba(230, 230, 230, 0.14)",
        lavender: "#f3efff",
        blueviolet: "#603cff",
      },
      spacing: {},
      fontFamily: {
        "plus-jakarta-sans": "'Plus Jakarta Sans'",
        inherit: "inherit",
        poppins: "Poppins",
      },
      borderRadius: {
        "26xl": "45px",
        sm: "14px",
        "59xl": "78px",
        "11xl": "30px",
        "30xl": "49px",
        xl: "20px",
        "41xl": "60px",
        "20xl": "39px",
      },
    },
    fontSize: {
      sm: "0.875rem",
      xs: "0.75rem",
      base: "1rem",
      lg: "1.125rem",
      inherit: "inherit",
    },
    screens: {
      mq1125: {
        raw: "screen and (max-width: 1125px)",
      },
      mq1025: {
        raw: "screen and (max-width: 1025px)",
      },
      mq750: {
        raw: "screen and (max-width: 750px)",
      },
      mq450: {
        raw: "screen and (max-width: 450px)",
      },
    },
  },
  corePlugins: {
    preflight: false,
  },
};
