from rest_framework import viewsets
from ..models import Project
from ..serializers.project_serializer import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


# 1. GitHub Integration Impact:
# GET requests will eventually pull from GitHub-synced data
# Updates might need to handle both manual changes and GitHub sync updates
# We might want to prevent certain fields from being manually updated if they should only sync from GitHub

# 2. Permission Considerations:
# GET requests should be public (no auth needed)
# All other operations should require authentication
# We might want to add checks to ensure only the owner can modify projects

# 3. Data Integrity:
# When adding/updating tags or tech stack, we might want custom validation
# We might want to prevent complete deletion and instead implement soft delete via status change

# ...

# Leave the basic ModelViewSet for now
# Plan to add permissions and authentication once we build the users app
# Add custom methods when we implement the GitHub integration
