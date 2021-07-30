from .serializers import RatingSerializer
from rest_framework import viewsets
from .models import Rating


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer

    def get_queryset(self):
        ratings = Rating.objects.filter(user=self.request.user)
        return ratings

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
