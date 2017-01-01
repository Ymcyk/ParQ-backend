import re

from django.http import Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from users.models import Driver

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
    try:
        driver = Driver.objects.get(pk=request.user.id)
    except Driver.DoesNotExist:
        return Response({'owner':'Only drivers'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        tickets = Ticket.objects.filter(vehicle__owner=driver)
        badge = request.query_params.get('badge', None)
        if badge:
            regex = '{0}{{8}}-{0}{{4}}-{0}{{4}}-{0}{{4}}-{0}{{12}}'.format('[a-f0-9]')
            if not bool(re.search(regex, badge)):
                return Response('Bad badge id', status=status.HTTP_406_NOT_ACCEPTABLE)
            tickets = tickets.filter(vehicle__badge__uuid=badge)
            now = timezone.now()
            tickets = tickets.filter(end__gte=now).filter(start__lte=now)
        serializer = TicketResponseSerializer(tickets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

