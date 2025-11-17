import { useState } from 'react'
import { 
  CheckCircle, Code, FileText, Lightbulb, Star, GitFork, 
  Calendar, ExternalLink, TrendingUp, AlertCircle, Download
} from 'lucide-react'

export default function ResultsDisplay({ results }) {
  const [activeTab, setActiveTab] = useState('overview')

  const { repository, analysis, documentation, suggestions } = results

  const tabs = [
    { id: 'overview', label: 'Overview', icon: CheckCircle },
    { id: 'analysis', label: 'Analysis', icon: Code },
    { id: 'docs', label: 'Documentation', icon: FileText },
    { id: 'suggestions', label: 'Suggestions', icon: Lightbulb },
  ]

  const priorityColors = {
    High: 'text-red-400 bg-red-900 bg-opacity-30 border-red-700',
    Medium: 'text-yellow-400 bg-yellow-900 bg-opacity-30 border-yellow-700',
    Low: 'text-green-400 bg-green-900 bg-opacity-30 border-green-700',
  }

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      {/* Repository Header */}
      <div className="card mb-8">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-3xl font-bold mb-2">{repository.name}</h2>
            <p className="text-gray-400">{repository.description}</p>
          </div>
          <a 
            href={repository.web_url || '#'} 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-gitlab-orange hover:text-gitlab-purple transition-colors"
          >
            <ExternalLink className="w-6 h-6" />
          </a>
        </div>

        <div className="flex flex-wrap gap-4 text-sm text-gray-400">
          <div className="flex items-center gap-2">
            <Star className="w-4 h-4" />
            <span>{repository.stars} stars</span>
          </div>
          <div className="flex items-center gap-2">
            <GitFork className="w-4 h-4" />
            <span>{repository.forks} forks</span>
          </div>
          <div className="flex items-center gap-2">
            <Code className="w-4 h-4" />
            <span>{repository.language}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {tabs.map((tab) => {
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-gitlab-orange to-gitlab-purple text-white'
                  : 'bg-gray-800 bg-opacity-50 text-gray-400 hover:text-white'
              }`}
            >
              <Icon className="w-5 h-5" />
              {tab.label}
            </button>
          )
        })}
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {/* Overview Tab */}
        {activeTab === 'overview' && analysis && (
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <TrendingUp className="w-6 h-6 text-gitlab-orange" />
                Project Overview
              </h3>
              <p className="text-gray-300 leading-relaxed">{analysis.overview}</p>
            </div>

            <div className="card">
              <h3 className="text-xl font-bold mb-4">Code Quality Assessment</h3>
              <p className="text-gray-300 leading-relaxed">{analysis.code_quality}</p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="card">
                <h3 className="text-xl font-bold mb-4 text-green-400">Strengths</h3>
                <ul className="space-y-2">
                  {analysis.strengths && analysis.strengths.map((strength, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-300">{strength}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="card">
                <h3 className="text-xl font-bold mb-4 text-yellow-400">Areas for Improvement</h3>
                <ul className="space-y-2">
                  {analysis.areas_for_improvement && analysis.areas_for_improvement.map((area, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <AlertCircle className="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-300">{area}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="card">
              <h3 className="text-xl font-bold mb-4">Technology Stack</h3>
              <div className="flex flex-wrap gap-2">
                {analysis.tech_stack && analysis.tech_stack.map((tech, i) => (
                  <span 
                    key={i}
                    className="px-4 py-2 bg-gitlab-purple bg-opacity-20 border border-gitlab-purple rounded-lg text-sm"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            <div className="card">
              <h3 className="text-xl font-bold mb-4">Complexity Score</h3>
              <p className="text-gray-300 leading-relaxed">{analysis.complexity_score}</p>
            </div>
          </div>
        )}

        {/* Analysis Tab */}
        {activeTab === 'analysis' && analysis && (
          <div className="card">
            <h3 className="text-2xl font-bold mb-6 gradient-text">Detailed Analysis</h3>
            <div className="space-y-6">
              <div>
                <h4 className="text-lg font-semibold mb-2 text-gitlab-orange">Overview</h4>
                <p className="text-gray-300 leading-relaxed">{analysis.overview}</p>
              </div>
              <div>
                <h4 className="text-lg font-semibold mb-2 text-gitlab-orange">Code Quality</h4>
                <p className="text-gray-300 leading-relaxed">{analysis.code_quality}</p>
              </div>
              <div>
                <h4 className="text-lg font-semibold mb-2 text-gitlab-orange">Complexity</h4>
                <p className="text-gray-300 leading-relaxed">{analysis.complexity_score}</p>
              </div>
            </div>
          </div>
        )}

        {/* Documentation Tab */}
        {activeTab === 'docs' && documentation && (
          <div className="space-y-6">
            {Object.entries(documentation).map(([key, value]) => (
              <div key={key} className="card">
                <h3 className="text-xl font-bold mb-4 capitalize">
                  {key.replace(/_/g, ' ')}
                </h3>
                <p className="text-gray-300 leading-relaxed whitespace-pre-wrap">{value}</p>
              </div>
            ))}
          </div>
        )}

        {/* Suggestions Tab */}
        {activeTab === 'suggestions' && suggestions && (
          <div className="space-y-4">
            {suggestions.map((suggestion, i) => (
              <div key={i} className={`card border-2 ${priorityColors[suggestion.priority]}`}>
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <Lightbulb className="w-6 h-6 flex-shrink-0" />
                    <h3 className="text-xl font-bold">{suggestion.title}</h3>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${priorityColors[suggestion.priority]}`}>
                    {suggestion.priority}
                  </span>
                </div>
                <p className="text-sm text-gray-400 mb-2 font-semibold">{suggestion.category}</p>
                <p className="text-gray-300 mb-3 leading-relaxed">{suggestion.description}</p>
                <div className="bg-gray-900 bg-opacity-50 p-3 rounded-lg">
                  <p className="text-sm text-gray-400">
                    <strong>Expected Impact:</strong> {suggestion.impact}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}