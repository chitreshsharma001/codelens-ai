import { useState, useEffect } from 'react'
import { Loader2, Brain, FileText, Lightbulb, CheckCircle } from 'lucide-react'

export default function LoadingSpinner() {
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState(0)
  
  const steps = [
    { icon: Brain, text: 'Fetching repository data from GitLab API...', duration: 3000 },
    { icon: FileText, text: 'Running AI analysis on code structure...', duration: 12000 },
    { icon: Lightbulb, text: 'Generating documentation and insights...', duration: 10000 }
  ]

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress(prev => {
        if (prev >= 95) return prev
        return prev + 1
      })
    }, 250)

    const stepTimer = setInterval(() => {
      setCurrentStep(prev => (prev < steps.length - 1 ? prev + 1 : prev))
    }, 8000)

    return () => {
      clearInterval(timer)
      clearInterval(stepTimer)
    }
  }, [])

  return (
    <div className="max-w-2xl mx-auto text-center animate-fade-in">
      <div className="card">
        <div className="flex justify-center mb-6">
          <Loader2 className="w-16 h-16 text-gitlab-orange animate-spin" />
        </div>
        
        <h3 className="text-2xl font-bold mb-4 gradient-text">
          Analyzing Repository...
        </h3>
        
        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-400 mb-2">
            <span>Progress</span>
            <span>{progress}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2.5 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-gitlab-orange to-gitlab-purple h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
        
        <div className="space-y-4 text-left max-w-md mx-auto">
          {steps.map((step, index) => {
            const Icon = step.icon
            const isActive = index === currentStep
            const isComplete = index < currentStep
            
            return (
              <div 
                key={index}
                className={`flex items-center gap-3 transition-all duration-300 ${
                  isActive ? 'text-gray-100 scale-105' : isComplete ? 'text-green-400' : 'text-gray-500'
                }`}
              >
                {isComplete ? (
                  <CheckCircle className="w-5 h-5 flex-shrink-0" />
                ) : (
                  <Icon className={`w-5 h-5 flex-shrink-0 ${isActive ? 'animate-pulse' : ''}`} />
                )}
                <span className="font-medium">{step.text}</span>
              </div>
            )
          })}
        </div>

        <div className="mt-6 space-y-2">
          <p className="text-sm text-gray-400">
            ⏱️ Estimated time: 15-30 seconds
          </p>
          <p className="text-xs text-gray-500">
            Powered by Gemini AI • Processing your repository data securely
          </p>
        </div>
      </div>
    </div>
  )
}