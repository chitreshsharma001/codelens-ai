import { createServer } from 'node:http';
import { GitLabService } from './services/gitlab_service.js';
import { AIService } from './services/ai_service.js';

export function createApp({ gitlab = new GitLabService(), ai = new AIService() } = {}) {
  return createServer(async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    const send = (status, body) => {
      res.writeHead(status, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(body));
    };
    if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
    const path = new URL(req.url, 'http://localhost').pathname;
    if (path === '/api/health' && req.method === 'GET') {
      send(200, { status: 'healthy', message: 'CodeLens AI is running' }); return;
    }
    if (!['/api/analyze', '/api/generate-readme'].includes(path)) {
      send(404, { error: 'Not found' }); return;
    }
    if (req.method !== 'POST') { send(405, { error: 'Method not allowed' }); return; }
    try {
      const chunks = [];
      let size = 0;
      for await (const chunk of req) {
        size += chunk.length;
        if (size > 1_048_576) {
          send(413, { error: 'Request body too large' }); return;
        }
        chunks.push(chunk);
      }
      let data;
      try { data = JSON.parse(Buffer.concat(chunks).toString('utf8')); }
      catch { send(400, { error: 'Invalid JSON body' }); return; }
      if (typeof data?.repo_url !== 'string' || !data.repo_url.trim()) {
        send(400, { error: 'Repository URL is required' }); return;
      }
      const repo = await gitlab.getRepositoryData(data.repo_url);
      if (!repo) { send(400, { error: 'Could not fetch repository data. Check URL and permissions.' }); return; }
      if (path === '/api/generate-readme') {
        send(200, { success: true, readme: await ai.generateReadme(repo) }); return;
      }
      const analysis = await ai.analyzeRepository(repo);
      const documentation = await ai.generateDocumentation(repo, analysis);
      send(200, {
        success: true,
        repository: { name: repo.name, description: repo.description, url: repo.web_url,
          languages: repo.languages || {}, stars: repo.star_count || 0, forks: repo.forks_count || 0 },
        analysis, documentation,
      });
    } catch (error) {
      if (error.status === 429) {
        send(429, { error: 'GitLab rate limit exceeded',
          message: 'Too many requests to GitLab API. Try again in a few minutes or add GITLAB_API_TOKEN in backend/.env.',
          tips: ['Wait 1-2 minutes before retrying', 'Add GITLAB_API_TOKEN for higher limits'] });
      } else {
        console.error(error.message);
        send(error.status || 500, { error: error.message || 'Internal server error' });
      }
    }
  });
}
