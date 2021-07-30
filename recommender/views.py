from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie
from .serializers import MovieSerializer
from .MovieRecommender import *
from .SearchPagination import SearchPagination
from auth.serializers import UserRatingSerializer


class MovieListView(ListAPIView):
    pagination_class = SearchPagination
    serializer_class = MovieSerializer

    def get_queryset(self):
        movie_title = self.request.query_params.get('title', "")
        user_ratings_serializer = UserRatingSerializer(self.request.user)
        movies_user_rated_ids = [movie['id'] for movie in user_ratings_serializer.data['my_movies']]
        queryset = Movie.objects.filter(title__icontains=movie_title).exclude(id__in=movies_user_rated_ids)
        return queryset


class MovieRecommendView(APIView):

    def get(self, request, format=None):
        user_ratings_serializer = UserRatingSerializer(self.request.user)
        movies_user_rated = user_ratings_serializer.data['my_movies']
        user_ratings_objects = user_ratings_serializer.data['my_ratings']
        if movies_user_rated:
            user_ratings = [rating['rating'] for rating in user_ratings_objects]
            avg_rating = sum(user_ratings) / len(user_ratings)
            movies_titles_user_liked = [rating['movie']['title'] for rating in user_ratings_objects if
                                        rating['rating'] >= avg_rating]
            movies_titles_user_rated = [movie['title'] for movie in movies_user_rated]
            movie_recommendation_titles = get_recommendation(rated_movies=movies_titles_user_rated,
                                                             liked_movies=movies_titles_user_liked)
            movies = Movie.objects.filter(title__in=movie_recommendation_titles).order_by('title')
            movie_serializer = MovieSerializer(movies, many=True)
            return Response(movie_serializer.data)

        return Response([])
