import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { getProxyOptions } from 'frappe-ui/src/utils/vite-dev-server'
import { webserver_port } from '../../../sites/common_site_config.json'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host:true,
    port: 8080,
    proxy: {
        "^/(app|login|api|assets|files)": {
          // Localhost resolution changes in Node 17
          target: `http://localhost:${webserver_port}`,
          ws: true,
          router: function (req) {
            const site_name = req.headers.host.split(":")[0];
            return `http://${site_name}:${webserver_port}`;
          },
        },
      },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      "tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
    },
  },
  build: {
    "^/(app|login|api|assets|files)": {
        // Localhost resolution changes in Node 17
        target: `http://localhost:${webserver_port}`,
        ws: true,
        router: function (req) {
          const site_name = req.headers.host.split(":")[0];
          return `http://${site_name}:${webserver_port}`;
        },
      },
    outDir: `../${path.basename(path.resolve('..'))}/public/frontend`,
    emptyOutDir: true,
    target: 'es2015',
    commonjsOptions: {
        include: [/tailwind.config.js/, /node_modules/],
    },
  },
  optimizeDeps: {
    include: ['frappe-ui > feather-icons', 'showdown', "tailwind.config.js",'engine.io-client'],
  },
})
