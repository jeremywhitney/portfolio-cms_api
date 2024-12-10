from django.db import models
from django.contrib.auth.models import User
from .tag import Tag
from .tech_stack import TechStack


class Project(models.Model):
    # Syntax: Tuples of (value, display_name)
    STATUS_CHOICES = [
        ("in_development", "In Development"),
        ("completed", "Completed"),
        ("archived", "Archived"),
        ("paused", "Paused"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="in_development"
    )
    tag = models.ManyToManyField(Tag, through="ProjectTag")
    tech_stack = models.ManyToManyField(TechStack, through="ProjectTechStack")
    repo_url = models.URLField()
    deploy_url = models.URLField(blank=True, null=True)
    date_created = models.DateTimeField()
    last_update = models.DateTimeField()

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ["-date_created"]  # newest first
