import requests
import os
import sys
from time import sleep

# The public URL of the deployed service (e.g., frontend URL)
# RENDER_EXTERNAL_URL is available in paid Render tiers; fallback to hardcoded URL
SERVICE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://codelens-ai-frontend.onrender.com")

def run_health_check(url, max_retries=5, delay=5):
    """Pings the deployed service URL to check for a 200 OK status."""
    print(f"Starting health check for: {url}")
    
    if not url.endswith('/'):
        url += '/'

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Health check successful! Status: {response.status_code}")
                return 0
            else:
                print(f"⚠️ Attempt {attempt + 1}: Received status code {response.status_code}. Retrying...")

        except requests.exceptions.ConnectionError:
            print(f"Attempt {attempt + 1}: Connection failed. Retrying...")
            
        if attempt < max_retries - 1:
            sleep(delay)

    print(f"Health check failed after {max_retries} attempts.")
    return 1

if __name__ == "__main__":
    exit_code = run_health_check(SERVICE_URL)
    sys.exit(exit_code)