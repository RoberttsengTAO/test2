import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],

  server: {
    proxy: {
      // 代理 API 請求
      '/api': {
        target: 'http://backend:8000', // 後端服務地址
        //target: 'http://localhost:8000',
        changeOrigin: true,              // 更改來源
        rewrite: (path) => path.replace(/^\/api/, ''), // 可選，移除/api前綴
      },
    },
  },
})
