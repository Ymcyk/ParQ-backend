from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
            read_only=True,
            )

    class Meta:
        model = Transaction
        fields = ('id', 'user', 'transaction_id')
        read_only_fields = ('id', 'user')

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

