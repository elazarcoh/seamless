/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pages/**/*.{html,js,py}", "app.py", "components/**/*.{html,js,py}"],

  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
}

