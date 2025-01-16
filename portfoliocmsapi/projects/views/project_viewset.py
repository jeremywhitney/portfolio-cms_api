from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Project, Tag, TechStack
from ..serializers import ProjectSerializer, GitHubRepositorySerializer
from ...utils import CreateRelationshipMixin, UpdateRelationshipMixin
from ...services.github import GitHubClient, GitHubSyncService


class ProjectViewSet(
    CreateRelationshipMixin, UpdateRelationshipMixin, viewsets.ModelViewSet
):
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    relationship_configs = {"tag": {"model": Tag}, "tech_stack": {"model": TechStack}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize GitHub services
        self.github_client = GitHubClient()
        self.sync_service = GitHubSyncService(github_client=self.github_client)

    @action(methods=["get"], detail=False, url_path="github")
    def list_github_repositories(self, request):
        """
        Lists GitHub repositories that aren't already linked to projects.
        """
        available_repos = self.sync_service.get_available_repositories()
        serializer = GitHubRepositorySerializer(available_repos, many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=False, url_path="github/create")
    def create_from_github(self, request):
        """
        Creates a new project from GitHub repository data.
        Expects a repo_url in the request data.
        """
        repo_url = request.data.get("repo_url")
        if not repo_url:
            return Response({"error": "repo_url is required"}, status=400)

        # Extract owner and repo name from URL
        repo_parts = repo_url.split("/")
        owner = repo_parts[-2]
        repo_name = repo_parts[-1]

        # Prepare project data from GitHub
        project_data = self.sync_service.prepare_project_data(owner, repo_name)
        # Add the user to the project data
        project_data["user"] = request.user.id

        # Create the project
        serializer = self.get_serializer(data=project_data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()

        # Sync languages and topics
        self.sync_service.sync_repository_languages(project)
        self.sync_service.sync_repository_topics(project)

        return Response(self.get_serializer(project).data, status=201)
