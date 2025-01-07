# Handles raw GitHub API communication

import requests
from django.conf import settings


class GitHubClient:
    """
    Client for interacting with GitHub's REST API.
    Handles authentication and basic request configuration.
    """

    def __init__(self, access_token=None):
        """
        Initializes the GitHub API client with authentication and configuration.

        When the client is created, it verifies that the provided token (or the one from
        settings) is valid by making a test request to GitHub's API. This helps catch
        authentication issues immediately rather than having them appear during later operations.

        Args:
            access_token: Optional GitHub personal access token. If not provided,
                        uses the token from Django settings.

        Raises:
            ValueError: If the token is invalid or authentication fails
        """
        self.base_url = "https://api.github.com"
        self.session = requests.Session()

        # Use provided token or fall back to settings
        token = access_token or settings.GITHUB_ACCESS_TOKEN

        # Configure session headers we'll use for all requests
        self.session.headers.update(
            {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            }
        )

        # Verify the token is valid by making a test request
        try:
            test_response = self.session.get(f"{self.base_url}/user")
            test_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Invalid GitHub token or authentication failed: {str(e)}")

    def get_all_repositories(self) -> list:
        """
        Fetches all repositories for the authenticated user.

        This method retrieves a list of all repositories accessible to the authenticated user,
        including both public and private repositories. Each repository object includes
        basic information like name and description, as well as topics and language data
        that we'll use for generating tech stack items and tags.

        Returns:
            list: A list of dictionaries containing repository information

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        response = self.session.get(
            f"{self.base_url}/user/repos",
            headers=self.session.headers,
            params={
                "sort": "updated",  # Get most recently updated repos first
                "direction": "desc",  # Descending order (newest first)
                "per_page": 100,  # Maximum items per page to reduce API calls
            },
        )
        response.raise_for_status()
        return response.json()

    def get_repository_details(self, owner: str, repo: str) -> dict:
        """
        Fetches detailed information about a specific repository.

        Args:
            owner: The GitHub username of the repository owner
            repo: The name of the repository

        Returns:
            Dictionary containing repository information

        Example:
            client.get_repository_details('jeremywhitney', 'portfolio-cms_api')
        """
        response = self.session.get(
            f"{self.base_url}/repos/{owner}/{repo}", headers=self.session.headers
        )
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()

    def check_rate_limit(self) -> dict:
        """
        Checks the current rate limit status for the GitHub API.

        The GitHub API has rate limits to prevent excessive usage. For authenticated
        requests, you typically get 5,000 requests per hour. This method helps us
        monitor our usage to ensure we don't exceed these limits.

        Returns:
            dict: A dictionary containing rate limit information including:
                - The total number of requests allowed per hour
                - The number of remaining requests
                - The time when the limit will reset

        Raises:
            requests.exceptions.RequestException: If the rate limit check fails
        """
        response = self.session.get(
            f"{self.base_url}/rate_limit", headers=self.session.headers
        )
        response.raise_for_status()
        return response.json()
