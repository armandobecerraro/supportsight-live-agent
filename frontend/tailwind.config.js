/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#01696F', hover: '#0C4E54' },
        surface: '#F9F8F5',
        border: '#D4D1CA',
      },
    },
  },
  plugins: [],
}
