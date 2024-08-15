/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./examples/**/*.{html,js,py}"],

  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
}

