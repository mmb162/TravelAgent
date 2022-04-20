from . models import Itinerary
import django_filters
from django_filters.filters import RangeFilter

# Creating product filters
class ItineraryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Itinerary
        fields = ['name', 'description']