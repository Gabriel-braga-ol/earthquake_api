import django_filters
from .models import Earthquake

class EarthquakeFilter(django_filters.FilterSet):
    min_magnitude = django_filters.NumberFilter(field_name='magnitude', lookup_expr='gte')
    place = django_filters.CharFilter(field_name='place', lookup_expr='icontains')
    start_date = django_filters.DateTimeFilter(field_name='time', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='time', lookup_expr='lte')

    class Meta:
        model = Earthquake
        fields = ['min_magnitude', 'place', 'start_date', 'end_date']