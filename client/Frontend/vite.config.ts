import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import { readFileSync, existsSync } from 'node:fs'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))

function loadRootEnv(): Record<string, string> {
  const rootEnvPath = resolve(__dirname, '../../.env')
  if (!existsSync(rootEnvPath)) return {}
  const lines = readFileSync(rootEnvPath, { encoding: 'utf-8' }).split(/\r?\n/)
  const env: Record<string, string> = {}
  for (const raw of lines) {
    const line = raw.trim()
    if (!line || line.startsWith('#') || !line.includes('=')) continue
    const [k, ...rest] = line.split('=')
    const key = k.trim()
    const value = rest.join('=').trim().replace(/^['"]|['"]$/g, '')
    if (key.startsWith('VITE_')) env[key] = value
  }
  return env
}

export default defineConfig(({ mode }) => {
  const viteEnv = loadEnv(mode, process.cwd(), '')
  const rootEnv = loadRootEnv()
  return {
    plugins: [react()],
    server: {
      host: '0.0.0.0',
      port: 5173,
      // Проксируем вызовы API в dev-режиме на бэкенд
      proxy: {
        '/api': {
          target: (rootEnv.VITE_API_BASE_URL || viteEnv.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, ''),
          changeOrigin: true,
          secure: false,
        },
      },
    },
    define: {
      ...Object.fromEntries(
        Object.entries({ ...viteEnv, ...rootEnv })
          .filter(([k]) => k.startsWith('VITE_'))
          .map(([k, v]) => [
            `import.meta.env.${k}`,
            JSON.stringify(v),
          ]),
      ),
    },
  }
})
