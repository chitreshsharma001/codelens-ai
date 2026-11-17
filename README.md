# CodeLens AI

AI-powered GitLab repository analysis and documentation generation with a React frontend and JavaScript backend.

The app retrieves repository metadata, file structure, languages, README and recent commits from GitLab, then uses Gemini to generate an overview, quality and complexity assessments, architecture notes, suggestions and downloadable documentation. Assessments use metadata and README context rather than a full source-code audit.

## Run locally

Requires Node.js 24+ and a Gemini API key.

1. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`. Optionally add `GITLAB_API_TOKEN` for private repositories and higher limits.
2. Start the backend:

   ```sh
   cd backend
   npm start
   ```

3. In another terminal, start the frontend:

   ```sh
   cd frontend
   npm install
   npm run dev
   ```

Open http://localhost:3000. Vite proxies `/api` to http://localhost:5000. Set `VITE_API_URL` when building a frontend hosted separately from the API; see `frontend/.env.example`.

Alternatively, run `docker compose up --build` from the root after creating `.env`.

## Backend

Uses Node.js built-in HTTP, fetch, environment-file loading and tests with no third-party runtime dependencies. Gemini is called through its REST API.

- `GET /api/health`
- `POST /api/analyze` with `{"repo_url":"https://gitlab.com/group/project"}`
- `POST /api/generate-readme` with the same body

Run `npm test` in `backend` for mocked API and service tests. Run `npm run build` in `frontend` for a production build. See [backend setup](backend/README.md) for configuration, fallback behavior and deployment commands.

## Structure

```text
backend/
  server.js                    Environment loading and startup
  app.js                       API routes and CORS
  services/gitlab_service.js    GitLab integration
  services/ai_service.js        Gemini integration and fallbacks
  test/backend.test.js         API and service tests
frontend/                      React, Vite and Tailwind CSS
scripts/ai_gitlab_bot.js        CI review workflow simulation
monitoring/health_check.js      Deployment health check
.gitlab-ci.yml                 Tests, security scans and Docker builds
```

The CI review bot demonstrates the workflow; it does not perform an actual AI code review. Backend tests mock external services and do not post comments or call paid APIs.

## Deployment

Deploy the backend as a Node service (`backend` root, `npm install` build, `npm start` start), or use its Dockerfile. Set `GEMINI_API_KEY` and optional `GITLAB_API_TOKEN` in the hosting environment. Build the frontend with `VITE_API_URL` set to the deployed backend URL.

## License

See [LICENSE](LICENSE).
