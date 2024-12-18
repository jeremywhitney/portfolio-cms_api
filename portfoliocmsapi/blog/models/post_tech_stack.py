from django.db import models
from .post import Post
from portfoliocmsapi.projects.models.tech_stack import TechStack


class PostTechStack(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tech_stack = models.ForeignKey(TechStack, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} - {self.tech_stack.name}"

    class Meta:
        verbose_name = "post tech stack"
        unique_together = ("post", "tech_stack")
