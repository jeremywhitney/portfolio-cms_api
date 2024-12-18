from django.db import models
from .post import Post
from portfoliocmsapi.projects.models.tag import Tag


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} - {self.tag.name}"

    class Meta:
        verbose_name = "post tag"
        verbose_name_plural = "post tags"
        unique_together = ("post", "tag")
