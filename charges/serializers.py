from rest_framework import serializers

from .models import Schedule, Charge

class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = ('cost', 'minutes', 'duration', 'minute_billing')

class ScheduleSerializer(serializers.ModelSerializer):
    charges = ChargeSerializer(many=True)

    class Meta:
        model = Schedule
        fields = ('start', 'end', 'charges')

