import { useState } from 'react'
import Hero from './components/Hero'
import AnalysisForm from './components/AnalysisForm'
import ResultsDisplay from './components/ResultsDisplay'
import LoadingSpinner from './components/LoadingSpinner'
import { Sparkles } from 'lucide-react'

function App() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [theme, setTheme] = useState('dark')

  const handleAnalyze = async (repoUrl) => {
    console.log('Starting analysis for:', repoUrl)
    setLoading(true)
    setError(null)
    setResults(null)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'https://codelens-ai.onrender.com'
      console.log('API URL:', apiUrl)
      const response = await fetch(`${apiUrl}/api/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repo_url: repoUrl }),
      })
      console.log('Response status:', response.status)
      if (!response.ok) {
        const errorData = await response.json()
        if (errorData.tips || errorData.message) {
          throw errorData
        }
        throw new Error(errorData.error || 'Analysis failed')
      }
      const data = await response.json()
      console.log('Analysis complete:', data)
      setResults(data)

      try {
        const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]')
        history.unshift({
          repoUrl,
          data,
          date: new Date().toISOString(),
        })
        localStorage.setItem('analysisHistory', JSON.stringify(history.slice(0, 10)))
      } catch (historyErr) {
        console.error('Could not save analysis to history:', historyErr)
      }

    } catch (err) {
      console.error('Analysis error:', err)
      setError(err.error ? err : err.message)
    } finally {
      setLoading(false)
    }
  }

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'))
  }

  return (
    <div className={`min-h-screen ${theme}`}>
      <header className="border-b border-gray-800 bg-gray-900 bg-opacity-50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src="/codelens-logo.png" alt="CodeLens AI" className="w-8 h-8" />
            <h1 className="text-2xl font-bold gradient-text">CodeLens AI</h1>
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-400">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              <span>Powered by Gemini AI</span>
            </div>
            <button
              onClick={toggleTheme}
              className="text-sm px-3 py-1 rounded-full border border-gray-700 hover:bg-gray-800 transition-colors"
            >
              {theme === 'dark' ? '☀️ Light' : '🌙 Dark'}
            </button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        {!results && !loading && <Hero />}

        <div className="max-w-4xl mx-auto mb-12">
          <AnalysisForm onAnalyze={handleAnalyze} disabled={loading} />
        </div>

        {loading && <LoadingSpinner />}

        {error && (
          <div className="max-w-4xl mx-auto mb-12 animate-fade-in">
            <div className="card bg-red-900 bg-opacity-30 border-red-700">
              <h3 className="text-xl font-bold text-red-400 mb-3">
                {typeof error === 'object' && error.error === 'GitLab rate limit exceeded'
                  ? '⏱️ Rate Limit Reached'
                  : '⚠️ Error'}
              </h3>
              <p className="text-gray-300">
                {typeof error === 'object' ? (error.message || error.error) : error}
              </p>
              {typeof error === 'object' && error.tips && (
                <ul className="mt-3 list-disc list-inside text-sm text-gray-400 space-y-1">
                  {error.tips.map((tip, i) => (
                    <li key={i}>{tip}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}

        {results && !loading && (
          <ResultsDisplay results={results} />
        )}
      </main>
    </div>
  )
}

export default App