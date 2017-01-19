from django.utils import timezone
from datetime import timedelta

from schedule.periods import Day
from rest_framework import serializers

from badges.models import Vehicle
from badges.serializers import VehicleSerializer
from .models import Parking, Ticket

class ParkingSerializer(serializers.ModelSerializer):
    open = serializers.SerializerMethodField('get_hours_for_parking')

    def get_hours_for_parking(self, obj):
        now = timezone.now()
        occurrences = Day(obj.schedule_lot.schedule_set.all(), now).get_occurrences()
        schedule = occurrences[0] if occurrences else None

        if schedule:
            #start = '{0}:{1}Z'.format(schedule.start.hour, schedule.start.minute)
            #end = '{0}:{1}Z'.format(schedule.end.hour, schedule.end.minute)

            hours = {'start': schedule.start, 'end': schedule.end}
        else:
            hours = dict()
        return hours

    class Meta:
        model = Parking
        fields = ('id', 'name', 'description', 'open')
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
    minutes = serializers.IntegerField(
            min_value=1,
            )

    class Meta:
        model = Ticket
        fields = ('minutes', 'vehicle', 'parking')

    def create(self, validated_data):
        start = timezone.now()
        end = start + timedelta(minutes=validated_data['minutes'])
        return Ticket.objects.create(
                    start = start,
                    end = end,
                    vehicle = validated_data['vehicle'],
                    parking = validated_data['parking']
                )
