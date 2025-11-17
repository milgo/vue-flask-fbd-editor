import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
	  rollupOptions: {
		  output: {
			  dir: 'webservice/dist',
			  entryFileNames: 'plugin.js',
			  assetFileNames: (assetInfo) => {
				if (assetInfo.name == 'styles-light.css')
					return 'styles-light.css'
				if (assetInfo.name == 'warning.png')
					return 'warning.png'
				if (assetInfo.name == 'vite.svg')
					return 'vite.svg'
				return assetInfo.name;
			  },
			  chunkFileNames: 'chunk.js',
			  manualChunks: undefined,
		  }
		}
	  },
})
