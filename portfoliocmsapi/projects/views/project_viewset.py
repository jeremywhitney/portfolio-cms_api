from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Project, Tag, TechStack
from ..serializers.project_serializer import ProjectSerializer
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
    def github(self, request):
        """
        Lists GitHub repositories that aren't already linked to projects.
        """
        available_repos = self.sync_service.get_available_repositories()
        return Response(available_repos)
