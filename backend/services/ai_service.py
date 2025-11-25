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
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
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
        "strengths": ["Specific strength 1 with examples", "Specific strength 2 with examples", "Specific strength 3"],
        "weaknesses": ["Specific issue 1 with location", "Specific issue 2 with impact", "Specific issue 3"],
        "assessment": "Write a detailed paragraph analyzing code organization, naming conventions, patterns used, and overall quality"
    }},
    "complexity": {{
        "score": 6,
        "factors": ["Specific complexity factor 1", "Specific complexity factor 2", "Specific complexity factor 3"],
        "explanation": "Explain in detail why you gave this complexity score, mentioning specific files, patterns, or architectural decisions"
    }},
    "architecture": {{
        "pattern": "Identify the exact architectural pattern: MVC / MVVM / Microservices / Monolith / Layered / Clean Architecture / etc",
        "structure": "Write 2-3 paragraphs describing how the project is organized, what each major directory contains, and how components interact",
        "components": ["List all major components/modules with their responsibilities"]
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
- Be extremely detailed and specific
- Analyze the actual file structure and code patterns
- Provide at least 5 improvement suggestions across different categories
- Make suggestions actionable with clear implementation steps
- Base your analysis on the actual repository data provided
- Use technical terminology appropriately

OUTPUT FORMAT: Return ONLY valid JSON. No explanations before or after. Just the JSON object.
"""
        
        try:
            print("Analyzing repository with AI...")
            response = self.model.generate_content(
                analysis_prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 8192
                }
            )
            
            print(f"AI Analysis received, length: {len(response.text)}")
            analysis = self._parse_ai_response(response.text)
            
            if not analysis:
                print("Failed to parse AI response, using fallback")
                return self._get_fallback_analysis(repo_data)
            
            print("Analysis completed successfully")
            return analysis
        except Exception as e:
            print(f"Error in analysis: {str(e)}")
            return self._get_fallback_analysis(repo_data)
    
    def generate_documentation(self, repo_data, analysis):
        """Generate comprehensive documentation using Gemini"""
        
        context = self._prepare_context(repo_data)
        
        doc_prompt = f"""
You are an expert technical writer analyzing a REAL GitLab repository. You must generate SPECIFIC, DETAILED documentation based on the ACTUAL code and files in this repository.

REPOSITORY YOU ARE ANALYZING:
{context}

ANALYSIS ALREADY COMPLETED:
{json.dumps(analysis, indent=2)}

YOUR TASK: Generate detailed, repository-specific documentation. DO NOT use generic placeholders or templates. Every sentence must be specific to THIS repository based on the file structure, languages, and analysis provided above.

Generate documentation in this JSON format:
{{
    "readme": {{
        "title": "{repo_data.get('name', 'Project')}",
        "description": "Write 3-4 SPECIFIC paragraphs about what THIS repository does. Mention the actual technologies, frameworks, and purpose based on the file structure and languages. If you see React files, mention React. If you see Python/Flask, mention that. Be SPECIFIC about what the code does.",
        "features": [
            "List 5-7 ACTUAL features you can identify from the file structure and code",
            "Each feature should be specific to what this project actually does",
            "Mention actual filenames or components if visible in the structure"
        ],
        "content": "Generate a COMPLETE markdown README with:\n- Project title and badges\n- Detailed description (3-4 paragraphs) specific to THIS project\n- Features list based on actual functionality\n- Installation steps using the actual languages/tools detected\n- Usage examples with real code snippets in the detected language\n- Architecture overview based on the file structure\n- Contributing guidelines\n- License (if detected, otherwise suggest common ones)"
    }},
    "getting_started": {{
        "prerequisites": [
            "List ACTUAL prerequisites based on the detected languages and frameworks",
            "For Python projects: Python version, pip, virtualenv",
            "For Node.js: Node.js version, npm/yarn",
            "For Java: JDK version, Maven/Gradle",
            "Include database if you see database files",
            "Include Docker if you see Dockerfile"
        ],
        "installation": [
            "Write ACTUAL installation steps for THIS specific project",
            "Use the real package manager: npm, pip, maven, gradle, etc.",
            "Reference actual config files you see: package.json, requirements.txt, pom.xml",
            "Include database setup if relevant",
            "Include environment variable setup if you see .env.example"
        ],
        "quick_start": "Write a REAL quick start guide with:\n- Clone command with actual repo URL: {repo_data.get('web_url', 'repo-url')}\n- Install command using detected package manager\n- Setup steps for actual config files\n- Run command based on the project type (npm start, python app.py, java -jar, etc.)\n- Access URL if it's a web app",
        "configuration": "Explain ACTUAL configuration based on files you see:\n- If you see .env.example, list those variables\n- If you see config files, explain them\n- If you see docker-compose.yml, explain the services\n- Provide real examples, not generic placeholders"
    }},
    "api_endpoints": {{
        "available": "Set to true if you detect API routes/endpoints in the code (look for @app.route, router, API files)",
        "endpoints": [
            "If you see Flask routes, list them with methods and paths",
            "If you see Express routes, list them",
            "If you see Spring Boot controllers, list the endpoints",
            "For each endpoint: provide actual method, path, description, parameters",
            "Include real curl examples"
        ]
    }},
    "architecture": {{
        "overview": "Write 2-3 paragraphs explaining THIS project's architecture based on the folder structure:\n- Explain what each major folder contains\n- Describe how components interact based on the structure\n- Mention actual architectural patterns you identify (MVC, microservices, etc.)",
        "diagram": "Create a text-based diagram of THIS project's architecture based on actual folders and files you see",
        "technologies": {{
            "Frontend": "List ACTUAL frontend tech from the analysis (React, Vue, Angular, HTML, etc.)",
            "Backend": "List ACTUAL backend tech from languages detected",
            "Database": "Mention ACTUAL database if you see database files or configs",
            "DevOps": "List ACTUAL DevOps tools if you see Dockerfile, .gitlab-ci.yml, etc.",
            "Testing": "Mention ACTUAL test frameworks if you see test files"
        }},
        "folder_structure": "Explain THIS project's ACTUAL folder structure based on the file tree provided:\n```\n[Use actual folders from the file tree]\n```\nExplain what each folder contains based on the actual files you see"
    }},
    "contributing": {{
        "guidelines": "Generate contributing guidelines for {repo_data.get('name')}:\n- Fork and clone THIS repository: {repo_data.get('web_url')}\n- Setup using ACTUAL installation steps\n- Code style based on ACTUAL languages used\n- Testing with ACTUAL test framework if detected",
        "code_style": "Provide code style rules for the ACTUAL languages in this project:\n- If Python: PEP 8, type hints\n- If JavaScript/TypeScript: ESLint, Prettier\n- If Java: Google Java Style Guide\n- Be specific to what's actually used",
        "pull_request_process": "Standard PR process adapted to this project",
        "development_setup": "ACTUAL development setup for THIS project using detected tools and package managers"
    }},
    "usage": {{
        "basic_usage": "Write REAL usage guide with actual commands for THIS project:\n- How to run the application\n- How to access it (URL, CLI commands, etc.)\n- Common operations specific to what this project does",
        "examples": [
            "Provide 3-5 REAL code examples in the actual language used",
            "Show how to use actual features you identified",
            "Use real function/class names if visible in the structure"
        ],
        "common_tasks": [
            "List ACTUAL tasks users would perform with THIS project",
            "Provide real code snippets in the detected language",
            "Reference actual files and components"
        ]
    }}
}}

CRITICAL RULES - YOU MUST FOLLOW THESE:
1. **NO PLACEHOLDERS**: Every [bracket], every "TODO", every "your-X-here" is FORBIDDEN
2. **BE SPECIFIC**: Use actual filenames, languages, frameworks you see in the data
3. **REAL CODE**: All code examples must use the actual programming language detected
4. **ACTUAL STRUCTURE**: Use the real folder structure provided, not generic examples
5. **TRUE FEATURES**: Only list features you can infer from the actual file structure and analysis
6. **CONTEXTUAL**: If it's a web app (has frontend/backend folders), document it as such
7. **ACCURATE**: If you see requirements.txt, say "pip install -r requirements.txt", not "npm install"
8. **DETAILED**: Write 2-3 full paragraphs for descriptions, not 1 sentence

REMEMBER: You are documenting the repository at {repo_data.get('web_url')} - make EVERYTHING specific to it!

OUTPUT FORMAT: Return ONLY valid JSON. No explanations before or after. Just the JSON object.
"""
        
        try:
            print("Generating documentation with AI...")
            response = self.model.generate_content(
                doc_prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 8192
                }
            )
            
            print(f"AI Response received, length: {len(response.text)}")
            print(f"First 500 chars: {response.text[:500]}")
            
            documentation = self._parse_ai_response(response.text)
            
            if not documentation:
                print("Failed to parse documentation response, using fallback")
                return self._get_fallback_documentation(repo_data)
            
            print("Documentation generated successfully")
            return documentation
        except Exception as e:
            print(f"Error in documentation generation: {str(e)}")
            return self._get_fallback_documentation(repo_data)
    
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