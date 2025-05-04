import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  preview: {
    // Allow your Render domain to access the preview server
    host: '0.0.0.0',
    port: Number(process.env.PORT) || 3000,
    strictPort: true,
    allowedHosts: [
      'trip-finder-ui.onrender.com',
      'localhost',
      // Add any other domains you might use
    ]
  },
}) 