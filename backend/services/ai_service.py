import os
import json
import requests

class AIService:
    def __init__(self):
        # Get API key from environment variable
        self.api_key = os.environ.get('GEMINI_API_KEY', '')
        if not self.api_key:
            print("WARNING: GEMINI_API_KEY not set!")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def _call_gemini(self, prompt):
        """Call Google Gemini API"""
        try:
            url = f"{self.api_url}?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048
                }
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code != 200:
                print(f"Gemini API Error: {response.status_code}")
                return None
            
            data = response.json()
            text = data['candidates'][0]['content']['parts'][0]['text']
            return text
            
        except Exception as e:
            print(f"Error calling Gemini: {str(e)}")
            return None
    
    def analyze_repository(self, repo_data):
        """Analyze repository and provide insights"""
        try:
            prompt = f"""
Analyze this GitLab repository and provide a comprehensive analysis.

Repository: {repo_data.get('name')}
Description: {repo_data.get('description')}
Languages: {json.dumps(repo_data.get('languages', {}))}
Topics: {json.dumps(repo_data.get('topics', []))}
File Structure: {json.dumps(repo_data.get('file_structure', [])[:20])}

Provide your analysis in JSON format with these fields:
{{
    "overview": "Brief overview of the project",
    "code_quality": "Assessment of code organization",
    "tech_stack": ["List", "of", "technologies"],
    "strengths": ["Key", "strengths"],
    "areas_for_improvement": ["Areas", "to", "improve"],
    "complexity_score": "1-10 rating with explanation"
}}

Return ONLY valid JSON, no markdown or extra text.
"""
            
            response_text = self._call_gemini(prompt)
            
            if not response_text:
                return self._get_fallback_analysis()
            
            # Clean response
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned.replace('```json', '').replace('```', '').strip()
            elif cleaned.startswith('```'):
                cleaned = cleaned.replace('```', '').strip()
            
            return json.loads(cleaned)
            
        except Exception as e:
            print(f"Error in analyze_repository: {str(e)}")
            return self._get_fallback_analysis()
    
    def generate_documentation(self, repo_data):
        """Generate comprehensive documentation"""
        try:
            prompt = f"""
Generate documentation for this repository:

Repository: {repo_data.get('name')}
Description: {repo_data.get('description')}
README: {repo_data.get('readme', 'No README')[:1000]}
Files: {json.dumps(repo_data.get('file_structure', [])[:15])}

Create documentation sections as JSON:
{{
    "getting_started": "How to get started",
    "installation": "Installation steps",
    "usage": "How to use",
    "architecture": "Architecture overview",
    "api_endpoints": "API docs if applicable",
    "contributing": "How to contribute"
}}

Return ONLY valid JSON.
"""
            
            response_text = self._call_gemini(prompt)
            
            if not response_text:
                return self._get_fallback_documentation()
            
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned.replace('```json', '').replace('```', '').strip()
            elif cleaned.startswith('```'):
                cleaned = cleaned.replace('```', '').strip()
            
            return json.loads(cleaned)
            
        except Exception as e:
            print(f"Error in generate_documentation: {str(e)}")
            return self._get_fallback_documentation()
    
    def get_suggestions(self, repo_data):
        """Get improvement suggestions"""
        try:
            prompt = f"""
Analyze this repository and provide improvement suggestions:

Repository: {repo_data.get('name')}
Languages: {json.dumps(repo_data.get('languages', {}))}
Files: {json.dumps(repo_data.get('file_structure', [])[:20])}
Has README: {bool(repo_data.get('readme') and len(repo_data.get('readme', '')) > 50)}

Provide suggestions as JSON:
{{
    "suggestions": [
        {{
            "category": "Documentation/Testing/CI-CD/Security/Code Quality",
            "priority": "High/Medium/Low",
            "title": "Brief title",
            "description": "Detailed suggestion",
            "impact": "Expected impact"
        }}
    ]
}}

Focus on: documentation, testing, CI/CD, security, code organization.
Return ONLY valid JSON.
"""
            
            response_text = self._call_gemini(prompt)
            
            if not response_text:
                return self._get_fallback_suggestions()
            
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned.replace('```json', '').replace('```', '').strip()
            elif cleaned.startswith('```'):
                cleaned = cleaned.replace('```', '').strip()
            
            result = json.loads(cleaned)
            return result.get('suggestions', [])
            
        except Exception as e:
            print(f"Error in get_suggestions: {str(e)}")
            return self._get_fallback_suggestions()
    
    def generate_readme(self, repo_data):
        """Generate a complete README.md"""
        try:
            prompt = f"""
Create a professional README.md for this repository:

Repository: {repo_data.get('name')}
Description: {repo_data.get('description')}
Languages: {json.dumps(repo_data.get('languages', {}))}
Topics: {json.dumps(repo_data.get('topics', []))}

Generate a complete markdown README with:
- Title and description
- Features
- Installation
- Usage
- Contributing
- License

Return raw markdown text.
"""
            
            response_text = self._call_gemini(prompt)
            
            if not response_text:
                return self._get_fallback_readme(repo_data)
            
            return response_text
            
        except Exception as e:
            print(f"Error in generate_readme: {str(e)}")
            return self._get_fallback_readme(repo_data)
    
    # Fallback methods for when API fails
    def _get_fallback_analysis(self):
        return {
            "overview": "Repository analysis based on structure",
            "code_quality": "Well-organized codebase",
            "tech_stack": ["Multiple languages detected"],
            "strengths": ["Active development", "Clear structure"],
            "areas_for_improvement": ["Consider adding more documentation"],
            "complexity_score": "Moderate complexity - 5/10"
        }
    
    def _get_fallback_documentation(self):
        return {
            "getting_started": "Clone the repository and follow setup instructions",
            "installation": "Run setup commands as specified in the project",
            "usage": "See examples in the repository",
            "architecture": "Standard project architecture",
            "api_endpoints": "Check source code for API details",
            "contributing": "Fork, make changes, and submit pull requests"
        }
    
    def _get_fallback_suggestions(self):
        return [
            {
                "category": "Documentation",
                "priority": "High",
                "title": "Add comprehensive README",
                "description": "Create detailed documentation for users and contributors",
                "impact": "Improves onboarding and adoption"
            },
            {
                "category": "Testing",
                "priority": "High",
                "title": "Implement automated tests",
                "description": "Add unit and integration tests",
                "impact": "Increases code reliability"
            }
        ]
    
    def _get_fallback_readme(self, repo_data):
        name = repo_data.get('name', 'Repository')
        desc = repo_data.get('description', 'A GitLab project')
        
        return f"""# {name}

{desc}

## Installation

```bash
git clone [repository-url]
cd {name}
```

## Usage

[Add usage instructions here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify license]
"""