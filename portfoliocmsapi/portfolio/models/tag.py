from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ["name"]  # alphabetical order
