import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createApp } from '../app.js';
import { GitLabService } from '../services/gitlab_service.js';
import { AIService, fallbackAnalysis, fallbackDocumentation, parseAIResponse } from '../services/ai_service.js';

const repo = { name: 'Example', description: 'Example repository', web_url: 'https://gitlab.com/team/example', languages: { JavaScript: 100 }, file_tree: [] };
const analysis = fallbackAnalysis(repo);
const documentation = fallbackDocumentation(repo, analysis);

test('API preserves frontend contract, README route, validation and CORS', async t => {
  const calls = [];
  const server = createApp({ gitlab: { async getRepositoryData(url) { calls.push(url); return repo; } },
    ai: { async analyzeRepository() { return analysis; }, async generateDocumentation() { return documentation; }, async generateReadme() { return '# Example'; } } });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => { server.close(resolve); server.closeAllConnections(); }));
  const url = `http://127.0.0.1:${server.address().port}`;
  const post = (path, body) => fetch(url + path, { method: 'POST', body, headers: { 'Content-Type': 'application/json' } });
  assert.deepEqual(await (await fetch(url + '/api/health')).json(), { status: 'healthy', message: 'CodeLens AI is running' });
  const response = await post('/api/analyze', JSON.stringify({ repo_url: repo.web_url }));
  assert.equal(response.status, 200);
  assert.equal(response.headers.get('access-control-allow-origin'), '*');
  assert.deepEqual(await response.json(), { success: true, repository: { name: repo.name, description: repo.description, url: repo.web_url, languages: repo.languages, stars: 0, forks: 0 }, analysis, documentation });
  assert.deepEqual(await (await post('/api/generate-readme', JSON.stringify({ repo_url: repo.web_url }))).json(), { success: true, readme: '# Example' });
  for (const body of ['{', '{}', 'null', '[]', '{"repo_url":123}']) assert.equal((await post('/api/analyze', body)).status, 400);
  assert.equal(calls.length, 2);
  assert.equal((await post('/api/analyze', JSON.stringify({ repo_url: 'x'.repeat(1_048_576) }))).status, 413);
  assert.equal((await fetch(url + '/api/analyze')).status, 405);
  assert.equal((await fetch(url + '/missing')).status, 404);
  assert.equal((await fetch(url + '/api/analyze', { method: 'OPTIONS' })).status, 204);
});

test('API returns friendly rate limit errors', async t => {
  const server = createApp({ gitlab: { async getRepositoryData() { throw Object.assign(new Error('Rate limited'), { status: 429 }); } }, ai: {} });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => { server.close(resolve); server.closeAllConnections(); }));
  const response = await fetch(`http://127.0.0.1:${server.address().port}/api/analyze`, { method: 'POST', body: JSON.stringify({ repo_url: repo.web_url }) });
  assert.equal(response.status, 429);
  assert.ok((await response.json()).tips.length);
});

test('GitLab encodes subgroups, sends token, fetches default-branch README and maps commits', async () => {
  const calls = [];
  const service = new GitLabService({ token: 'test-token', fetchImpl: async (url, options) => {
    calls.push(url);
    assert.equal(options.headers['PRIVATE-TOKEN'], 'test-token');
    if (url.includes('/raw?')) return new Response('# Hello');
    if (url.includes('/tree?')) return Response.json([{ type: 'blob', path: 'a.js' }, { type: 'tree', path: 'src' }]);
    if (url.endsWith('/languages')) return Response.json({ JavaScript: 100 });
    if (url.includes('/commits?')) return Response.json([{ id: '1', author_name: 'Dev', message: 'a'.repeat(300) }]);
    return Response.json({ ...repo, default_branch: 'develop' });
  } });
  const result = await service.getRepositoryData('https://gitlab.com/team/subgroup/example.git/');
  assert.ok(calls.every(url => url.includes('/projects/team%2Fsubgroup%2Fexample')));
  assert.ok(calls.some(url => url.endsWith('raw?ref=develop')));
  assert.equal(result.file_tree[0].type, 'tree');
  assert.equal(result.recent_commits[0].author, 'Dev');
  assert.equal(result.recent_commits[0].message.length, 200);
  assert.equal(result.readme_content, '# Hello');
  for (const url of ['https://evil.com/gitlab.com/team/repo', 'https://gitlab.com/team/repo/-/tree/main', 'not a URL']) assert.throws(() => service.extractProjectPath(url), /Invalid/);
});

test('GitLab tolerates unavailable supplemental data but propagates rate limits', async () => {
  const service = new GitLabService({ fetchImpl: async url => url.endsWith('/projects/team%2Frepo') ? Response.json(repo) : new Response('', { status: 404 }) });
  const result = await service.getRepositoryData('https://gitlab.com/team/repo');
  assert.deepEqual(result.languages, {});
  assert.deepEqual(result.file_tree, []);
  assert.equal(result.readme_content, 'No README found');
  const limited = new GitLabService({ fetchImpl: async () => new Response('', { status: 429 }) });
  await assert.rejects(limited.getRepositoryData(repo.web_url), { status: 429 });
});

test('Gemini uses REST JSON output and parses fenced responses', async () => {
  const ai = new AIService({ apiKey: 'test-key', fetchImpl: async (url, options) => {
    assert.ok(url.endsWith(':generateContent'));
    assert.equal(options.headers['x-goog-api-key'], 'test-key');
    assert.equal(JSON.parse(options.body).generationConfig.responseMimeType, 'application/json');
    return Response.json({ candidates: [{ content: { parts: [{ text: JSON.stringify(analysis) }] } }] });
  } });
  assert.deepEqual(await ai.analyzeRepository(repo), analysis);
  assert.deepEqual(parseAIResponse('```json\n{"ok":true}\n```'), { ok: true });
  assert.throws(() => parseAIResponse('[]'));
});

test('AI failures and incomplete responses retain renderable fallback documents', async () => {
  const ai = new AIService({ apiKey: 'test-key', fetchImpl: async () => Response.json({ candidates: [{ content: { parts: [{ text: '{}' }] } }] }) });
  assert.deepEqual(await ai.analyzeRepository(repo), analysis);
  assert.deepEqual(await ai.generateDocumentation(repo, analysis), documentation);
  const unavailable = new AIService({ apiKey: '', fetchImpl: () => { throw new Error('Must not call without key'); } });
  assert.match(await unavailable.generateReadme(repo), /# Example/);
});

test('Gemini documentation and README return generated content', async () => {
  const generated = { ...documentation, readme: { ...documentation.readme, content: '# Generated README' } };
  const ai = new AIService({ apiKey: 'test-key', fetchImpl: async (_url, options) => {
    const prompt = JSON.parse(options.body).contents[0].parts[0].text;
    const result = prompt.startsWith('You are') ? analysis : generated;
    return Response.json({ candidates: [{ content: { parts: [{ text: JSON.stringify(result) }] } }] });
  } });
  assert.deepEqual(await ai.generateDocumentation(repo, analysis), generated);
  assert.equal(await ai.generateReadme(repo), '# Generated README');
  const failed = new AIService({ apiKey: 'test-key', fetchImpl: async () => new Response('', { status: 503 }) });
  assert.deepEqual(await failed.analyzeRepository(repo), analysis);
});
