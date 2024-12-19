// tailwind.config.js
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  theme: {
    extend: {
      colors: {
        kon: '#0f69af',  // 自定義的藍色
        secondary: '#38b2ac', // 自定義的綠色
        customGray: '#f4f4f4', // 自定義的灰色
      }
    }
  },
  plugins: [],
  
}
