import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  base: '',
  root: 'src',
  build: {
    outDir: '../../backend/static',
    emptyOutDir: true
  },
  plugins: [react()]
})


