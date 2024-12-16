from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_superuser",
            "last_login",
            "date_joined",
        ]
        read_only_fields = ["is_active", "is_superuser", "last_login", "date_joined"]
