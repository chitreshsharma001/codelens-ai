# CodeLens AI backend

JavaScript API using Node.js built-in HTTP, fetch, environment loading and test runner. No third-party runtime dependencies are required. Requires Node.js 24+.

```sh
cd backend
npm start
```

Use `npm run dev` for automatic restarts and `npm test` for mocked API and service tests.

Copy the root `.env.example` to `.env` and set `GEMINI_API_KEY`. The server loads `backend/.env` first, then the root `.env`, without overriding existing environment variables. Optional settings: `GITLAB_API_TOKEN`, `GEMINI_MODEL` (default `gemini-flash-lite-latest`) and `PORT` (default 5000). The server binds to `0.0.0.0`.

API routes:

- `GET /api/health`: health status.
- `POST /api/analyze`: accepts `{"repo_url":"https://gitlab.com/group/project"}` and returns `success`, `repository`, `analysis`, and `documentation`.
- `POST /api/generate-readme`: same request body; returns `success` and a Markdown `readme` string.

Public GitLab.com projects work without a token; private projects require repository read access. Nested subgroups and clone URLs ending in `.git` are supported. Pass a project URL rather than a branch or file URL.

Invalid JSON and missing/invalid URLs return 400. GitLab errors retain their status, including friendly 429 responses. Unavailable optional metadata falls back to empty values. Gemini errors return clearly marked fallback analysis and documentation; check server logs for the reason. Fallback scores of 5 are placeholders, not measured results.

Docker: run `docker build -t codelens-backend backend` from the root, then `docker run --env-file .env -p 5000:5000 codelens-backend`.

For Render, select Node, set the root directory to `backend`, build command to `npm install`, and start command to `npm start`. Set API keys in the deployment environment.
