import { useState } from 'react'
import Hero from './components/Hero'
import AnalysisForm from './components/AnalysisForm'
import ResultsDisplay from './components/ResultsDisplay'
import LoadingSpinner from './components/LoadingSpinner'
import { GitlabIcon, Sparkles } from 'lucide-react'

function App() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleAnalyze = async (repoUrl) => {
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
      const response = await fetch(`${apiUrl}/api/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repo_url: repoUrl }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Analysis failed')
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err.message)
      console.error('Analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900 bg-opacity-50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <GitlabIcon className="w-8 h-8 text-gitlab-orange" />
            <h1 className="text-2xl font-bold gradient-text">RepoInsight AI</h1>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Sparkles className="w-4 h-4" />
            <span>Powered by Gemini AI</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        {!results && !loading && <Hero />}

        {/* Analysis Form */}
        <div className="max-w-4xl mx-auto mb-12">
          <AnalysisForm onAnalyze={handleAnalyze} disabled={loading} />
        </div>

        {/* Loading State */}
        {loading && <LoadingSpinner />}

        {/* Error State */}
        {error && (
          <div className="max-w-4xl mx-auto mb-12 animate-fade-in">
            <div className="card bg-red-900 bg-opacity-30 border-red-700">
              <h3 className="text-xl font-bold text-red-400 mb-2">Analysis Failed</h3>
              <p className="text-red-300">{error}</p>
              <p className="text-sm text-gray-400 mt-4">
                Tips: Make sure the repository is public or you've set GITLAB_TOKEN
              </p>
            </div>
          </div>
        )}

        {/* Results Display */}
        {results && !loading && <ResultsDisplay results={results} />}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 bg-gray-900 bg-opacity-50 mt-20">
        <div className="container mx-auto px-4 py-8 text-center text-gray-400">
          <p className="mb-2">Built for GitLab Hackathon Challenge 2025</p>
          <p className="text-sm">i-Hack 2025 | E-Summit, IIT Bombay</p>
          <div className="mt-4 flex items-center justify-center gap-4 text-sm">
            <a href="https://gitlab.com" target="_blank" rel="noopener noreferrer" 
               className="hover:text-gitlab-orange transition-colors">
              GitLab
            </a>
            <span>•</span>
            <a href="https://zenyukti.in" target="_blank" rel="noopener noreferrer"
               className="hover:text-gitlab-purple transition-colors">
                Team ZenYukti
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App