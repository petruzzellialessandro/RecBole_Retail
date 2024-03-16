/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors:
      {
        primary: {
          100: '#000',
          500: '#2D2D2D',
        },
        accent:{
          500: '#F55233',
          700: '#F66347',
          800: '#F66246',
        },
      },
    },
  },
  plugins: [
    require('tailwindcss/nesting'),
    require('postcss-import'),
    require('autoprefixer'),
    require('tailwindcss'),
  ],
}

