from rest_framework import serializers
from .models import FederatedLearningResult

class FederatedLearningResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FederatedLearningResult
        fields = '__all__'
