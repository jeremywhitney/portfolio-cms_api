from rest_framework import viewsets
from ..models import TechStack
from ..serializers.tech_stack_serializer import TechStackSerializer


class TechStackViewSet(viewsets.ModelViewSet):
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
