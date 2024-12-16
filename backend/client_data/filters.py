
from django_filters import rest_framework as django_filters

from .models import ClientData

class ClientDataFilter(django_filters.FilterSet):
    upload_time = django_filters.DateFromToRangeFilter()

    class Meta:
        model = ClientData
        fields = ['upload_time']