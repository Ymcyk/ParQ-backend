from rest_framework import serializers

from badges.models import Vehicle
from badges.serializers import VehicleSerializer
from .models import Parking, Ticket

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ('id', 'name', 'description')
        read_only_fields = fields

class TicketResponseSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()
    parking = ParkingSerializer()

    class Meta:
        model = Ticket
        fields = ('start', 'end', 'vehicle', 'parking', 'price')

class TicketSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(
            queryset=Vehicle.objects.all()
            )
    parking = serializers.PrimaryKeyRelatedField(
            queryset=Parking.objects.all()
            )

    class Meta:
        model = Ticket
        fields = ('start', 'end', 'vehicle', 'parking', 'price')
        read_only_fields = ('price',)

    def create(self, validated_data):
        return Ticket.objects.create(
                    start = validated_data['start'],
                    end = validated_data['end'],
                    vehicle = validated_data['vehicle'],
                    parking = validated_data['parking']
                )
