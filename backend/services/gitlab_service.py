import requests
import os
from typing import Dict, List, Optional

class GitLabService:
    def __init__(self):
        self.base_url = "https://gitlab.com/api/v4"
        self.token = os.getenv('GITLAB_API_TOKEN')
        self.headers = {
            'PRIVATE-TOKEN': self.token
        } if self.token else {}
    
    def get_repository_data(self, repo_url: str) -> Dict:
        """
        Fetch comprehensive repository data from GitLab
        """
        try:
            # Extract project path from URL
            project_path = self._extract_project_path(repo_url)
            
            if not project_path:
                raise ValueError("Invalid GitLab repository URL")
            
            # Encode the project path for API
            encoded_path = requests.utils.quote(project_path, safe='')
            
            # Fetch project details
            project_data = self._get_project_details(encoded_path)
            
            # Fetch additional data
            file_tree = self._get_file_tree(encoded_path)
            languages = self._get_languages(encoded_path)
            readme_content = self._get_readme(encoded_path)
            commits = self._get_recent_commits(encoded_path)
            
            return {
                'name': project_data.get('name'),
                'description': project_data.get('description', 'No description provided'),
                'web_url': project_data.get('web_url'),
                'default_branch': project_data.get('default_branch', 'main'),
                'star_count': project_data.get('star_count', 0),
                'forks_count': project_data.get('forks_count', 0),
                'languages': languages,
                'file_tree': file_tree,
                'readme_content': readme_content,
                'recent_commits': commits,
                'created_at': project_data.get('created_at'),
                'last_activity_at': project_data.get('last_activity_at')
            }
            
        except Exception as e:
            print(f"Error fetching repository data: {str(e)}")
            raise
    
    def _extract_project_path(self, repo_url: str) -> Optional[str]:
        """Extract project path from GitLab URL"""
        try:
            # Remove trailing slashes and .git
            url = repo_url.rstrip('/').replace('.git', '')
            
            # Handle different URL formats
            if 'gitlab.com/' in url:
                # Extract path after gitlab.com/
                path = url.split('gitlab.com/')[-1]
                return path
            
            return None
        except Exception as e:
            print(f"Error extracting project path: {str(e)}")
            return None
    
    def _get_project_details(self, encoded_path: str) -> Dict:
        """Get project details from GitLab API"""
        url = f"{self.base_url}/projects/{encoded_path}"
        response = requests.get(url, headers=self.headers, timeout=10)
        
        # Log rate limit info if available
        if 'RateLimit-Remaining' in response.headers:
            print(f"GitLab API - Remaining: {response.headers.get('RateLimit-Remaining')}/{response.headers.get('RateLimit-Limit')}")
        
        if response.status_code == 429:
            reset_time = response.headers.get('RateLimit-Reset', 'unknown')
            raise requests.exceptions.HTTPError(
                f"GitLab rate limit exceeded. Please wait or add a GITLAB_API_TOKEN to increase limits. Resets at: {reset_time}"
            )
        
        response.raise_for_status()
        return response.json()
    
    def _get_file_tree(self, encoded_path: str, max_depth: int = 3) -> List[Dict]:
        """Get repository file tree"""
        try:
            url = f"{self.base_url}/projects/{encoded_path}/repository/tree"
            params = {
                'recursive': True,
                'per_page': 100
            }
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            files = response.json()
            
            # Sort files: directories first, then by path
            sorted_files = sorted(files, key=lambda x: (x.get('type') != 'tree', x.get('path', '')))
            
            return sorted_files[:100]  # Limit to 100 files
            
        except Exception as e:
            print(f"Error fetching file tree: {str(e)}")
            return []
    
    def _get_languages(self, encoded_path: str) -> Dict:
        """Get programming languages used in the repository"""
        try:
            url = f"{self.base_url}/projects/{encoded_path}/languages"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching languages: {str(e)}")
            return {}
    
    def _get_readme(self, encoded_path: str) -> str:
        """Get README content"""
        try:
            # Try different README file names
            readme_files = ['README.md', 'README.MD', 'readme.md', 'Readme.md', 'README']
            
            for readme_name in readme_files:
                try:
                    url = f"{self.base_url}/projects/{encoded_path}/repository/files/{readme_name}/raw"
                    response = requests.get(url, headers=self.headers, timeout=10)
                    
                    if response.status_code == 200:
                        return response.text
                except:
                    continue
            
            return "No README found"
            
        except Exception as e:
            print(f"Error fetching README: {str(e)}")
            return "Unable to fetch README"
    
    def _get_recent_commits(self, encoded_path: str, limit: int = 10) -> List[Dict]:
        """Get recent commits"""
        try:
            url = f"{self.base_url}/projects/{encoded_path}/repository/commits"
            params = {'per_page': limit}
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            commits = response.json()
            
            # Extract relevant commit info
            return [
                {
                    'id': commit.get('id'),
                    'title': commit.get('title'),
                    'author': commit.get('author_name'),
                    'date': commit.get('created_at'),
                    'message': commit.get('message', '')[:200]  # First 200 chars
                }
                for commit in commits
            ]
            
        except Exception as e:
            print(f"Error fetching commits: {str(e)}")
            return []