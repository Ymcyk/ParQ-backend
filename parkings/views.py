import re

from django.http import Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from users.models import Driver
from users.exceptions import NotEnoughMoney

from .models import Parking, Ticket
from .serializers import ParkingSerializer, TicketSerializer, TicketResponseSerializer

@api_view(['GET'])
def parking_list(request, format=None):
    if request.method == 'GET':
        vehicles = Parking.objects.all()
        serializer = ParkingSerializer(vehicles, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def ticket_list(request, format=None):
    
    if request.method == 'GET':
        tickets = Ticket.objects.all()
        badge = request.query_params.get('badge', None)
        parking = request.query_params.get('parking', None)
        if badge:
            regex = '{0}{{8}}-{0}{{4}}-{0}{{4}}-{0}{{4}}-{0}{{12}}'.format('[a-f0-9]')
            if not bool(re.search(regex, badge)):
                return Response('Bad badge id', status=status.HTTP_406_NOT_ACCEPTABLE)
            tickets = tickets.filter(vehicle__badge__uuid=badge)
            now = timezone.now()
            tickets = tickets.filter(end__gte=now).filter(start__lte=now)
        elif parking:
            try:
                driver = Driver.objects.get(pk=request.user.id)
            except Driver.DoesNotExist:
                return Response({'owner':'Only drivers'}, status=status.HTTP_403_FORBIDDEN)
            tickets = tickets.filter(vehicle__owner=driver).filter(parking__id=parking)
            now = timezone.now()
            tickets = tickets.filter(end__gte=now)
        else:
            return Response({'params': 'badge or parking'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TicketResponseSerializer(tickets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            driver = Driver.objects.get(pk=request.user.id)
        except Driver.DoesNotExist:
            return Response({'owner':'Only drivers'}, status=status.HTTP_403_FORBIDDEN)

        print(request.data)
        serializer = TicketSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except NotEnoughMoney:
            return Response({'user': 'Not enough money'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

