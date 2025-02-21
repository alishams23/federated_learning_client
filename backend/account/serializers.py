from .models import User
from rest_framework import serializers


class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)  # Email is now required
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'A user with this email already exists.'})
        
        user = User.objects.create_user(**validated_data)
        return user
