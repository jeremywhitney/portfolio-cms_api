from django.contrib.auth.models import User
from unittest.mock import Mock
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
        # Set up mock client to return sample repositories
        self.github_client.get_all_repositories.return_value = self.mock_repos

        # Create a test user
        test_user = User.objects.create_user(username="testuser", password="testpass")

        # Create a project for one of the repositories
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

    def test_prepare_project_data(self, db):
        """
        Tests that GitHub repository data is correctly transformed into a format
        that matches the Project model fields. This transformation happens when
        a user selects a repository in the UI, before the data is used to
        populate the project creation form.
        """
        # Use one of the mock repositories as test data
        test_repo = self.mock_repos[0]

        # Have the mock client return this repository when asked for details
        self.github_client.get_repository_details.return_value = test_repo

        # Get the transformed data
        project_data = self.sync_service.prepare_project_data(
            owner="jeremywhitney", repo_name="portfolio-cms_api"
        )

        # Verify the transformation matches the Project model's structure
        assert project_data["title"] == test_repo["name"]
        assert project_data["description"] == test_repo["description"]
        assert project_data["repo_url"] == test_repo["html_url"]
        assert project_data["date_created"] == test_repo["created_at"]
        assert project_data["last_update"] == test_repo["updated_at"]
        assert "status" in project_data  # Should provide a default status

    def test_full_project_sync(self, db):
        """
        Tests a complete project synchronization with GitHub. This verifies that all
        fields that can be updated from GitHub are properly synced while preserving
        fields that are managed within the CMS.
        """
        # Create our test user - required since projects belong to users
        test_user = User.objects.create_user(username="testuser", password="testpass")

        # Create a project with initial data as if it was made some time ago
        initial_project = Project.objects.create(
            user=test_user,
            title="Old Project Title",
            description="This is an outdated description",
            repo_url="https://github.com/jeremywhitney/portfolio-cms_api",
            date_created="2024-01-01T00:00:00Z",
            last_update="2024-01-02T00:00:00Z",
            status="in_development",  # This is a CMS-managed field
        )

        # Set up mock GitHub data that represents newer repository information
        updated_repo_data = {
            "name": "Updated Project Title",
            "description": "This description has been updated on GitHub",
            "html_url": "https://github.com/jeremywhitney/portfolio-cms_api",
            "created_at": "2024-01-01T00:00:00Z",  # Creation date stays the same
            "updated_at": "2024-01-05T00:00:00Z",  # Last update is newer
        }

        # Configure our mock client to return this updated data
        self.github_client.get_repository_details.return_value = updated_repo_data

        # Perform the sync operation
        updated_project = self.sync_service.sync_project(initial_project)

        # Verify that GitHub-sourced fields were updated
        assert updated_project.title == updated_repo_data["name"]
        assert updated_project.description == updated_repo_data["description"]
        assert updated_project.last_update == updated_repo_data["updated_at"]

        # Verify that CMS-managed fields remain unchanged
        assert updated_project.status == "in_development"

        # Verify the immutable fields stayed the same
        assert updated_project.repo_url == initial_project.repo_url
        assert updated_project.date_created == initial_project.date_created
        assert updated_project.user == test_user

    def test_sync_repository_languages(self, db):
        """
        Tests that GitHub repository languages are correctly converted into TechStack items.
        """
        # Create test user and project
        test_user = User.objects.create_user(username="testuser", password="testpass")
        project = Project.objects.create(
            user=test_user,
            title="Test Project",
            description="Test description",
            repo_url="https://github.com/jeremywhitney/portfolio-cms_api",
            date_created="2024-01-01T00:00:00Z",
            last_update="2024-01-02T00:00:00Z",
        )

        # Mock GitHub API response with language data
        mock_languages = {"Python": 33495, "JavaScript": 5000, "HTML": 2000}
        self.github_client.get_repository_languages.return_value = mock_languages

        # Sync languages to TechStack
        self.sync_service.sync_repository_languages(project)

        # Verify TechStack items were created and linked to project
        project_tech_stack = project.tech_stack.all()
        tech_stack_names = {tech.name for tech in project_tech_stack}

        assert "Python" in tech_stack_names
        assert "JavaScript" in tech_stack_names
        assert "HTML" in tech_stack_names

    def test_sync_repository_topics(self, db):
        """
        Tests that GitHub repository topics are correctly converted into Tags.
        """
        # Create test user and project
        test_user = User.objects.create_user(username="testuser", password="testpass")
        project = Project.objects.create(
            user=test_user,
            title="Test Project",
            description="Test description",
            repo_url="https://github.com/jeremywhitney/portfolio-cms_api",
            date_created="2024-01-01T00:00:00Z",
            last_update="2024-01-02T00:00:00Z",
        )

        # Mock GitHub API response with topic data
        mock_repo_data = {
            "name": "portfolio-cms_api",
            "topics": ["portfolio", "django", "rest-api"],
        }
        self.github_client.get_repository_details.return_value = mock_repo_data

        # Sync topics to Tags
        self.sync_service.sync_repository_topics(project)

        # Verify Tags were created and linked to project
        project_tags = project.tag.all()
        tag_names = {tag.name for tag in project_tags}

        assert "Portfolio" in tag_names
        assert "Django" in tag_names
        assert "Rest-Api" in tag_names
