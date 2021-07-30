from django.db import models
from django.contrib.auth.models import User
from recommender.models import Movie
from django.core.validators import MaxValueValidator, MinValueValidator


class Rating(models.Model):
    user = models.ForeignKey(User, related_name='my_ratings', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    class Meta:
        unique_together = [['movie', 'user']]
