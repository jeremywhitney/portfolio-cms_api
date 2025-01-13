import os
import sys
import django
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Add the project root to Python path
sys.path.append(str(BASE_DIR))

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfoliocmsproject.settings")
django.setup()

import requests
from django.conf import settings
from pprint import pprint


def test_github_connection():
    headers = {
        "Authorization": f"token {settings.GITHUB_ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    base_url = "https://api.github.com"

    # First get the repository basic info
    repo_name = "portfolio-cms_api"  # Let's look specifically at your CMS project
    response = requests.get(
        f"{base_url}/repos/jeremywhitney/{repo_name}", headers=headers
    )

    if response.status_code == 200:
        repo = response.json()

        # Now let's get the languages used in the repository
        languages_response = requests.get(
            f"{base_url}/repos/jeremywhitney/{repo_name}/languages", headers=headers
        )

        print("Basic Repository Info:")
        pprint(repo)

        print("\nRepository Languages:")
        pprint(languages_response.json())


if __name__ == "__main__":
    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfoliocmsproject.settings")
    django.setup()

    test_github_connection()
