from typing import List, Dict
from portfoliocmsapi.projects.models import Project


class GitHubSyncService:
    """
    Service for synchronizing GitHub repository data with portfolio projects.

    This service acts as a bridge between our GitHub API client and the Project model.
    It handles fetching repository data and transforming it into a format that matches
    our project structure, while ensuring we don't create duplicate projects for the
    same repository.
    """

    def __init__(self, github_client):
        # We accept the client as a parameter to make testing easier and to separate
        # concerns between API communication and data synchronization
        self.github_client = github_client

    def get_available_repositories(self) -> List[Dict]:
        """
        Retrieves a list of GitHub repositories that aren't yet linked to any projects.

        This method compares all repositories from GitHub against existing projects in
        our database to identify repositories that are available for project creation.
        This prevents accidentally creating duplicate projects for the same repository.

        Returns:
            List of repository data dictionaries for repositories that don't have
            corresponding projects yet.
        """
        # First, get all repositories from GitHub
        all_repos = self.github_client.get_all_repositories()

        # Get the repo URLs of existing projects from our database
        existing_urls = set(Project.objects.values_list("repo_url", flat=True))

        # Filter out any repositories that already have associated projects
        available_repos = [
            repo for repo in all_repos if repo["html_url"] not in existing_urls
        ]

        return available_repos
