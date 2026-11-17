# CodeLens AI frontend

React 18, Vite and Tailwind CSS frontend for the JavaScript backend.

```sh
npm install
npm run dev
```

Open http://localhost:3000. Start the backend separately with `npm start` in `../backend`. Vite proxies `/api` to http://localhost:5000 by default.

To use a separately hosted API, copy `.env.example` to `.env` and set `VITE_API_URL` to the backend origin before building.

```sh
npm run build
npm run preview
```

Build output is written to `dist`. The Dockerfile builds the frontend and serves it through Nginx. Docker Compose supplies the API URL at build time.

See the [project README](../README.md) for environment setup and deployment.
