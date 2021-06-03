from rest_framework import serializers
from .models import Rating
from recommender.serializers import MovieSerializer


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'movie', 'rating')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['movie'] = MovieSerializer(instance.movie).data
        return response
