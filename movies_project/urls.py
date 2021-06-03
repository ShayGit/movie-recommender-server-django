from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('auth.urls')),
    path('api/', include('ratings.urls')),
    path('api/', include('recommender.urls')),
    path('api/', include(router.urls)),
]
