from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from recommender.models import Movie
from .serializers import RatingSerializer
from rest_framework import viewsets, status
from .models import Rating
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    def get_queryset(self):
        ratings = Rating.objects.filter(user = self.request.user)
        return ratings

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def create(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            rating = Rating.objects.create(movie=serializer.validated_data['movie'],rating=serializer.validated_data['rating'],user=self.request.user)
            return Response(RatingSerializer(rating).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
