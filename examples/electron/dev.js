const concurrently = require('concurrently')
const path = require('path')

const EXISTING_SERVER_PORT = process.env.EXISTING_SERVER_PORT ?? 8000

const { result } = concurrently(
  [
    {
      command: 'electron-vite dev --watch',
      name: 'Electron',
      env: { EXISTING_SERVER_PORT },
      cwd: path.resolve(__dirname)
    },
    {
      command: `nodemon --legacy-watch --watch engine --exec python scripts/dev.py`,
      name: 'Python',
      cwd: path.resolve(__dirname),
      env: {
        UVICORN_PORT: EXISTING_SERVER_PORT,
        UVICORN_HOST: '0.0.0.0'
      }
    }
  ],
  {
    prefix: 'name',
    killOthers: ['failure', 'success'],
    cwd: path.resolve(__dirname)
  }
)

result
  .then(() => {
    console.log('All processes have completed successfully')
  })
  .catch((reason) => {
    console.log('Some processes have failed:')
  })
