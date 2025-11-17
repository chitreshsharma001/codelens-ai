import { Brain, FileText, TrendingUp, Zap } from 'lucide-react'

export default function Hero() {
  return (
    <div className="text-center mb-16 animate-fade-in">
      <h2 className="text-5xl md:text-6xl font-bold mb-6">
        AI-Powered Repository
        <br />
        <span className="gradient-text">Analysis & Documentation</span>
      </h2>
      
      <p className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
        Instantly analyze any GitLab repository with advanced AI. Get comprehensive 
        insights, automated documentation, and actionable improvement suggestions.
      </p>

      {/* Features Grid */}
      <div className="grid md:grid-cols-4 gap-6 max-w-5xl mx-auto mt-12">
        <div className="card hover:border-gitlab-orange transition-all cursor-pointer">
          <Brain className="w-10 h-10 text-gitlab-orange mb-4 mx-auto" />
          <h3 className="font-bold mb-2">AI Analysis</h3>
          <p className="text-sm text-gray-400">
            Deep code analysis powered by Claude AI
          </p>
        </div>

        <div className="card hover:border-gitlab-purple transition-all cursor-pointer">
          <FileText className="w-10 h-10 text-gitlab-purple mb-4 mx-auto" />
          <h3 className="font-bold mb-2">Auto Docs</h3>
          <p className="text-sm text-gray-400">
            Generate comprehensive documentation instantly
          </p>
        </div>

        <div className="card hover:border-gitlab-orange transition-all cursor-pointer">
          <TrendingUp className="w-10 h-10 text-gitlab-orange mb-4 mx-auto" />
          <h3 className="font-bold mb-2">Insights</h3>
          <p className="text-sm text-gray-400">
            Get actionable improvement suggestions
          </p>
        </div>

        <div className="card hover:border-gitlab-purple transition-all cursor-pointer">
          <Zap className="w-10 h-10 text-gitlab-purple mb-4 mx-auto" />
          <h3 className="font-bold mb-2">Fast</h3>
          <p className="text-sm text-gray-400">
            Results in seconds, not hours
          </p>
        </div>
      </div>
    </div>
  )
}