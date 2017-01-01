from django.db.utils import IntegrityError

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view

from users.models import Driver
from users.utils import send_badge

from .models import Badge, Vehicle
from .serializers import VehicleSerializer

@api_view(['GET', 'POST'])
def vehicle_list(request, format=None):
    try:
        driver = Driver.objects.get(pk=request.user.id)
    except Driver.DoesNotExist:
        return Response({'owner':'Only drivers'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        vehicles = Vehicle.objects.filter(owner=driver)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            if 'badge' not in request.data:
                badge = Badge.objects.create()
                serializer.save(owner=driver, badge=badge)
                # wysyłanie maila do użytkownika
                send_badge(request.user.email, badge)
            else:
                try:
                    print('JESTEM TUTAJ')
                    serializer.save(owner=driver)
                except IntegrityError:
                    Response({'badge':'Is already used'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def vehicle_detail(request, pk, format=None):
    try:
        driver = Driver.objects.get(pk=request.user.id)
    except Driver.DoesNotExist:
        return Response({'owner':'Only drivers'}, status=status.HTTP_403_FORBIDDEN)

    try:
        vehicle = Vehicle.objects.get(pk=pk)
    except Vehicle.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if vehicle.owner != driver:
        return Response({'vehicle':'Not owner'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

