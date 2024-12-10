from django.db import models


class TechStack(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "tech stack"
        ordering = ["name"]  # alphabetical order
