import { useState } from 'react'
import { Search, GitBranch } from 'lucide-react'

export default function AnalysisForm({ onAnalyze, disabled }) {
  const [repoUrl, setRepoUrl] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (repoUrl.trim()) {
      onAnalyze(repoUrl.trim())
    }
  }

  return (
    <div className="card animate-fade-in">
      <form onSubmit={handleSubmit}>
        <label className="block mb-4">
          <div className="flex items-center gap-2 mb-2 text-gray-300">
            <GitBranch className="w-5 h-5" />
            <span className="font-semibold">GitLab Repository URL</span>
          </div>
          
          <input
            type="text"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://gitlab.com/username/repository"
            className="input-field"
            disabled={disabled}
            required
          />
        </label>

        <button
          type="submit"
          disabled={disabled || !repoUrl.trim()}
          className="btn-primary w-full flex items-center justify-center gap-2"
        >
          <Search className="w-5 h-5" />
          {disabled ? 'Analyzing...' : 'Analyze Repository'}
        </button>

        <div className="mt-4 text-sm text-gray-400">
          <p className="mb-2">💡 <strong>Example repositories to try:</strong></p>
          <ul className="space-y-1 ml-6">
            <li>• https://gitlab.com/gitlab-org/gitlab</li>
            <li>• https://gitlab.com/inkscape/inkscape</li>
            <li>• Any public GitLab repository</li>
          </ul>
        </div>
      </form>
    </div>
  )
}