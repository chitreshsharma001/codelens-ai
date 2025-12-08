import google.generativeai as genai
import os
import json
import re

class AIService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-flash-lite-latest')
    
    def analyze_repository(self, repo_data):
        """Generate comprehensive repository analysis using Gemini"""
        
        # Prepare context for AI
        context = self._prepare_context(repo_data)
        
        # Generate detailed analysis
        analysis_prompt = f"""
You are an expert code analyst. Analyze this GitLab repository and provide a DETAILED, COMPREHENSIVE analysis.

Repository Information:
{context}

Provide a thorough analysis in the following JSON format:
{{
    "overview": {{
        "summary": "Write 2-3 detailed paragraphs explaining what this project does, its main purpose, and key features. Be specific about the technology and functionality.",
        "purpose": "Explain what specific problem this project solves and who would use it",
        "tech_stack": ["List all technologies, frameworks, and tools used"],
        "project_type": "Categorize as: web application / REST API / library / CLI tool / microservice / mobile app / etc"
    }},
    "code_quality": {{
        "score": 7,
        "strengths": ["Clear, plain English strength point 1 without special characters", "Clear strength point 2", "Clear strength point 3", "Clear strength point 4"],
        "weaknesses": ["Clear area for improvement 1 in plain language", "Clear area for improvement 2", "Clear area for improvement 3", "Clear area for improvement 4"],
        "assessment": "2-3 concise sentences in plain English summarizing code quality. Do NOT use backticks, slashes, or technical symbols."
    }},
    "complexity": {{
        "score": 6,
        "factors": ["Complexity factor 1", "Complexity factor 2", "Complexity factor 3", "Complexity factor 4"],
        "explanation": "2-3 concise sentences explaining the complexity level and key challenges"
    }},
    "architecture": {{
        "pattern": "Identify the exact architectural pattern: MVC / MVVM / Microservices / Monolith / Layered / Client-Server / etc",
        "structure": "Write 1-2 clear, concise sentences describing the overall project organization and key architectural decisions. Focus on the big picture, avoid mentioning specific file names.",
        "components": ["Component 1: Brief description", "Component 2: Brief description", "Component 3: Brief description"]
    }},
    "suggestions": [
        {{
            "category": "Security",
            "priority": "High",
            "title": "Specific, actionable suggestion title",
            "description": "Detailed explanation of the issue or improvement needed",
            "implementation": "Step-by-step guide on how to implement this suggestion",
            "impact": "Explain the expected benefits and impact of implementing this"
        }},
        {{
            "category": "Testing",
            "priority": "High",
            "title": "Another specific suggestion",
            "description": "Detailed description",
            "implementation": "How to do it",
            "impact": "Why it matters"
        }},
        {{
            "category": "Performance",
            "priority": "Medium",
            "title": "Performance improvement",
            "description": "What needs optimization",
            "implementation": "How to optimize",
            "impact": "Expected performance gains"
        }},
        {{
            "category": "Documentation",
            "priority": "Medium",
            "title": "Documentation improvement",
            "description": "What documentation is missing",
            "implementation": "What to document",
            "impact": "Improved developer experience"
        }},
        {{
            "category": "Code Quality",
            "priority": "Low",
            "title": "Code refactoring suggestion",
            "description": "What could be refactored",
            "implementation": "How to refactor",
            "impact": "Better maintainability"
        }}
    ]
}}

IMPORTANT:
- Write in clear, plain English without backticks, slashes, or code symbols
- Describe features and structure in simple terms, not file paths
- Be specific but avoid technical jargon in user-facing descriptions
- Provide at least 4-5 points for strengths, weaknesses, and factors
- Focus on what the code does, not where it is located
- Keep points concise and easy to understand

OUTPUT FORMAT: Return ONLY valid JSON. No explanations before or after. Just the JSON object.
"""
        
        try:
            print("Analyzing repository with AI...")
            print(f"Using model: models/gemini-2.5-flash")
            print(f"Prompt length: {len(analysis_prompt)} chars")
            
            response = self.model.generate_content(
                analysis_prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 8192
                }
            )
            
            print(f"AI Analysis received")
            print(f"Response text length: {len(response.text)}")
            print(f"Response preview (first 200 chars): {response.text[:200]}")
            
            analysis = self._parse_ai_response(response.text)
            
            if not analysis:
                print("Failed to parse AI response, using fallback")
                print(f"Full response text: {response.text}")
                return self._get_fallback_analysis(repo_data)
            
            print("Analysis completed successfully")
            return analysis
        except Exception as e:
            print(f"Error in analysis: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return self._get_fallback_analysis(repo_data)
    def generate_documentation(self, repo_data, analysis):
        """Generate comprehensive documentation using Gemini"""
        
        context = self._prepare_context(repo_data)
        languages = list(repo_data.get('languages', {}).keys())
        primary_lang = languages[0] if languages else 'Unknown'
        
        doc_prompt = f"""Based on the following repository analysis, generate comprehensive documentation.

Repository Context:
{context}

Analysis Results:
{json.dumps(analysis, indent=2)}

Generate documentation in JSON format with the following structure:
{{
  "readme": {{
    "title": "Project Title",
    "description": "Comprehensive project description (at least 100 words)",
    "features": ["Feature 1", "Feature 2", ...],
    "content": "Full README.md content in markdown format with sections: Overview, Features, Tech Stack, Installation, Usage, Contributing"
  }},
  "getting_started": {{
    "prerequisites": ["Prerequisite 1", "Prerequisite 2"],
    "installation": ["Step 1", "Step 2"],
    "quick_start": "Quick start guide in markdown",
    "configuration": "Configuration instructions"
  }},
  "api_endpoints": {{
    "available": true/false,
    "endpoints": [
      {{"method": "GET", "path": "/api/example", "description": "Description", "example": "curl example"}}
    ]
  }},
  "architecture": {{
    "overview": "Architecture description",
    "diagram": "ASCII diagram or description",
    "technologies": {{"Category": "Technologies used"}},
    "folder_structure": "Folder structure explanation"
  }},
  "contributing": {{
    "guidelines": "Contributing guidelines in markdown",
    "code_style": "Code style guide",
    "pull_request_process": "PR process description"
  }},
  "usage": {{
    "basic_usage": "Basic usage instructions",
    "examples": ["Example 1 code", "Example 2 code"],
    "common_tasks": [
      {{"task": "Task name", "steps": ["Step 1", "Step 2"], "code": "Optional code example"}}
    ]
  }}
}}

Make the documentation specific to this {primary_lang} project. Be detailed and comprehensive.
Return ONLY valid JSON, no markdown formatting."""
        
        try:
            print("Generating comprehensive documentation with AI...")
            response = self.model.generate_content(
                doc_prompt,
                generation_config={
                    'temperature': 0.5,
                    'max_output_tokens': 4096
                }
            )
            
            print(f"AI documentation response preview: {response.text[:200]}")
            documentation = self._parse_ai_response(response.text)
            if not documentation or not documentation.get('readme'):
                print("AI response incomplete, using enhanced fallback")
                return self._get_enhanced_documentation(repo_data, analysis)
            
            print("Documentation generated successfully with AI")
            return documentation
        except Exception as e:
            print(f"Error in documentation generation: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._get_enhanced_documentation(repo_data, analysis)
    
    def _get_lang_benefits(self, lang):
        """Get language benefits description"""
        benefits = {
            'JavaScript': 'flexibility and wide ecosystem support',
            'Python': 'readability and extensive library support',
            'Java': 'robustness and enterprise-grade features',
            'TypeScript': 'type safety and modern JavaScript features',
            'Go': 'performance and simplicity',
            'Rust': 'memory safety and performance',
        }
        return benefits.get(lang, 'versatility and community support')
    
    def _prepare_context(self, repo_data):
        """Prepare repository context for AI"""
        context = f"""
Project Name: {repo_data.get('name', 'Unknown')}
Description: {repo_data.get('description', 'No description provided')}
Languages Used: {', '.join(repo_data.get('languages', {}).keys()) if repo_data.get('languages') else 'Not specified'}
Primary Language: {max(repo_data.get('languages', {'Unknown': 100}).items(), key=lambda x: x[1])[0] if repo_data.get('languages') else 'Unknown'}
Default Branch: {repo_data.get('default_branch', 'main')}
Stars: {repo_data.get('star_count', 0)}
Forks: {repo_data.get('forks_count', 0)}
Web URL: {repo_data.get('web_url', 'N/A')}
"""
        
        if 'file_tree' in repo_data and repo_data['file_tree']:
            context += f"\n\nProject File Structure:\n{self._format_file_tree(repo_data['file_tree'])}"
        
        if 'readme_content' in repo_data and repo_data['readme_content']:
            context += f"\n\nExisting README Content (first 2000 chars):\n{repo_data['readme_content'][:2000]}"
        
        return context
    
    def _format_file_tree(self, files, max_files=100):
        """Format file tree for context"""
        if not files:
            return "No files available"
        
        file_list = files[:max_files]
        formatted = []
        
        for file in file_list:
            path = file.get('path', '')
            file_type = file.get('type', 'file')
            
            if file_type == 'tree':
                formatted.append(f"📁 {path}/")
            else:
                formatted.append(f"📄 {path}")
        
        return '\n'.join(formatted)
    
    def _parse_ai_response(self, response_text):
        """Parse AI response and extract JSON"""
        try:
            # Remove markdown code blocks if present
            text = response_text.strip()
            
            # Handle various markdown formats
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                # Find first and last code block
                parts = text.split('```')
                if len(parts) >= 3:
                    text = parts[1]
            
            # Remove any remaining backticks
            text = text.strip('`').strip()
            
            # Try direct parsing first
            try:
                parsed = json.loads(text)
                print("JSON parsed successfully (direct)")
                return parsed
            except:
                pass
            
            # Try to extract JSON object using regex
            json_match = re.search(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', text, re.DOTALL)
            if json_match:
                try:
                    parsed = json.loads(json_match.group())
                    print("JSON parsed successfully (regex)")
                    return parsed
                except:
                    pass
            
            # Last resort: find largest JSON-like structure
            brace_count = 0
            start_idx = -1
            for i, char in enumerate(text):
                if char == '{':
                    if brace_count == 0:
                        start_idx = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_idx >= 0:
                        try:
                            json_str = text[start_idx:i+1]
                            parsed = json.loads(json_str)
                            print("JSON parsed successfully (brace matching)")
                            return parsed
                        except:
                            start_idx = -1
            
            print("All JSON parsing attempts failed")
            return None
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {str(e)}")
            print(f"Response preview: {response_text[:500]}")
            return None
        except Exception as e:
            print(f"Unexpected error parsing response: {str(e)}")
            return None
    
    def _get_fallback_analysis(self, repo_data=None):
        """Fallback analysis if AI fails"""
        # Use actual repository data if available
        tech_stack = ["Unable to determine"]
        if repo_data and repo_data.get('languages'):
            tech_stack = list(repo_data.get('languages', {}).keys())
        
        return {
            "overview": {
                "summary": "This repository contains a software project. Unable to generate detailed analysis at this time. Please ensure the repository is accessible and contains analyzable code.",
                "purpose": "Analysis temporarily unavailable",
                "tech_stack": tech_stack,
                "project_type": "Software Project"
            },
            "code_quality": {
                "score": 5,
                "strengths": [
                    "Repository is properly structured",
                    "Contains version-controlled code"
                ],
                "weaknesses": [
                    "Unable to perform deep code analysis",
                    "AI service temporarily unavailable"
                ],
                "assessment": "Automated analysis is temporarily unavailable. Please try again or check the repository manually."
            },
            "complexity": {
                "score": 5,
                "factors": [
                    "Analysis unavailable",
                    "Unable to determine complexity metrics"
                ],
                "explanation": "Complexity analysis could not be performed at this time."
            },
            "architecture": {
                "pattern": "To be determined",
                "structure": "Unable to analyze project structure automatically. Please review the repository manually.",
                "components": ["Analysis unavailable"]
            },
            "suggestions": [
                {
                    "category": "Documentation",
                    "priority": "High",
                    "title": "Add comprehensive README",
                    "description": "Ensure the repository has a detailed README with setup instructions and usage examples.",
                    "implementation": "Create a README.md file with project description, installation steps, and usage guide.",
                    "impact": "Improved developer onboarding and project clarity"
                }
            ]
        }
    
    def _get_install_command(self, language, command_type):
        """Get installation commands based on language"""
        commands = {
            'Python': {
                'prerequisites': 'Python 3.8+, pip',
                'install': 'pip install -r requirements.txt',
                'run': 'python app.py  # or python main.py'
            },
            'JavaScript': {
                'prerequisites': 'Node.js 14+, npm or yarn',
                'install': 'npm install',
                'run': 'npm start'
            },
            'TypeScript': {
                'prerequisites': 'Node.js 14+, npm',
                'install': 'npm install',
                'run': 'npm run dev'
            },
            'Java': {
                'prerequisites': 'JDK 11+, Maven or Gradle',
                'install': 'mvn install  # or gradle build',
                'run': 'mvn spring-boot:run'
            },
            'Go': {
                'prerequisites': 'Go 1.16+',
                'install': 'go mod download',
                'run': 'go run main.go'
            }
        }
        return commands.get(language, commands['Python']).get(command_type, 'See project docs')
    
    def _get_prerequisites_for_lang(self, language, has_docker):
        """Get prerequisites based on language"""
        prereqs = []
        if language == 'Python':
            prereqs = ['Python 3.8 or higher', 'pip package manager', 'virtualenv (recommended)']
        elif language in ['JavaScript', 'TypeScript']:
            prereqs = ['Node.js 14.x or higher', 'npm or yarn package manager']
        elif language == 'Java':
            prereqs = ['JDK 11 or higher', 'Maven or Gradle build tool']
        elif language == 'Go':
            prereqs = ['Go 1.16 or higher', 'Go modules enabled']
        else:
            prereqs = [f'{language} runtime environment', 'Package manager for {language}']
        
        if has_docker:
            prereqs.append('Docker and Docker Compose (optional)')
        
        return prereqs
    
    def _get_config_hint(self, language):
        """Get configuration hints"""
        if language == 'Python':
            return "\\nCreate .env file:\\n```\\nDATABASE_URL=your_db_url\\nAPI_KEY=your_key\\n```"
        elif language in ['JavaScript', 'TypeScript']:
            return "\\nCreate .env file:\\n```\\nREACT_APP_API_URL=http://localhost:5000\\n```"
        return "\\nCheck config files for environment variables needed"
    
    def _suggest_endpoints(self, is_api, analysis):
        """Suggest API endpoints if detected"""
        if not is_api:
            return []
        
        return [
            {
                "method": "GET",
                "path": "/api/health",
                "description": "Health check endpoint",
                "parameters": {},
                "example": "curl http://localhost:5000/api/health"
            },
            {
                "method": "POST",
                "path": "/api/analyze",
                "description": "Main analysis endpoint (detected from project structure)",
                "parameters": {"repo_url": "GitLab repository URL"},
                "example": "curl -X POST http://localhost:5000/api/analyze -H 'Content-Type: application/json' -d '{\"repo_url\":\"https://gitlab.com/user/repo\"}'"
            }
        ]
    
    def _create_architecture_diagram(self, repo_data, is_web_app, is_api):
        """Create ASCII architecture diagram"""
        if is_web_app:
            return """
┌─────────────────┐
│   React/Vue     │  Frontend
│   (Client)      │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│  Backend API    │  Server
│  (Flask/Express)│
└────┬───────┬────┘
     │       │
     │       └──────► External APIs
     │
     └──────────────► Database
"""
        elif is_api:
            return """
┌─────────────────┐
│   API Clients   │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│  API Server     │
│  (Routes)       │
└────┬───────────┘
     │
     └──────────────► Services/Database
"""
        else:
            return """
┌─────────────────┐
│  Application    │
│  Entry Point    │
└────────┬────────┘
         │
┌────────▼────────┐
│  Core Logic     │
│  & Services     │
└─────────────────┘
"""
    
    def _extract_technologies(self, repo_data, analysis):
        """Extract technologies from repo data"""
        tech = {}
        languages = repo_data.get('languages', {})
        
        # Frontend detection
        if 'JavaScript' in languages or 'TypeScript' in languages:
            tech['Frontend'] = 'React, Vite' if 'vite' in str(repo_data.get('file_tree', [])).lower() else 'JavaScript/TypeScript'
        elif 'HTML' in languages:
            tech['Frontend'] = 'HTML/CSS/JavaScript'
        
        # Backend detection
        if 'Python' in languages:
            tech['Backend'] = 'Python, Flask' if 'flask' in str(repo_data.get('file_tree', [])).lower() else 'Python'
        elif 'Java' in languages:
            tech['Backend'] = 'Java, Spring Boot' if 'spring' in str(repo_data.get('file_tree', [])).lower() else 'Java'
        elif 'Go' in languages:
            tech['Backend'] = 'Go'
        
        # DevOps detection
        file_tree_str = str(repo_data.get('file_tree', []))
        if 'Dockerfile' in file_tree_str:
            tech['DevOps'] = 'Docker, ' + ('Docker Compose, ' if 'docker-compose' in file_tree_str else '') + ('GitLab CI/CD' if '.gitlab-ci.yml' in file_tree_str else '')
        
        return tech
    
    def _get_code_style_for_lang(self, language):
        """Get code style guidelines"""
        styles = {
            'Python': '- Follow PEP 8 style guide\\n- Use type hints where applicable\\n- Write docstrings for functions\\n- Use meaningful variable names',
            'JavaScript': '- Use ESLint with recommended config\\n- Prefer const/let over var\\n- Use async/await for promises\\n- Follow Airbnb style guide',
            'TypeScript': '- Enable strict mode\\n- Define interfaces for data structures\\n- Use TypeScript features (enums, generics)\\n- Follow ESLint + TypeScript rules',
            'Java': '- Follow Google Java Style Guide\\n- Use meaningful class and method names\\n- Write Javadoc comments\\n- Follow SOLID principles'
        }
        return styles.get(language, 'Follow standard coding practices for ' + language)
    
    def _get_usage_example(self, language, is_web_app, is_api):
        """Generate usage example"""
        if is_web_app:
            return "1. Start the application\\n2. Open browser to http://localhost:3000\\n3. Use the interface to interact with features"
        elif is_api:
            return "Send requests to API endpoints:\\n```bash\\ncurl http://localhost:5000/api/endpoint\\n```"
        elif language == 'Python':
            return "```python\\nfrom main import app\\napp.run()\\n```"
        else:
            return "Run the main application file and follow on-screen instructions"
    
    def _get_code_examples(self, language, is_web_app, is_api):
        """Generate code examples"""
        examples = []
        if language == 'Python':
            examples.append("# Import and use\\nimport main\\nresult = main.function()\\nprint(result)")
        elif language in ['JavaScript', 'TypeScript']:
            examples.append("// Import and use\\nimport { function } from './module';\\nconst result = await function();\\nconsole.log(result);")
        return examples
    
    def _get_common_tasks(self, language, is_web_app):
        """Get common tasks"""
        tasks = []
        if is_web_app:
            tasks.append({"task": "Start development server", "steps": ["Run npm run dev or equivalent"], "code": "npm run dev"})
            tasks.append({"task": "Build for production", "steps": ["Run build command"], "code": "npm run build"})
        elif language == 'Python':
            tasks.append({"task": "Run application", "steps": ["Execute main file"], "code": "python app.py"})
        return tasks
    
    def _enhance_documentation(self, doc, repo_data, analysis):
        """Enhance incomplete documentation"""
        # Ensure readme has substantial content
        if doc.get('readme', {}).get('content', '').count('\\n') < 20:
            doc['readme']['content'] = self._generate_detailed_readme(repo_data, analysis)
        return doc
    
    def _generate_detailed_readme(self, repo_data, analysis, primary_lang=None, is_web_app=None, has_docker=None):
        """Generate detailed README content"""
        name = repo_data.get('name', 'Project')
        desc = repo_data.get('description', '')
        languages = repo_data.get('languages', {})
        lang_list = ', '.join(languages.keys()) if languages else 'Multiple languages'
        if primary_lang is None:
            primary_lang = list(languages.keys())[0] if languages else 'Unknown'
        url = repo_data.get('web_url', '')
        stars = repo_data.get('star_count', 0)
        forks = repo_data.get('forks_count', 0)
        
        # Detect project characteristics if not provided
        file_tree_str = str(repo_data.get('file_tree', [])).lower()
        if is_web_app is None:
            is_web_app = 'frontend' in file_tree_str or 'client' in file_tree_str
        if has_docker is None:
            has_docker = 'dockerfile' in file_tree_str or 'docker-compose' in file_tree_str
        has_backend = 'backend' in file_tree_str or 'server' in file_tree_str or 'api' in file_tree_str
        has_docker = 'dockerfile' in file_tree_str
        has_ci = '.gitlab-ci.yml' in file_tree_str or '.github' in file_tree_str
        
        # Get analysis insights
        tech_stack = analysis.get('overview', {}).get('tech_stack', []) if analysis else []
        project_type = analysis.get('overview', {}).get('project_type', 'software application') if analysis else 'software application'
        purpose = analysis.get('overview', {}).get('purpose', desc or 'various purposes') if analysis else (desc or 'various purposes')
        
        # Build comprehensive README
        readme = f"""# {name}

{'⭐ ' + str(stars) + ' Stars | ' if stars > 0 else ''}{'🔱 ' + str(forks) + ' Forks | ' if forks > 0 else ''}🌐 [View on GitLab]({url})

## 📋 Overview

**{name}** is a {'full-stack web application' if is_web_app and has_backend else 'web application' if is_web_app else 'software project'} built with **{lang_list}**. {'This project combines a modern frontend with a robust backend API architecture.' if is_web_app and has_backend else 'This repository provides comprehensive functionality for ' + purpose + '.'}

{desc if desc else f'This {project_type} leverages modern development practices and tools to deliver a reliable and maintainable solution.'}

### Key Highlights

- 🚀 **Technology Stack**: Built with {lang_list}
- {'🌐 **Full-Stack Architecture**: Separate frontend and backend services' if is_web_app and has_backend else ''}
- {'📦 **Containerized**: Docker support for easy deployment' if has_docker else ''}
- {'⚙️ **CI/CD Pipeline**: Automated testing and deployment' if has_ci else ''}
- 🔧 **Modern Development**: Following industry best practices

## ✨ Features

"""
        
        # Add features
        if tech_stack:
            for tech in tech_stack:
                readme += f"- **{tech}**: Integration and utilization\n"
        else:
            if is_web_app:
                readme += f"- **Interactive User Interface**: {'React/Vue-based' if 'javascript' in file_tree_str or 'typescript' in file_tree_str else 'Modern'} frontend\n"
            if has_backend:
                readme += f"- **RESTful API**: Backend API services for data management\n"
            if has_docker:
                readme += f"- **Docker Support**: Containerized deployment for consistency\n"
            if has_ci:
                readme += f"- **Automated CI/CD**: Continuous integration and deployment pipeline\n"
            readme += f"- **{primary_lang} Implementation**: Leveraging {primary_lang} ecosystem\n"
            readme += f"- **Version Control**: GitLab-based collaboration and code management\n"
        
        readme += f"""
## 🛠️ Technology Stack

### Languages & Frameworks
"""
        for lang, percentage in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            readme += f"- **{lang}**: {percentage:.1f}%\n"
        
        if is_web_app:
            readme += f"\n### Architecture\n"
            readme += f"- **Frontend**: {'React/Vite' if 'vite' in file_tree_str else 'Modern JavaScript/TypeScript' if 'javascript' in file_tree_str else 'Client-side application'}\n"
        if has_backend:
            readme += f"- **Backend**: {'Flask' if primary_lang == 'Python' else 'Express' if primary_lang == 'JavaScript' else 'Spring Boot' if primary_lang == 'Java' else 'API Server'}\n"
        if has_docker:
            readme += f"- **Containerization**: Docker & Docker Compose\n"
        if has_ci:
            readme += f"- **CI/CD**: GitLab CI/CD Pipeline\n"
        
        # Installation instructions
        readme += f"""
## 🚀 Getting Started

### Prerequisites

"""
        if primary_lang == 'Python':
            readme += f"""- Python 3.8 or higher
- pip package manager
- virtualenv (recommended)
"""
        elif primary_lang in ['JavaScript', 'TypeScript']:
            readme += f"""- Node.js 14.x or higher
- npm or yarn package manager
"""
        elif primary_lang == 'Java':
            readme += f"""- JDK 11 or higher
- Maven or Gradle
"""
        else:
            readme += f"""- {primary_lang} runtime environment
- Appropriate package manager
"""
        
        if has_docker:
            readme += f"- Docker and Docker Compose (optional)\n"
        
        readme += f"""
### Installation

1. **Clone the repository**
   ```bash
   git clone {url}
   cd {name}
   ```

2. **Install dependencies**
   ```bash
"""
        
        if primary_lang == 'Python':
            readme += f"   pip install -r requirements.txt\n"
        elif primary_lang in ['JavaScript', 'TypeScript']:
            readme += f"   npm install\n"
        elif primary_lang == 'Java':
            readme += f"   mvn install\n"
        else:
            readme += f"   # Follow language-specific installation steps\n"
        
        readme += f"""   ```

3. **Configure environment** (if needed)
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
"""
        
        if primary_lang == 'Python':
            readme += f"   python app.py\n"
        elif primary_lang in ['JavaScript', 'TypeScript']:
            readme += f"   npm start\n"
        elif primary_lang == 'Java':
            readme += f"   mvn spring-boot:run\n"
        else:
            readme += f"   # Follow language-specific run instructions\n"
        
        readme += f"""   ```

"""
        
        if has_docker:
            readme += f"""### Docker Deployment

```bash
docker-compose up --build
```

The application will be available at the configured port.

"""
        
        readme += f"""## 📖 Usage

{'Visit `http://localhost:3000` (or configured port) to access the application.' if is_web_app else 'Run the application and follow the on-screen instructions or API documentation.'}

For detailed API documentation and usage examples, refer to the codebase documentation.

## 🏗️ Project Structure

The project follows a {'modular architecture with separate frontend and backend services' if is_web_app and has_backend else 'structured organization for maintainability'}:

"""
        
        # Add simplified folder structure
        if is_web_app and has_backend:
            readme += f"""```
{name}/
├── frontend/          # Client-side application
├── backend/           # Server-side API
{'├── docker-compose.yml  # Container orchestration' if has_docker else ''}
{'└── .gitlab-ci.yml    # CI/CD configuration' if has_ci else ''}
```
"""
        elif is_web_app:
            readme += f"""```
{name}/
├── src/               # Source code
├── public/            # Static assets
└── package.json       # Dependencies
```
"""
        else:
            readme += f"""```
{name}/
├── src/               # Source files
├── tests/             # Test suite
└── README.md          # Documentation
```
"""
        
        readme += f"""
## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate tests.

## 📄 License

Check the repository for license information. If no license is specified, please contact the maintainers.

## 🔗 Links

- **Repository**: [{url}]({url})
- **Issues**: [{url}/-/issues]({url}/-/issues)
- **Merge Requests**: [{url}/-/merge_requests]({url}/-/merge_requests)

---

**Built with ❤️ using {lang_list}**
"""
        
        return readme
    
    def _get_enhanced_documentation(self, repo_data, analysis):
        """Get enhanced fallback documentation with real content"""
        name = repo_data.get('name', 'Project')
        url = repo_data.get('web_url', 'N/A')
        languages = list(repo_data.get('languages', {}).keys())
        primary_lang = languages[0] if languages else 'Unknown'
        
        readme_content = self._generate_detailed_readme(repo_data, analysis)
        
        return {
            "readme": {
                "title": name,
                "description": f"{name} is a {primary_lang}-based project hosted on GitLab. " + 
                              (analysis.get('overview', {}).get('summary', 'This project provides various functionality and features.') if analysis else
                               "This repository contains code and resources for the application."),
                "features": analysis.get('overview', {}).get('tech_stack', []) or [
                    f"{primary_lang} codebase",
                    "Version-controlled development",
                    "GitLab integration"
                ],
                "content": readme_content
            },
            "getting_started": {
                "prerequisites": self._get_prerequisites_for_lang(primary_lang, False),
                "installation": [
                    f"git clone {url}",
                    f"cd {name}",
                    self._get_install_command(primary_lang, 'install')
                ],
                "quick_start": f"Clone the repository and run:\\n```bash\\n{self._get_install_command(primary_lang, 'run')}\\n```",
                "configuration": self._get_config_hint(primary_lang)
            },
            "api_endpoints": {
                "available": False,
                "endpoints": []
            },
            "architecture": {
                "overview": f"This {primary_lang} project is organized with standard directory structure. " +
                           (analysis.get('architecture', {}).get('structure', '') if analysis else ''),
                "diagram": self._create_architecture_diagram(repo_data, False, False),
                "technologies": self._extract_technologies(repo_data, analysis),
                "folder_structure": self._format_file_tree(repo_data.get('file_tree', []), max_files=30)
            },
            "contributing": {
                "guidelines": f"Fork {url}, make changes, and submit pull requests.",
                "code_style": self._get_code_style_for_lang(primary_lang)
            },
            "usage": {
                "basic_usage": self._get_usage_example(primary_lang, False, False),
                "examples": self._get_code_examples(primary_lang, False, False),
                "common_tasks": self._get_common_tasks(primary_lang, False)
            }
        }
    
    def _get_fallback_documentation(self, repo_data):

        """Fallback documentation if AI fails"""
        project_name = repo_data.get('name', 'Project')
        
        return {
            "readme": {
                "title": project_name,
                "description": f"{project_name} is a software project. Detailed documentation generation is temporarily unavailable. Please check back later or contact the repository maintainers for more information.",
                "features": [
                    "Version-controlled codebase",
                    "GitLab repository hosting",
                    "Collaborative development environment"
                ],
                "content": f"# {project_name}\n\n## Description\n\nThis project is hosted on GitLab. Automated documentation generation is temporarily unavailable.\n\n## Getting Started\n\nPlease refer to the repository files for setup and usage instructions.\n\n## Contributing\n\nContributions are welcome. Please fork the repository and submit pull requests."
            },
            "getting_started": {
                "prerequisites": [
                    "Git installed on your system",
                    "Appropriate runtime environment for the project"
                ],
                "installation": [
                    "Clone the repository",
                    "Navigate to project directory",
                    "Follow project-specific setup instructions"
                ],
                "quick_start": "Clone the repository and review the project files for specific setup instructions.",
                "configuration": "Check the repository for configuration files and environment setup requirements."
            },
            "api_endpoints": {
                "available": False,
                "endpoints": []
            },
            "architecture": {
                "overview": "Architecture details are being generated. Please check the repository structure manually.",
                "diagram": "Architecture diagram unavailable",
                "technologies": {},
                "folder_structure": "Please explore the repository to understand the folder structure."
            },
            "contributing": {
                "guidelines": "Fork the repository, make changes, and submit pull requests for review.",
                "code_style": "Follow standard coding practices for the languages used in this project.",
                "pull_request_process": "Submit pull requests through GitLab's interface for review.",
                "development_setup": "Clone the repository and set up your local development environment."
            },
            "usage": {
                "basic_usage": "Refer to the repository documentation for usage instructions.",
                "examples": [],
                "common_tasks": []
            }
        }