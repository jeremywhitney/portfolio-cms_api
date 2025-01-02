from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from ..models import Post
from portfoliocmsapi.projects.models import Project, Tag, TechStack
from ..serializers.post_serializer import PostSerializer
from ...utils import CreateRelationshipMixin, UpdateRelationshipMixin


class PostViewSet(
    CreateRelationshipMixin, UpdateRelationshipMixin, viewsets.ModelViewSet
):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    relationship_configs = {
        "project": {"model": Project},
        "tag": {"model": Tag},
        "tech_stack": {"model": TechStack},
    }
