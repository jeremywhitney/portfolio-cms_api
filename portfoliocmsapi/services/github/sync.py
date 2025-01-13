import requests
from typing import List, Dict
from portfoliocmsapi.projects.models import Project, TechStack, Tag


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

    def prepare_project_data(self, owner: str, repo_name: str) -> Dict:
        """
        Prepares GitHub repository data for project creation by transforming
        it to match the Project model's structure.

        Args:
            owner: GitHub username of the repository owner
            repo_name: Name of the repository

        Returns:
            Dictionary containing transformed data ready for Project creation
        """
        repo_data = self.github_client.get_repository_details(owner, repo_name)

        project_data = {
            "title": repo_data["name"],
            "description": repo_data["description"] or "",  # Handle possible None
            "repo_url": repo_data["html_url"],
            "date_created": repo_data["created_at"],
            "last_update": repo_data["updated_at"],
            "status": "in_development",  # Default status for new projects
        }

        return project_data

    def sync_project(self, project: Project) -> Project:
        """
        Performs a complete synchronization of a project with its GitHub repository data.

        This method updates all GitHub-sourced fields while preserving fields that are
        managed within the CMS. Think of it like refreshing a webpage - we're getting
        the latest version of the data while keeping our local customizations.

        Args:
            project: The Project instance to synchronize with GitHub

        Returns:
            The updated Project instance

        Note:
            Fields like status that are managed in the CMS will not be modified.
            The user, repo_url, and date_created fields are considered immutable
            and won't be changed even if the GitHub data differs.
        """
        # Extract the owner and repo name from the project's repo_url
        # Example URL: https://github.com/jeremywhitney/portfolio-cms_api
        repo_parts = project.repo_url.split("/")
        owner = repo_parts[-2]  # Second to last part is the owner
        repo_name = repo_parts[-1]  # Last part is the repository name

        try:
            # Fetch the latest data from GitHub
            repo_data = self.github_client.get_repository_details(owner, repo_name)

            # Update only the fields that should be synchronized with GitHub
            project.title = repo_data["name"]
            project.description = (
                repo_data["description"] or ""
            )  # Handle potential None values
            project.last_update = repo_data["updated_at"]

            # Save the changes to the database
            project.save()

            return project

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Unable to sync project: {str(e)}")

    def sync_repository_languages(self, project: Project) -> None:
        """
        Syncs GitHub repository languages with project TechStack items.
        """
        # Extract repo information from URL
        repo_parts = project.repo_url.split("/")
        owner = repo_parts[-2]
        repo_name = repo_parts[-1]

        # Get languages from GitHub
        languages = self.github_client.get_repository_languages(owner, repo_name)

        # Create TechStack items and link them to project
        for language in languages.keys():
            tech_stack, _ = TechStack.objects.get_or_create(name=language)
            project.tech_stack.add(tech_stack)

    def sync_repository_topics(self, project: Project) -> None:
        """
        Syncs GitHub repository topics with project Tags.
        """
        # Extract repo information from URL
        repo_parts = project.repo_url.split("/")
        owner = repo_parts[-2]
        repo_name = repo_parts[-1]

        # Get repo details which include topics
        repo_data = self.github_client.get_repository_details(owner, repo_name)

        # Create Tags and link them to project
        for topic in repo_data["topics"]:
            tag, _ = Tag.objects.get_or_create(name=topic)
            project.tag.add(tag)
