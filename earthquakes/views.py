from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Earthquake
from .serializers import EarthquakeSerializer
from .filters import EarthquakeFilter

class EarthquakeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Earthquake.objects.all() # Seleciona todos os registros de Earthquake
    serializer_class = EarthquakeSerializer # converte cada objeto Earthquake desse queryset em JSON
    filterset_class = EarthquakeFilter
    filter_backends = [DjangoFilterBackend]