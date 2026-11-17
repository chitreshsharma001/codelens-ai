export class GitLabService {
  constructor({ token = process.env.GITLAB_API_TOKEN, fetchImpl = fetch } = {}) {
    this.fetch = fetchImpl;
    this.headers = token ? { 'PRIVATE-TOKEN': token } : {};
    this.baseUrl = 'https://gitlab.com/api/v4';
  }

  extractProjectPath(repoUrl) {
    try {
      const url = new URL(repoUrl);
      const path = url.pathname.replace(/\/+$/, '').replace(/\.git$/, '').slice(1);
      if (url.protocol !== 'https:' || url.hostname !== 'gitlab.com' || path.split('/').length < 2 || path.includes('/-/')) throw new Error();
      return path;
    } catch { throw Object.assign(new Error('Invalid GitLab repository URL'), { status: 400 }); }
  }

  async request(path, { text = false } = {}) {
    const response = await this.fetch(`${this.baseUrl}${path}`, {
      headers: this.headers, signal: AbortSignal.timeout(10_000),
    });
    if (!response.ok) throw Object.assign(new Error(`GitLab request failed (${response.status})`), { status: response.status });
    return text ? response.text() : response.json();
  }

  async optional(path, fallback, options) {
    try { return await this.request(path, options); }
    catch (error) { if (error.status === 429) throw error; return fallback; }
  }

  async getReadme(project, branch) {
    for (const name of ['README.md', 'README.MD', 'readme.md', 'Readme.md', 'README']) {
      const content = await this.optional(`${project}/repository/files/${encodeURIComponent(name)}/raw?ref=${encodeURIComponent(branch)}`, null, { text: true });
      if (content !== null) return content;
    }
    return 'No README found';
  }

  async getRepositoryData(repoUrl) {
    const project = `/projects/${encodeURIComponent(this.extractProjectPath(repoUrl))}`;
    const details = await this.request(project);
    const branch = details.default_branch || 'main';
    const [tree, languages, readme, commits] = await Promise.all([
      this.optional(`${project}/repository/tree?recursive=true&per_page=100`, []),
      this.optional(`${project}/languages`, {}), this.getReadme(project, branch),
      this.optional(`${project}/repository/commits?per_page=10`, []),
    ]);
    return { ...details, languages, readme_content: readme,
      file_tree: tree.sort((a, b) => Number(b.type === 'tree') - Number(a.type === 'tree') || a.path.localeCompare(b.path)).slice(0, 100),
      recent_commits: commits.map(c => ({ id: c.id, title: c.title, author: c.author_name, date: c.created_at, message: (c.message || '').slice(0, 200) })) };
  }
}
