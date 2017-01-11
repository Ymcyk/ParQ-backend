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
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        print('username:', username, 'email:', email, 'password:', password)
        user = User.objects.create_user(username=username, email=email, password=password)
        driver = Driver.objects.create(user=user)
        return driver

