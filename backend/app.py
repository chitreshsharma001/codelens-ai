from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from services.gitlab_service import GitLabService
from services.ai_service import AIService

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize services
gitlab_service = GitLabService()
ai_service = AIService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'RepoInsight AI is running'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_repository():
    """
    Analyze a GitLab repository
    Expected JSON: { "repo_url": "https://gitlab.com/username/project" }
    """
    try:
        data = request.get_json()
        repo_url = data.get('repo_url')
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        # Step 1: Fetch repository data from GitLab
        print(f"Fetching repository data for: {repo_url}")
        repo_data = gitlab_service.fetch_repository_data(repo_url)
        
        if not repo_data:
            return jsonify({'error': 'Could not fetch repository data. Check URL and permissions.'}), 400
        
        # Step 2: Analyze with AI
        print("Analyzing repository with AI...")
        analysis = ai_service.analyze_repository(repo_data)
        
        # Step 3: Generate documentation
        print("Generating documentation...")
        documentation = ai_service.generate_documentation(repo_data)
        
        # Step 4: Get improvement suggestions
        print("Getting improvement suggestions...")
        suggestions = ai_service.get_suggestions(repo_data)
        
        return jsonify({
            'success': True,
            'repository': {
                'name': repo_data.get('name'),
                'description': repo_data.get('description'),
                'language': repo_data.get('language'),
                'stars': repo_data.get('star_count', 0),
                'forks': repo_data.get('forks_count', 0)
            },
            'analysis': analysis,
            'documentation': documentation,
            'suggestions': suggestions
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-readme', methods=['POST'])
def generate_readme():
    """
    Generate README content for a repository
    Expected JSON: { "repo_url": "...", "repo_data": {...} }
    """
    try:
        data = request.get_json()
        repo_url = data.get('repo_url')
        
        # Fetch fresh data
        repo_data = gitlab_service.fetch_repository_data(repo_url)
        
        if not repo_data:
            return jsonify({'error': 'Could not fetch repository data'}), 400
        
        # Generate comprehensive README
        readme_content = ai_service.generate_readme(repo_data)
        
        return jsonify({
            'success': True,
            'readme': readme_content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)