from django.db import models
from django.contrib.auth.models import User
from portfoliocmsapi.projects.models import Project, Tag, TechStack


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    project = models.ManyToManyField(
        Project, blank=True, null=True, on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(Tag, through="PostTag")
    tech_stack = models.ManyToManyField(TechStack, through="PostTechStack")
    date_created = models.DateTimeField()
    last_update = models.DateTimeField()

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["-date_created"]  # newest first
