from rest_framework import serializers
from .models import Property, ListedProperty, UserProfile
from django.contrib.auth.models import User

class ListedPropertySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = ListedProperty
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'
