from django.http import Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Parking, Ticket
from .serializers import ParkingSerializer, TicketSerializer

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
        valid = request.query_params.get('valid', None)
        if badge:
            tickets = tickets.filter(vehicle__badge__uuid=badge)
            if valid:
                now = timezone.now()
                tickets = tickets.filter(end__gte=now).filter(start__lte=now)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

