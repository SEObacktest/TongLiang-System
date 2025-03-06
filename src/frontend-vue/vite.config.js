import { defineConfig } from 'vite'
import { resolve } from 'path'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@img': resolve(__dirname, 'src/assets/imgs'),
      '@css': resolve(__dirname, 'src/assets/css'),
      '@icons': resolve(__dirname, 'src/assets/icons'),
      '@js': resolve(__dirname, 'src/assets/js'),
      '@video': resolve(__dirname, 'src/assets/video'),
      '@fonts': resolve(__dirname, 'src/assets/fonts'),
    },
  },
  base: '',
  server: {
    host: '0.0.0.0',
    port: 3000,
    open: false,
    cors: true,
    
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        // vite对于proxy的封装和vuecli不一样，需要额外增加secure: false绕过https的安全验证才能请求到https的地址
        changeOrigin: true, // 允许跨域
        secure: false,
      },
      '/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true, // 允许跨域
        secure: false,
      }
    },
  },
})

