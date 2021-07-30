from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
router = DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Movies Recommendation System API",
      default_version='v1',
      contact=openapi.Contact(email="shay291@gmail.com")
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('auth.urls')),
    path('api/', include('ratings.urls')),
    path('api/', include('recommender.urls')),
    path('api/', include(router.urls)),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
