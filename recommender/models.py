from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(max_length=200)

    def __str__(self):
        return self.title
