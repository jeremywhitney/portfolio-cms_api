from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from ..models import Project, Tag, TechStack
from ..serializers.project_serializer import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        # Handle tag updates if included in request
        if "tag" in self.request.data:
            tag_ids = self.request.data.get("tag", [])

            if not tag_ids:  # Empty array = remove all tags
                instance.tag.clear()
            else:
                # Validate tags exist in database
                for tag_id in tag_ids:
                    if not Tag.objects.filter(id=tag_id).exists():
                        raise ValidationError(f"Tag with id {tag_id} does not exist")

                    # Toggle logic: remove if exists, add if doesn't
                    if instance.tag.filter(id=tag_id).exists():
                        instance.tag.remove(tag_id)
                    else:
                        instance.tag.add(tag_id)

        # Handle tech stack updates if included in request
        if "tech_stack" in self.request.data:
            tech_stack_ids = self.request.data.get("tech_stack", [])

            if not tech_stack_ids:  # Empty array = remove all tech stack items
                instance.tech_stack.clear()
            else:
                # Validate tech stack items exist in database
                for tech_id in tech_stack_ids:
                    if not TechStack.objects.filter(id=tech_id).exists():
                        raise ValidationError(
                            f"Tech Stack with id {tech_id} does not exist"
                        )

                    # Toggle logic: remove if exists, add if doesn't
                    if instance.tech_stack.filter(id=tech_id).exists():
                        instance.tech_stack.remove(tech_id)
                    else:
                        instance.tech_stack.add(tech_id)


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
