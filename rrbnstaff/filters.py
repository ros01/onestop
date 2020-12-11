from fleet.models import Vehicle
import django_filters

class VehicleFilter(django_filters.FilterSet):
    class Meta:
        model = Vehicle
        fields = ['location', 'interstate_trip',]

   