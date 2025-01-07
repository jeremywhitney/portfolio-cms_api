import pytest
from django.contrib.auth.models import User
from unittest.mock import Mock, patch
from portfoliocmsapi.services.github.sync import GitHubSyncService
from portfoliocmsapi.projects.models import Project


class TestGitHubSyncService:
    def setup_method(self):
        self.github_client = Mock()
        self.sync_service = GitHubSyncService(github_client=self.github_client)

        self.mock_repos = [
            {
                "name": "portfolio-cms_api",
                "description": "My portfolio CMS",
                "html_url": "https://github.com/jeremywhitney/portfolio-cms_api",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-02T00:00:00Z",
                "language": "Python",
                "topics": ["portfolio", "django"],
            },
            {
                "name": "another-project",
                "description": "Another project",
                "html_url": "https://github.com/jeremywhitney/another-project",
                "created_at": "2024-01-03T00:00:00Z",
                "updated_at": "2024-01-04T00:00:00Z",
                "language": "JavaScript",
                "topics": ["web"],
            },
        ]

    def test_get_available_repositories(self, db):
        # Set up our mock to return our sample repositories
        self.github_client.get_all_repositories.return_value = self.mock_repos

        # Create a test user
        test_user = User.objects.create_user(username="testuser", password="testpass")

        # Create a project for one of our repositories
        Project.objects.create(
            user=test_user,
            title="Existing Project",
            repo_url="https://github.com/jeremywhitney/portfolio-cms_api",
            description="Test project",
            date_created="2024-01-01T00:00:00Z",
            last_update="2024-01-02T00:00:00Z",
        )

        available_repos = self.sync_service.get_available_repositories()

        assert len(available_repos) == 1
        assert available_repos[0]["name"] == "another-project"
