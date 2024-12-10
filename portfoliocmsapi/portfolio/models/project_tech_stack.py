from django.db import models
from .project import Project
from .tech_stack import TechStack


class ProjectTechStack(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tech_stack = models.ForeignKey(TechStack, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.title} - {self.tech_stack.name}"

    class Meta:
        verbose_name = "project tech stack"
        unique_together = ("project", "tech_stack")
