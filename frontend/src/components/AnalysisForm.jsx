import { useState } from 'react'
import { Search, GitBranch, Zap } from 'lucide-react'

export default function AnalysisForm({ onAnalyze, disabled }) {
  const [repoUrl, setRepoUrl] = useState('')
  const [urlError, setUrlError] = useState('')

  const DEMO_REPO = 'https://gitlab.com/ayushHardeniya/repoinsight-ai'

  const validateGitLabUrl = (url) => {
    const gitlabPattern = /^https:\/\/gitlab\.com\/[\w-]+\/[\w-]+/i
    return gitlabPattern.test(url)
  }

  const handleUrlChange = (e) => {
    const url = e.target.value
    setRepoUrl(url)
    if (url && !validateGitLabUrl(url)) {
      setUrlError('Please enter a valid GitLab repository URL')
    } else {
      setUrlError('')
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (repoUrl.trim() && !urlError) {
      onAnalyze(repoUrl.trim())
    }
  }

  const handleDemoClick = () => {
    setRepoUrl(DEMO_REPO)
    setUrlError('')
    onAnalyze(DEMO_REPO)
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
            onChange={handleUrlChange}
            placeholder="https://gitlab.com/username/repository"
            className={`input-field ${urlError ? 'border-red-500' : ''}`}
            disabled={disabled}
            required
          />
          {urlError && (
            <p className="text-red-400 text-sm mt-1">{urlError}</p>
          )}
        </label>

        <div className="grid grid-cols-2 gap-3 mb-4">
          <button
            type="submit"
            disabled={disabled || !repoUrl.trim() || !!urlError}
            className="btn-primary flex items-center justify-center gap-2"
          >
            <Search className="w-5 h-5" />
            {disabled ? 'Analyzing...' : 'Analyze'}
          </button>
          
          <button
            type="button"
            onClick={handleDemoClick}
            disabled={disabled}
            className="px-6 py-3 rounded-lg font-semibold bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white transition-all duration-200 disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <Zap className="w-5 h-5" />
            Try Demo
          </button>
        </div>

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