from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MovieListView,MovieRecommendView

router = DefaultRouter()

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie_search'),
    path('movies/recommend/', MovieRecommendView.as_view(), name='movie_recommend'),
]