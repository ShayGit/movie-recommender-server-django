from rest_framework import serializers
from recommender.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id','title', 'image')

