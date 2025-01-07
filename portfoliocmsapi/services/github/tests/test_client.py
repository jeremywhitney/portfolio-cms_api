import pytest
from django.conf import settings
from unittest.mock import patch
from portfoliocmsapi.services.github.client import GitHubClient


class TestGitHubClient:
    """
    Test suite for the GitHub API client.
    We'll test initialization, API calls, and error handling.
    """

    def setup_method(self):
        """Creates a fresh client instance before each test"""
        self.client = GitHubClient()
        self.test_repo = "portfolio-cms_api"
        self.test_owner = "jeremywhitney"

    def test_client_initialization(self):
        """
        Tests that the client is configured correctly at startup.
        This ensures our authentication and headers are set properly.
        """
        assert self.client.base_url == "https://api.github.com"
        assert (
            self.client.session.headers["Authorization"]
            == f"token {settings.GITHUB_ACCESS_TOKEN}"
        )
        assert self.client.session.headers["Accept"] == "application/vnd.github.v3+json"

    @patch("requests.Session.get")
    def test_get_repository_details(self, mock_get):
        """
        Tests fetching repository details with a mocked response.
        We don't want to make real API calls in tests, so we simulate the response.
        """
        # Prepare mock response data
        mock_repo_data = {
            "name": self.test_repo,
            "description": "Test description",
            "html_url": f"https://github.com/{self.test_owner}/{self.test_repo}",
            "language": "Python",
        }

        # Configure the mock to return our test data
        mock_get.return_value.json.return_value = mock_repo_data
        mock_get.return_value.status_code = 200

        # Make the call
        repo_data = self.client.get_repository_details(self.test_owner, self.test_repo)

        # Verify the response
        assert repo_data["name"] == self.test_repo
        assert "description" in repo_data
        assert "html_url" in repo_data

        # Verify the correct endpoint was called
        mock_get.assert_called_once_with(
            f"{self.client.base_url}/repos/{self.test_owner}/{self.test_repo}",
            headers=self.client.session.headers,
        )

    @patch("requests.Session.get")
    def test_get_repository_languages(self, mock_get):
        """
        Tests fetching repository language information.
        This verifies we can get the programming languages used in a repository.
        """
        mock_languages = {"Python": 33495, "Shell": 248}
        mock_get.return_value.json.return_value = mock_languages
        mock_get.return_value.status_code = 200

        languages = self.client.get_repository_languages(
            self.test_owner, self.test_repo
        )

        assert "Python" in languages
        assert "Shell" in languages
        assert isinstance(languages["Python"], int)

    def test_invalid_token(self):
        """
        Tests that the client handles authentication errors appropriately.
        This ensures we fail gracefully when our token is invalid.
        """
        with pytest.raises(ValueError):
            GitHubClient(access_token="invalid_token")
