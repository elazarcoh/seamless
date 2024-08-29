/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pages/**/*.{html,js,py}", "app.py", "main.py", "components/**/*.{html,js,py}"],

  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
}

