from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Driver

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ('user', 'wallet')
        read_only_fields = ('wallet',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        driver = Driver.objects.create(user=user)
        return driver

    #def update(self, instance, validated_data):
    #    user_data = validated_data.pop('user')
    #    user = instance.user

