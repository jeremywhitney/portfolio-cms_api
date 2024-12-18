from rest_framework import serializers
from ..models import Media, Post
from portfoliocmsapi.projects.models import Project


class MediaSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), allow_null=True
    )
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), allow_null=True
    )

    class Meta:
        model = Media
        fields = [
            "id",
            "content_type",
            "file",
            "file_size",
            "project",
            "post",
            "upload_date",
        ]
