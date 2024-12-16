from rest_framework import serializers
from .tag_serializer import TagSerializer
from .tech_stack_serializer import TechStackSerializer
from ..models import Project


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    tag = TagSerializer(many=True, read_only=True)
    tech_stack = TechStackSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "user",
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

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "full_name": f"{obj.user.first_name} {obj.user.last_name}".strip(),
        }
