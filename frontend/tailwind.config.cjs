/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin');

module.exports = {
  darkMode: ["class"],
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [
    plugin(function ({ addComponents }) {
      addComponents({
        '.radix-select-trigger': {
          '@apply flex items-center justify-between border border-gray-300 rounded-md px-4 py-2 text-sm cursor-pointer': '',
        },
        '.radix-select-content': {
          '@apply bg-white border border-gray-200 rounded-md shadow-md overflow-hidden': '',
        },
        '.radix-select-item': {
          '@apply px-4 py-2 cursor-pointer hover:bg-gray-100': '',
        },
        '.radix-select-arrow': {
          '@apply h-4 w-4 text-gray-500': '',
        },
      });
    }),
  ],
};
