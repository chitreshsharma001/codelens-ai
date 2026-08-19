import os
import requests

# Required environment variables injected by GitLab CI/CD
GITLAB_URL = os.environ.get("CI_API_V4_URL")
PROJECT_ID = os.environ.get("CI_PROJECT_ID")
MR_IID = os.environ.get("CI_MERGE_REQUEST_IID")
# GITLAB_BOT_TOKEN must be manually set in CI/CD variables (Settings > CI/CD > Variables)
BOT_TOKEN = os.environ.get("GITLAB_BOT_TOKEN") 

def run_ai_review():
    """Simulates an AI analysis and posts a note on the Merge Request."""
    if not all([GITLAB_URL, PROJECT_ID, MR_IID, BOT_TOKEN]):
        print("Required CI variables (URL, ID, MR_IID, Token) not found. Skipping AI review.")
        return 0

    print("--- Starting AI Agentic Workflow Simulation ---")

    # Simulate AI analysis result
    ai_summary = "AI detected a potential dependency mismatch in 'requirements.txt' and noted missing docstrings in the 'ai_service.py' file. Code Quality: B+"
    
    note_endpoint = f"{GITLAB_URL}/projects/{PROJECT_ID}/merge_requests/{MR_IID}/notes"
    
    headers = {
        'Private-Token': BOT_TOKEN,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "body": f"**🤖 CodeLens AI Review:**\n\n{ai_summary}\n\n*This automated analysis was triggered by the CI pipeline to ensure code quality.*"
    }
    
    try:
        response = requests.post(note_endpoint, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print(f"✅ AI Review posted successfully to MR !{MR_IID}.")
            return 0
        else:
            print(f"❌ Failed to post AI Review. Status: {response.status_code}")
            return 1

    except Exception as e:
        print(f"❌ An error occurred during bot execution: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_ai_review()
    exit(exit_code)