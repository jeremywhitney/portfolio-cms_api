from rest_framework import serializers


class GitHubRepositorySerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(
        allow_null=True
    )  # GitHub repos can have null descriptions
    html_url = serializers.URLField()
    language = serializers.CharField(
        allow_null=True
    )  # Some repos might not have a primary language
    topics = serializers.ListField(child=serializers.CharField(), default=list)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
