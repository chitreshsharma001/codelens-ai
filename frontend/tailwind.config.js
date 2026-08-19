/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gitlab: {
          orange: '#FC6D26',
          purple: '#6E49CB',
          dark: '#1F1E24'
        }
      }
    },
  },
  plugins: [],
}