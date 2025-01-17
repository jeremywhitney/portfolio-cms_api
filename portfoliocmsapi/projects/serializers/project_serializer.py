from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Project
from .tag_serializer import TagSerializer
from .tech_stack_serializer import TechStackSerializer


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), read_only=False
    )
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
        read_only_fields = []
        extra_kwargs = {
            "date_created": {"read_only": False, "required": True},
            "last_update": {"read_only": False, "required": True},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["user"] = {
            "id": instance.user.id,
            "full_name": f"{instance.user.first_name} {instance.user.last_name}".strip(),
        }
        return ret
