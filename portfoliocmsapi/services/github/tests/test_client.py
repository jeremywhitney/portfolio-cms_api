import pytest
from django.conf import settings
from unittest.mock import patch
from portfoliocmsapi.services.github.client import GitHubClient


class TestGitHubClient:
    def setup_method(self):
        """Creates a fresh client instance before each test"""
        self.client = GitHubClient()
        self.test_repo = "portfolio-cms_api"
        self.test_owner = "jeremywhitney"

    def test_client_initialization(self):
        """Tests that the client is configured correctly at startup"""
        assert self.client.base_url == "https://api.github.com"
        assert (
            self.client.session.headers["Authorization"]
            == f"token {settings.GITHUB_ACCESS_TOKEN}"
        )
        assert self.client.session.headers["Accept"] == "application/vnd.github.v3+json"

    @patch("requests.Session.get")
    def test_get_all_repositories(self, mock_get):
        """Tests fetching all repositories for the authenticated user"""
        mock_repos = [
            {
                "name": "repo1",
                "description": "First test repo",
                "topics": ["python", "django"],
                "language": "Python",
            },
            {
                "name": "repo2",
                "description": "Second test repo",
                "topics": ["javascript", "react"],
                "language": "JavaScript",
            },
        ]
        mock_get.return_value.json.return_value = mock_repos
        mock_get.return_value.status_code = 200

        repos = self.client.get_all_repositories()

        assert len(repos) == 2
        assert repos[0]["name"] == "repo1"
        assert "topics" in repos[0]
        assert "language" in repos[0]

    @patch("requests.Session.get")
    def test_get_repository_details(self, mock_get):
        """Tests fetching detailed information about a specific repository"""
        mock_repo_data = {
            "name": self.test_repo,
            "description": "Test description",
            "html_url": f"https://github.com/{self.test_owner}/{self.test_repo}",
            "language": "Python",
            "topics": ["portfolio", "cms"],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-02T00:00:00Z",
        }

        mock_get.return_value.json.return_value = mock_repo_data
        mock_get.return_value.status_code = 200

        repo = self.client.get_repository_details(self.test_owner, self.test_repo)

        assert repo["name"] == self.test_repo
        assert "description" in repo
        assert "topics" in repo
        assert "language" in repo
        assert "created_at" in repo

    @patch("requests.Session.get")
    def test_get_repository_languages(self, mock_get):
        """Tests fetching language statistics for a repository"""
        mock_languages = {"Python": 33495, "Shell": 248}
        mock_get.return_value.json.return_value = mock_languages
        mock_get.return_value.status_code = 200

        languages = self.client.get_repository_languages(
            self.test_owner, self.test_repo
        )

        assert languages == mock_languages
        mock_get.assert_called_once_with(
            f"{self.client.base_url}/repos/{self.test_owner}/{self.test_repo}/languages",
            headers=self.client.session.headers,
        )

    @patch("requests.Session.get")
    def test_rate_limit_handling(self, mock_get):
        """Tests that the client properly checks and handles API rate limits"""
        mock_rate_limit = {
            "resources": {
                "core": {"limit": 5000, "remaining": 4990, "reset": 1644126465}
            }
        }
        mock_get.return_value.json.return_value = mock_rate_limit
        mock_get.return_value.status_code = 200

        rate_limit = self.client.check_rate_limit()

        assert "resources" in rate_limit
        assert "core" in rate_limit["resources"]
        assert rate_limit["resources"]["core"]["remaining"] > 0

    def test_invalid_token(self):
        """Tests that the client handles authentication errors appropriately"""
        with pytest.raises(ValueError):
            GitHubClient(access_token="invalid_token")
