from django.db.models import Avg
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Movie
from ratings.models import Rating
from .serializers import MovieSerializer
from .MovieRecommender import *
from .SearchPagination import SearchPagination

class MovieListView(ListAPIView):
    pagination_class = SearchPagination
    def get_queryset(self):
        movie_title = self.request.query_params.get('title')
        movie_title = movie_title if movie_title else ""
        movies_user_rated = Rating.objects.filter(user = self.request.user).values_list('movie', flat=True)
        print(movie_title)
        queryset = Movie.objects.filter(title__icontains=movie_title).exclude(id__in=movies_user_rated)

        return queryset

    serializer_class = MovieSerializer


class MovieRecommendView(APIView):

    def get(self, request, format=None):
        movies_user_rated = list(Movie.objects.filter(id__in=Rating.objects.filter(user=self.request.user).values_list('movie')))
        if movies_user_rated:
            avg_rating = Rating.objects.aggregate(average_rating=Avg('rating'))['average_rating']
            movies_user_liked = list(Movie.objects.filter(id__in=Rating.objects.filter(rating__gte=avg_rating).values_list('movie')))

            movie_recommendation_titles = get_recommendation(rated_movies = movies_user_rated, liked_movies=movies_user_liked)
            movies = Movie.objects.filter(title__in=movie_recommendation_titles)
            movie_serializer = MovieSerializer(movies,many=True)
            return Response(movie_serializer.data)
        else:
            return Response([])




