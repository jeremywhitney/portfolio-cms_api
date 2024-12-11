from rest_framework import serializers
from .tag_serializer import TagSerializer
from .tech_stack_serializer import TechStackSerializer
from ..models import Project


class ProjectSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True, fields=['id', 'first_name', 'last_name'])
    tag = TagSerializer(many=True, read_only=True)
    tech_stack = TechStackSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "user",  # Update to use a nested object displaying 'id', 'first_name', 'last_name' once UserSerializer is created
            "title",
            "description",
            "status",
            "tag",
            "tech_stack",
            "repo_url",
            "deploy_url",
            "date_created",
            "last_update",
        ]
