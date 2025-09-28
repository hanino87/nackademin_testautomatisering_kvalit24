import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    allowedHosts: ['app-frontend', 'localhost'] // ✅ allow both local + Jenkins this makes jenkins to accept app-frontend vite dont get 403 not allowed 
  }
})
