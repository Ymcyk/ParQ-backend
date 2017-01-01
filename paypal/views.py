from decimal import Decimal

from django.http import Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from .models import Transaction
from .serializers import TransactionSerializer

from paypal.utils import get_payment_money
from users.models import Driver
from users.serializers import DriverSerializer

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def payment_list(request):
    serializer = TransactionSerializer(data=request.data)
    print('Dane:', request.data)
    if serializer.is_valid():
        try:
            driver = Driver.objects.get(pk=request.user.id)
        except Driver.DoesNotExist:
            return Response('User is not driver', status=status.HTTP_403_FORBIDDEN)

        serializer.save(user=request.user)
        # money = get_payment_money(request.data['transaction_id'])

        money = request.data['money']
        driver.add_money(Decimal(money))
        driver.save()
        driver_ser = DriverSerializer(driver)
        return Response(driver_ser.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

