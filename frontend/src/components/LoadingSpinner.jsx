import { Loader2, Brain, FileText, Lightbulb } from 'lucide-react'

export default function LoadingSpinner() {
  return (
    <div className="max-w-2xl mx-auto text-center animate-fade-in">
      <div className="card">
        <div className="flex justify-center mb-6">
          <Loader2 className="w-16 h-16 text-gitlab-orange animate-spin" />
        </div>
        
        <h3 className="text-2xl font-bold mb-4 gradient-text">
          Analyzing Repository...
        </h3>
        
        <div className="space-y-4 text-left max-w-md mx-auto">
          <div className="flex items-center gap-3 text-gray-300">
            <Brain className="w-5 h-5 text-gitlab-orange flex-shrink-0" />
            <span>Fetching repository data from GitLab API...</span>
          </div>
          
          <div className="flex items-center gap-3 text-gray-300">
            <FileText className="w-5 h-5 text-gitlab-purple flex-shrink-0" />
            <span>Running AI analysis on code structure...</span>
          </div>
          
          <div className="flex items-center gap-3 text-gray-300">
            <Lightbulb className="w-5 h-5 text-gitlab-orange flex-shrink-0" />
            <span>Generating insights and suggestions...</span>
          </div>
        </div>

        <p className="text-sm text-gray-400 mt-6">
          This may take 15-30 seconds depending on repository size
        </p>
      </div>
    </div>
  )
}