from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from unittest.mock import Mock, patch
from portfoliocmsapi.projects.models import Project
from portfoliocmsapi.services.github import GitHubClient, GitHubSyncService


class TestProjectViewSetGitHub(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Mock the GitHub client
        self.github_client = Mock(spec=GitHubClient)
        self.sync_service = GitHubSyncService(github_client=self.github_client)

    def test_list_available_repositories(self):
        """
        Tests that the github action correctly returns repositories
        that aren't already linked to projects.
        """
        # Mock repository data
        mock_repos = [
            {
                "name": "repo1",
                "description": "First test repo",
                "html_url": "https://github.com/testuser/repo1",
            },
            {
                "name": "repo2",
                "description": "Second test repo",
                "html_url": "https://github.com/testuser/repo2",
            },
        ]

        # Create a project for repo1 (so it shouldn't show up in available repos)
        Project.objects.create(
            user=self.user,
            title="Existing Project",
            repo_url="https://github.com/testuser/repo1",
            description="Test project",
            date_created="2024-01-01T00:00:00Z",
            last_update="2024-01-02T00:00:00Z",
        )

        # Mock the actual HTTP request that GitHubClient makes
        with patch("requests.Session.get") as mock_get:
            mock_get.return_value.json.return_value = mock_repos
            mock_get.return_value.status_code = 200

            # Make request to the endpoint
            response = self.client.get("/api/projects/github")

            # Verify response
            assert response.status_code == 200
            assert len(response.json()) == 1  # Should only get repo2
            assert response.json()[0]["name"] == "repo2"
