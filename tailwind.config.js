/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./donate/*.{html,css,js}", "./styles/donate.tailwind.css"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
