from rest_framework import filters
from django_filters import rest_framework as django_filters
from .models import FederatedLearningResult
from .serializers import FederatedLearningResultSerializer

# Filter class for FederatedLearningResult
class FederatedLearningResultFilter(django_filters.FilterSet):
    metrics = django_filters.CharFilter(field_name='metrics', lookup_expr='icontains')
    processed_time = django_filters.DateTimeFilter(field_name='processed_time', lookup_expr='gte')  # Filter by date range
    model_path = django_filters.CharFilter(field_name='model_path', lookup_expr='icontains')

    class Meta:
        model = FederatedLearningResult
        fields = ['metrics', 'processed_time', 'model_path']
