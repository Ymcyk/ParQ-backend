from rest_framework import serializers

from users.models import Driver
from .models import Badge, Vehicle

#class BadgeSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Badge
#        fields = ('uuid',)
#        read_only_fields = ('uuid',)

class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
            queryset=Driver.objects.all()
            )
    badge = serializers.SlugRelatedField(
            slug_field='uuid',
            queryset=Badge.objects.all()
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
        read_only_fields = ('id',)

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

