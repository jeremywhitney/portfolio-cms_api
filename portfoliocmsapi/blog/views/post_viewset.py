from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from ..models import Post
from portfoliocmsapi.projects.models import *
from ..serializers.post_serializer import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        # Handle initial projects if included
        project_ids = self.request.data.get("project", [])
        if project_ids:
            # Validate projects exist
            for project_id in project_ids:
                if not Project.objects.filter(id=project_id).exists():
                    raise ValidationError(
                        f"Project with id {project_id} does not exist"
                    )
            # Add projects
            instance.project.add(*project_ids)

        # Handle initial tags if included
        tag_ids = self.request.data.get("tag", [])
        if tag_ids:
            # Validate tags exist
            for tag_id in tag_ids:
                if not Tag.objects.filter(id=tag_id).exists():
                    raise ValidationError(f"Tag with id {tag_id} does not exist")
            # Add tags
            instance.tag.add(*tag_ids)

        # Handle initial tech stack if included
        tech_stack_ids = self.request.data.get("tech_stack", [])
        if tech_stack_ids:
            # Validate tech stack items exist
            for tech_id in tech_stack_ids:
                if not TechStack.objects.filter(id=tech_id).exists():
                    raise ValidationError(
                        f"Tech Stack with id {tech_id} does not exist"
                    )
            # Add tech stack items
            instance.tech_stack.add(*tech_stack_ids)

    def perform_update(self, serializer):
        instance = serializer.save()

        # Handle project updates if included in request
        if "project" in self.request.data:
            project_ids = self.request.data.get("project", [])

            if not project_ids:  # Empty array = remove all projects
                instance.project.clear()
            else:
                # Validate projects exist in database
                for project_id in project_ids:
                    if not Project.objects.filter(id=project_id).exists():
                        raise ValidationError(
                            f"Project with id {project_id} does not exist"
                        )

                    # Toggle logic: remove if exists, add if doesn't
                    if instance.project.filter(id=project_id).exists():
                        instance.project.remove(project_id)
                    else:
                        instance.project.add(project_id)

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
