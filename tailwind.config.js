/** @type {import('tailwindcss').Config} */
export default {
	content: ["./src/**.{html,js,svelte,ts,jsx,tsx}"],
	theme: {
		extend: {
			transitionProperty: {
				height: "height",
			},
			colors: {
				"noble-black-700": "#131619",
				"noble-black-600": "#1a1d21",
				"noble-black-300": "#9b9c9e",
				"noble-black-400": "#686b6e",
				"noble-black-800": "#0d0f10",
				"noble-black-0": "#fff",
				"noble-black-500": "#363a3d",
				"glass-fill": "rgba(215, 237, 237, 0.16)",
				royalblue: "#4d62e5",
				lightgreen: "#b6f09c",
				"glass-stroke": "rgba(255, 255, 255, 0.08)",
				"noble-black-200": "#cdcecf",
				"heisenberg-blue-500": "#82dbf7",
				"noble-black-100": "#e8e9e9",
			},
			spacing: {},
			fontFamily: {
				"body-s-semibold": "'Plus Jakarta Sans'",
				inter: "Inter",
			},
			borderRadius: {
				"3xs": "10px",
				xl: "20px",
			},
		},
		fontSize: {
			xs: "12px",
			sm: "14px",
			xl: "20px",
			base: "16px",
			inherit: "inherit",
		},
		screens: {
			mq900: {
				raw: "screen and (max-width: 900px)",
			},
			mq675: {
				raw: "screen and (max-width: 675px)",
			},
			mq450: {
				raw: "screen and (max-width: 450px)",
			},
			sm: "640px",
			md: "768px",
			lg: "1024px",
			xl: "1280px",
			"2xl": "1400px",
		},
	},
	corePlugins: {
		preflight: false,
	},
};
