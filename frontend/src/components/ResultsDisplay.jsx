import { useState } from 'react'
import { 
  CheckCircle, Code, FileText, Lightbulb, Star, GitFork, 
  Calendar, ExternalLink, TrendingUp, AlertCircle, Download
} from 'lucide-react'

export default function ResultsDisplay({ results }) {
  const [activeTab, setActiveTab] = useState('overview')

  if (!results) return null

  const { repository, analysis, documentation } = results
  const suggestions = analysis?.suggestions || []

  // Debug: Log the data to console
  console.log('Repository:', repository)
  console.log('Analysis overview:', analysis?.overview)
  console.log('Tech stack from AI:', analysis?.overview?.tech_stack)
  console.log('Languages from GitLab:', repository?.languages)

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
            href={repository.url || repository.web_url || '#'} 
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
            <span>{repository.stars || 0} stars</span>
          </div>
          <div className="flex items-center gap-2">
            <GitFork className="w-4 h-4" />
            <span>{repository.forks || 0} forks</span>
          </div>
          {repository.languages && Object.keys(repository.languages).length > 0 && (
            <div className="flex items-center gap-2">
              <Code className="w-4 h-4" />
              <span>{Object.keys(repository.languages)[0]}</span>
            </div>
          )}
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
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-300 mb-2">Summary</h4>
                  <p className="text-gray-400 leading-relaxed">{analysis.overview?.summary?.substring(0, 200)}...</p>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-300 mb-2">Project Type</h4>
                  <p className="text-gray-400">{analysis.overview?.project_type}</p>
                </div>
                {analysis.overview?.tech_stack && (
                  <div>
                    <h4 className="font-semibold text-gray-300 mb-2">Tech Stack</h4>
                    <div className="flex flex-wrap gap-2">
                      {analysis.overview.tech_stack.slice(0, 8).map((tech, idx) => (
                        <span key={idx} className="px-3 py-1 bg-gray-700 rounded-full text-sm text-gray-300">
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="card">
              <h3 className="text-xl font-bold mb-4">Code Quality Assessment</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-300 font-semibold">Quality Score</span>
                  <span className="text-3xl font-bold text-green-400">{analysis.code_quality?.score}/10</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-gitlab-orange to-gitlab-purple h-3 rounded-full transition-all"
                    style={{ width: `${(analysis.code_quality?.score || 0) * 10}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {(analysis.code_quality?.strengths || analysis.code_quality?.weaknesses) && (
              <div className="grid md:grid-cols-2 gap-6">
                {analysis.code_quality?.strengths && (
                  <div className="card">
                    <h3 className="text-lg font-bold mb-3 text-green-400 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5" />
                      Strengths
                    </h3>
                    <ul className="space-y-2.5">
                      {analysis.code_quality.strengths.slice(0, 5).map((strength, i) => (
                        <li key={i} className="flex items-start gap-2.5">
                          <span className="text-green-400 text-lg leading-none">•</span>
                          <span className="text-base text-gray-300 leading-relaxed">{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {analysis.code_quality?.weaknesses && (
                  <div className="card">
                    <h3 className="text-lg font-bold mb-3 text-yellow-400 flex items-center gap-2">
                      <AlertCircle className="w-5 h-5" />
                      Areas for Improvement
                    </h3>
                    <ul className="space-y-2.5">
                      {analysis.code_quality.weaknesses.slice(0, 5).map((area, i) => (
                        <li key={i} className="flex items-start gap-2.5">
                          <span className="text-yellow-400 text-lg leading-none">•</span>
                          <span className="text-base text-gray-300 leading-relaxed">{area}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            <div className="card">
              <h3 className="text-xl font-bold mb-4">Technology Stack</h3>
              <div className="flex flex-wrap gap-2">
                {analysis.overview?.tech_stack && analysis.overview.tech_stack.length > 0 ? (
                  analysis.overview.tech_stack.map((tech, i) => (
                    <span 
                      key={i}
                      className="px-4 py-2 bg-gitlab-purple bg-opacity-20 border border-gitlab-purple rounded-lg text-sm"
                    >
                      {tech}
                    </span>
                  ))
                ) : repository?.languages && Object.keys(repository.languages).length > 0 ? (
                  Object.keys(repository.languages).map((lang, i) => (
                    <span 
                      key={i}
                      className="px-4 py-2 bg-gitlab-purple bg-opacity-20 border border-gitlab-purple rounded-lg text-sm"
                    >
                      {lang}
                    </span>
                  ))
                ) : (
                  <p className="text-gray-400">Unable to detect technology stack</p>
                )}
              </div>
            </div>

            {analysis.complexity && (
              <div className="card">
                <h3 className="text-xl font-bold mb-4">Complexity Analysis</h3>
                <div className="space-y-4">
                  {analysis.complexity?.score && (
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-gray-300 font-semibold">Complexity Score</span>
                      <span className="text-3xl font-bold text-blue-400">{analysis.complexity.score}/10</span>
                    </div>
                  )}
                  {analysis.complexity?.explanation && (
                    <div>
                      <h4 className="font-semibold text-gray-300 mb-2">Explanation</h4>
                      <p className="text-gray-400 leading-relaxed">{analysis.complexity.explanation.substring(0, 150)}...</p>
                    </div>
                  )}
                  {analysis.complexity?.factors && (
                    <div>
                      <h4 className="font-semibold text-gray-300 mb-2">Complexity Factors</h4>
                      <ul className="list-disc list-inside space-y-1 text-gray-400">
                        {analysis.complexity.factors.slice(0, 3).map((factor, idx) => (
                          <li key={idx}>{factor}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Analysis Tab */}
        {activeTab === 'analysis' && analysis && (
          <div className="space-y-6">
            {/* Architecture Card */}
            <div className="card">
              <h3 className="text-xl font-bold mb-4 gradient-text flex items-center gap-2">
                <Code className="w-5 h-5" />
                Architecture
              </h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-6">
                  {analysis.architecture?.pattern && (
                    <div>
                      <div className="text-sm font-semibold text-gray-400 mb-2">PATTERN</div>
                      <span className="inline-block px-4 py-2 bg-purple-900/30 border border-purple-500 rounded-lg text-base text-purple-300">
                        {analysis.architecture.pattern}
                      </span>
                    </div>
                  )}
                  {analysis.architecture?.components && analysis.architecture.components.length > 0 && (
                    <div>
                      <div className="text-sm font-semibold text-gray-400 mb-3">KEY COMPONENTS</div>
                      <div className="space-y-3">
                        {analysis.architecture.components.slice(0, 6).map((component, idx) => (
                          <div key={idx} className="flex items-start gap-3">
                            <CheckCircle className="w-4 h-4 text-purple-400 mt-1 flex-shrink-0" />
                            <span className="text-base text-gray-300 leading-relaxed">{component}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
                {analysis.architecture?.structure && (
                  <div>
                    <div className="text-sm font-semibold text-gray-400 mb-3">OVERVIEW</div>
                    <p className="text-base text-gray-300 leading-relaxed">
                      {analysis.architecture.structure}
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Quality Card */}
              <div className="card">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 bg-green-900/30 rounded-lg">
                    <CheckCircle className="w-6 h-6 text-green-400" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-400">Code Quality</div>
                    <div className="text-3xl font-bold text-green-400">{analysis.code_quality?.score || 0}<span className="text-lg text-gray-500">/10</span></div>
                  </div>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2 mb-3">
                  <div 
                    className="bg-gradient-to-r from-green-500 to-green-400 h-2 rounded-full transition-all"
                    style={{ width: `${(analysis.code_quality?.score || 0) * 10}%` }}
                  ></div>
                </div>
                {analysis.code_quality?.assessment && (
                  <p className="text-sm text-gray-300 leading-relaxed mt-3 pt-3 border-t border-gray-700">
                    {analysis.code_quality.assessment}
                  </p>
                )}
              </div>

              {/* Complexity Card */}
              <div className="card">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 bg-blue-900/30 rounded-lg">
                    <TrendingUp className="w-6 h-6 text-blue-400" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-400">Complexity</div>
                    <div className="text-3xl font-bold text-blue-400">{analysis.complexity?.score || 0}<span className="text-lg text-gray-500">/10</span></div>
                  </div>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2 mb-3">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-blue-400 h-2 rounded-full transition-all"
                    style={{ width: `${(analysis.complexity?.score || 0) * 10}%` }}
                  ></div>
                </div>
                {analysis.complexity?.explanation && (
                  <p className="text-sm text-gray-300 leading-relaxed mt-3 pt-3 border-t border-gray-700">
                    {analysis.complexity.explanation}
                  </p>
                )}
              </div>
            </div>

            {/* Complexity Factors */}
            {analysis.complexity?.factors && analysis.complexity.factors.length > 0 && (
              <div className="card">
                <h4 className="text-lg font-bold mb-4 text-blue-400">Complexity Factors</h4>
                <div className="grid md:grid-cols-2 gap-4">
                  {analysis.complexity.factors.slice(0, 6).map((factor, idx) => (
                    <div key={idx} className="flex items-start gap-3 p-4 bg-gray-800/50 rounded-lg">
                      <AlertCircle className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                      <span className="text-base text-gray-300 leading-relaxed">{factor}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Documentation Tab */}
        {activeTab === 'docs' && documentation && (
          <div className="space-y-6">
            {/* README Section */}
            {documentation.readme && (
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-2xl font-bold gradient-text">📄 README</h3>
                  <button 
                    onClick={() => {
                      const blob = new Blob([documentation.readme.content || ''], { type: 'text/markdown' });
                      const url = URL.createObjectURL(blob);
                      const a = document.createElement('a');
                      a.href = url;
                      a.download = 'README.md';
                      a.click();
                    }}
                    className="flex items-center gap-2 px-4 py-2 bg-gitlab-orange hover:bg-gitlab-purple transition-colors rounded-lg"
                  >
                    <Download className="w-4 h-4" />
                    Download README.md
                  </button>
                </div>
                {documentation.readme.description && (
                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-300 mb-2">Description</h4>
                    <p className="text-gray-400 leading-relaxed whitespace-pre-line">{documentation.readme.description}</p>
                  </div>
                )}
                {documentation.readme.features && (
                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-300 mb-2">Key Features</h4>
                    <ul className="list-disc list-inside space-y-1 text-gray-400">
                      {documentation.readme.features.map((feature, idx) => (
                        <li key={idx}>{feature}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {documentation.readme.content && (
                  <div>
                    <h4 className="font-semibold text-gray-300 mb-2">Full Content</h4>
                    <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm text-gray-300 whitespace-pre-wrap">
                      {documentation.readme.content}
                    </pre>
                  </div>
                )}
              </div>
            )}

            {/* Getting Started Section */}
            {documentation.getting_started && (
              <div className="card">
                <h3 className="text-2xl font-bold mb-4 gradient-text">🚀 Getting Started</h3>
                <div className="space-y-4">
                  {documentation.getting_started.prerequisites && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">Prerequisites</h4>
                      <ul className="list-disc list-inside space-y-1 text-gray-300">
                        {documentation.getting_started.prerequisites.map((req, idx) => (
                          <li key={idx}>{req}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {documentation.getting_started.installation && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">Installation Steps</h4>
                      <ol className="list-decimal list-inside space-y-1 text-gray-300">
                        {documentation.getting_started.installation.map((step, idx) => (
                          <li key={idx}>{step}</li>
                        ))}
                      </ol>
                    </div>
                  )}
                  {documentation.getting_started.quick_start && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">Quick Start</h4>
                      <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm text-gray-300 whitespace-pre-wrap">
                        {documentation.getting_started.quick_start}
                      </pre>
                    </div>
                  )}
                  {documentation.getting_started.configuration && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">Configuration</h4>
                      <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm text-gray-300 whitespace-pre-wrap">
                        {documentation.getting_started.configuration}
                      </pre>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* API Endpoints Section */}
            {documentation.api_endpoints && documentation.api_endpoints.available && (
              <div className="card">
                <h3 className="text-2xl font-bold mb-4 gradient-text">🔌 API Endpoints</h3>
                <div className="space-y-4">
                  {documentation.api_endpoints.endpoints && documentation.api_endpoints.endpoints.map((endpoint, idx) => (
                    <div key={idx} className="p-4 bg-gray-800 rounded-lg">
                      <div className="flex items-center gap-3 mb-2">
                        <span className={`px-3 py-1 rounded font-mono text-sm ${
                          endpoint.method === 'GET' ? 'bg-green-900 text-green-300' :
                          endpoint.method === 'POST' ? 'bg-blue-900 text-blue-300' :
                          endpoint.method === 'PUT' ? 'bg-yellow-900 text-yellow-300' :
                          'bg-red-900 text-red-300'
                        }`}>
                          {endpoint.method}
                        </span>
                        <span className="font-mono text-gray-300">{endpoint.path}</span>
                      </div>
                      <p className="text-gray-400 mb-2">{endpoint.description}</p>
                      {endpoint.parameters && (
                        <div className="mb-2">
                          <span className="text-sm font-semibold text-gray-400">Parameters:</span>
                          <pre className="mt-1 text-xs text-gray-500">{JSON.stringify(endpoint.parameters, null, 2)}</pre>
                        </div>
                      )}
                      {endpoint.example && (
                        <div>
                          <span className="text-sm font-semibold text-gray-400">Example:</span>
                          <pre className="mt-1 bg-gray-900 p-2 rounded text-xs text-gray-300 overflow-x-auto">
                            {endpoint.example}
                          </pre>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Architecture Section */}
            {documentation.architecture && (
              <div className="card">
                <h3 className="text-2xl font-bold mb-4 gradient-text">🏗️ Architecture</h3>
                <div className="space-y-4">
                  {documentation.architecture.overview && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">Overview</h4>
                      <p className="text-gray-300 leading-relaxed whitespace-pre-line">{documentation.architecture.overview}</p>
                    </div>
                  )}
                  {documentation.architecture.diagram && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">System Diagram</h4>
                      <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm text-gray-300">
                        {documentation.architecture.diagram}
                      </pre>
                    </div>
                  )}
                  {documentation.architecture.technologies && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">Technologies</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {Object.entries(documentation.architecture.technologies).map(([category, tech]) => (
                          <div key={category} className="p-3 bg-gray-800 rounded">
                            <div className="font-semibold text-gray-300 mb-1">{category}</div>
                            <div className="text-sm text-gray-400">{tech}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  {documentation.architecture.folder_structure && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">Folder Structure</h4>
                      <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm text-gray-300 whitespace-pre-wrap">
                        {documentation.architecture.folder_structure}
                      </pre>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Contributing Section */}
            {documentation.contributing && (
              <div className="card">
                <h3 className="text-2xl font-bold mb-4 gradient-text">🤝 Contributing</h3>
                <div className="space-y-4">
                  {documentation.contributing.guidelines && (
                    <div>
                      <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm text-gray-300 whitespace-pre-wrap">
                        {documentation.contributing.guidelines}
                      </pre>
                    </div>
                  )}
                  {documentation.contributing.code_style && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">Code Style</h4>
                      <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm text-gray-300 whitespace-pre-wrap">
                        {documentation.contributing.code_style}
                      </pre>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Usage Section */}
            {documentation.usage && (
              <div className="card">
                <h3 className="text-2xl font-bold mb-4 gradient-text">📖 Usage Guide</h3>
                <div className="space-y-4">
                  {documentation.usage.basic_usage && (
                    <div>
                      <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm text-gray-300 whitespace-pre-wrap">
                        {documentation.usage.basic_usage}
                      </pre>
                    </div>
                  )}
                  {documentation.usage.examples && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">Examples</h4>
                      <div className="space-y-3">
                        {documentation.usage.examples.map((example, idx) => (
                          <pre key={idx} className="bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm text-gray-300 whitespace-pre-wrap">
                            {example}
                          </pre>
                        ))}
                      </div>
                    </div>
                  )}
                  {documentation.usage.common_tasks && (
                    <div>
                      <h4 className="font-semibold text-gitlab-orange mb-2">Common Tasks</h4>
                      <div className="space-y-4">
                        {documentation.usage.common_tasks.map((task, idx) => (
                          <div key={idx} className="p-4 bg-gray-800 rounded-lg">
                            <h5 className="font-semibold text-gray-300 mb-2">{task.task}</h5>
                            {task.steps && (
                              <ol className="list-decimal list-inside space-y-1 text-gray-400 mb-2">
                                {task.steps.map((step, stepIdx) => (
                                  <li key={stepIdx}>{step}</li>
                                ))}
                              </ol>
                            )}
                            {task.code && (
                              <pre className="bg-gray-900 p-3 rounded text-xs text-gray-300 overflow-x-auto">
                                {task.code}
                              </pre>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
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