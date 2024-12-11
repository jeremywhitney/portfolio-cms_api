from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from ..models import Tag
from ..serializers.tag_serializer import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
