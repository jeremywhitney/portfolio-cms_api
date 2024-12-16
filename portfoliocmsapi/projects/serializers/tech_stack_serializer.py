from rest_framework import serializers
from ..models.tech_stack import TechStack


class TechStackSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechStack
        fields = ["id", "name"]
