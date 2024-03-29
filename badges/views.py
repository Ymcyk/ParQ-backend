from django.db.utils import IntegrityError

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

from users.models import Driver
from users.utils import send_badge

from .models import Badge, Vehicle
from .serializers import VehicleSerializer

class VehicleList(APIView):
    """
    List of vehicles. Access only for drivers
    """
    def retrive_driver(self, user):
        try:
            self.driver = Driver.objects.get(pk=user.id)
        except Driver.DoesNotExist:
            return Response({'owner':'Only drivers'}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, format=None):
        self.retrive_driver(request.user)
        vehicles = Vehicle.objects.filter(owner=self.driver)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        self.retrive_driver(request.user)
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            if 'badge' not in request.data:
                badge = Badge.objects.create()
                serializer.save(owner=self.driver, badge=badge)
                # wysyłanie maila do użytkownika
                try:
                    send_badge(request.user.email, badge, request.data['plate_number'])
                except ConnectionRefusedError:
                    print('Email z kodem QR nie został wysłany. Odmowa serwera')
            else:
                try:
                    serializer.save(owner=self.driver)
                except IntegrityError:
                    Response({'badge':'Is already used'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehicleDetail(APIView):
    """
    Now only delete method
    """
    def retrive_driver(self, user):
        try:
            self.driver = Driver.objects.get(pk=user.id)
        except Driver.DoesNotExist:
            return Response({'owner':'Only drivers'}, status=status.HTTP_403_FORBIDDEN)

    def retrive_vehicle(self, vehicle_id):
        try:
            self.vehicle = Vehicle.objects.get(pk=vehicle_id)
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk, format=None):
        self.retrive_driver(request.user)
        self.retrive_vehicle(pk)
        if self.vehicle.owner != self.driver:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

