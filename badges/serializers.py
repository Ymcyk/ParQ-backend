from rest_framework import serializers

from users.models import Driver
from .models import Badge, Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
            read_only=True,
            )
    badge = serializers.SlugRelatedField(
            slug_field='uuid',
            queryset=Badge.objects.all(),
            required=False,
            )
    plate_number = serializers.CharField(
            max_length=20
            )
    plate_country = serializers.CharField(
            max_length=3, 
            required=False
            )

    class Meta:
        model = Vehicle
        fields = ('id', 'owner', 'badge', 'name', 'plate_country', 'plate_number')
        read_only_fields = ('id', 'owner')

    def create(self, validated_data):
        vehicle = Vehicle(
                owner=validated_data['owner'],
                badge=validated_data['badge'],
                name=validated_data['name'],
                plate_number=validated_data['plate_number'],
                )
        if 'plate_country' in validated_data:
            vehicle.plate_country = validated_data['plate_country']
        vehicle.save()
        return vehicle

