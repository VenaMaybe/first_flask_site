import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: { // lets it call flask api
    proxy: {
      '/api': 'http://0.0.0.0:5000'
    }
  }
})