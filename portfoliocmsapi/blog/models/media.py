from django.db import models
from portfoliocmsapi.projects.models.project import Project
from .post import Post


class Media(models.Model):
    CONTENT_TYPES = [("audio", "Audio)"), ("image", "Image"), ("video", "Video")]

    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    file = models.FileField(upload_to="media/")
    file_size = models.PositiveIntegerField(editable=False)
    project = models.ForeignKey(
        Project, blank=True, null=True, on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
