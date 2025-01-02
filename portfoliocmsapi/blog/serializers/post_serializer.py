from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Post
from portfoliocmsapi.projects.models import Project
from portfoliocmsapi.projects.serializers import (
    TagSerializer,
    TechStackSerializer,
)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), read_only=False
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), allow_null=True, required=False
    )
    tag = TagSerializer(many=True, read_only=True)
    tech_stack = TechStackSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "title",
            "content",
            "project",
            "tag",
            "tech_stack",
            "date_created",
            "last_update",
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["user"] = {
            "id": instance.user.id,
            "full_name": f"{instance.user.first_name} {instance.user.last_name}".strip(),
        }
        ret["project"] = [
            {"id": project.id, "title": project.title}
            for project in instance.project.all()
        ]
        return ret
