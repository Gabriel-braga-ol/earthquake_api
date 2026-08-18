from rest_framework.routers import DefaultRouter
from .views import EarthquakeViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'earthquakes', EarthquakeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]