import requests
import os
from urllib.parse import quote

class GitLabService:
    def __init__(self):
        # GitLab API token (optional - public repos don't need it)
        self.token = os.environ.get('GITLAB_TOKEN', '')
        self.base_url = 'https://gitlab.com/api/v4'
        
    def fetch_repository_data(self, repo_url):
        """
        Fetch repository data from GitLab API
        repo_url: https://gitlab.com/username/project
        """
        try:
            # Extract project path from URL
            # Example: https://gitlab.com/gitlab-org/gitlab -> gitlab-org/gitlab
            parts = repo_url.replace('https://gitlab.com/', '').replace('http://gitlab.com/', '')
            project_path = parts.split('?')[0].strip('/')
            
            # URL encode the project path
            encoded_path = quote(project_path, safe='')
            
            # Headers
            headers = {}
            if self.token:
                headers['PRIVATE-TOKEN'] = self.token
            
            # Fetch project details
            project_url = f"{self.base_url}/projects/{encoded_path}"
            response = requests.get(project_url, headers=headers)
            
            if response.status_code != 200:
                print(f"Error fetching project: {response.status_code}")
                return None
            
            project_data = response.json()
            
            # Fetch repository tree (file structure)
            tree_url = f"{self.base_url}/projects/{encoded_path}/repository/tree"
            tree_response = requests.get(tree_url, headers=headers, params={'per_page': 100})
            tree_data = tree_response.json() if tree_response.status_code == 200 else []
            
            # Fetch README if exists
            readme_content = self._fetch_readme(encoded_path, headers)
            
            # Fetch recent commits
            commits_url = f"{self.base_url}/projects/{encoded_path}/repository/commits"
            commits_response = requests.get(commits_url, headers=headers, params={'per_page': 10})
            commits_data = commits_response.json() if commits_response.status_code == 200 else []
            
            # Fetch languages
            languages_url = f"{self.base_url}/projects/{encoded_path}/languages"
            languages_response = requests.get(languages_url, headers=headers)
            languages_data = languages_response.json() if languages_response.status_code == 200 else {}
            
            return {
                'name': project_data.get('name'),
                'description': project_data.get('description', 'No description provided'),
                'language': project_data.get('default_branch', 'main'),
                'star_count': project_data.get('star_count', 0),
                'forks_count': project_data.get('forks_count', 0),
                'web_url': project_data.get('web_url'),
                'created_at': project_data.get('created_at'),
                'last_activity_at': project_data.get('last_activity_at'),
                'readme': readme_content,
                'file_structure': tree_data,
                'recent_commits': commits_data,
                'languages': languages_data,
                'topics': project_data.get('topics', []),
                'visibility': project_data.get('visibility', 'private')
            }
            
        except Exception as e:
            print(f"Error in fetch_repository_data: {str(e)}")
            return None
    
    def _fetch_readme(self, encoded_path, headers):
        """Fetch README content"""
        try:
            readme_files = ['README.md', 'README.MD', 'readme.md', 'Readme.md']
            
            for readme_file in readme_files:
                file_url = f"{self.base_url}/projects/{encoded_path}/repository/files/{quote(readme_file, safe='')}/raw"
                response = requests.get(file_url, headers=headers, params={'ref': 'main'})
                
                if response.status_code == 200:
                    return response.text
                
                # Try master branch
                response = requests.get(file_url, headers=headers, params={'ref': 'master'})
                if response.status_code == 200:
                    return response.text
            
            return "No README found"
            
        except Exception as e:
            print(f"Error fetching README: {str(e)}")
            return "Error fetching README"