from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from ..models import TechStack
from ..serializers.tech_stack_serializer import TechStackSerializer


class TechStackViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
