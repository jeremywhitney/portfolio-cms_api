from django.db import models
from .project import Project
from .tag import Tag


class ProjectTag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.title} - {self.tag.name}"

    class Meta:
        verbose_name = "project tag"
        verbose_name_plural = "project tags"
        unique_together = ("project", "tag")
