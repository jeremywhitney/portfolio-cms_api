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

        # Mock repository data
        self.mock_repos = [
            {
                "name": "repo1",
                "description": "First test repo",
                "html_url": "https://github.com/testuser/repo1",
                "language": "Python",
                "topics": ["django", "api"],
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-02T00:00:00Z",
            },
            {
                "name": "repo2",
                "description": "Second test repo",
                "html_url": "https://github.com/testuser/repo2",
                "language": "JavaScript",
                "topics": ["react", "frontend"],
                "created_at": "2024-01-03T00:00:00Z",
                "updated_at": "2024-01-04T00:00:00Z",
            },
        ]

    def test_list_available_repositories(self):
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
            mock_get.return_value.json.return_value = self.mock_repos
            mock_get.return_value.status_code = 200

            response = self.client.get("/api/projects/github")

            assert response.status_code == 200
            assert len(response.json()) == 1  # Should only get repo2
            assert response.json()[0]["name"] == "repo2"

    def test_create_project_from_github(self):
        test_repo = self.mock_repos[0]

        self.client.force_authenticate(user=self.user)

        # Create two mock responses: one for repo details, one for languages
        mock_responses = {
            f"/repos/{self.user.username}/repo1": test_repo,
            f"/repos/{self.user.username}/repo1/languages": {"Python": 33495},
        }

        with patch("requests.Session.get") as mock_get:

            def mock_response(*args, **kwargs):
                mock = Mock()
                mock.status_code = 200
                # Get the endpoint from the URL
                url = args[0]
                if "languages" in url:
                    mock.json.return_value = mock_responses[
                        f"/repos/{self.user.username}/repo1/languages"
                    ]
                else:
                    mock.json.return_value = mock_responses[
                        f"/repos/{self.user.username}/repo1"
                    ]
                return mock

            mock_get.side_effect = mock_response

            response = self.client.post(
                "/api/projects/github/create",
                {"repo_url": test_repo["html_url"]},
                format="json",
            )

            assert response.status_code == 201
            assert response.data["title"] == test_repo["name"]
            assert response.data["repo_url"] == test_repo["html_url"]

            project = Project.objects.get(repo_url=test_repo["html_url"])
            assert project.title == test_repo["name"]

            # Verify TechStack and Tag relationships
            assert project.tech_stack.filter(name="Python").exists()
            assert project.tag.filter(name__in=["django", "api"]).count() == 2
