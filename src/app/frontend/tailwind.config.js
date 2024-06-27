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
          500: '#183D63',
          700: '#13304e',
          800: '#0e2339',
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

