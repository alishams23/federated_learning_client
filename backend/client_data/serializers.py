
from .models import ClientData
from rest_framework import serializers


class ClientDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ClientData
        fields = '__all__'