"""
Z założenie, wszystkie daty podawane są w UTC. W Androidzie jedynie podczas
pobierania daty od użytkownika pamiętać o odpowiednich transformacjach strefy!
"""
import re
from datetime import timedelta

from django.http import Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from djroles.models import Role
from users.models import Driver, Officer
from users.exceptions import NotEnoughMoney
from charges.exceptions import TicketNotInSchedule, NoSchedule

from .models import Parking, Ticket
from .serializers import ParkingSerializer, TicketSerializer, TicketResponseSerializer

class ParkingList(APIView):
    """
    List of all parkings
    """
    def get(self, request, format=None):
        parkings = Parking.objects.all()
        serializer = ParkingSerializer(parkings, many=True)
        return Response(serializer.data)

class TicketList(APIView):
    def get(self, request, format=None):
        tickets = Ticket.objects.all()
        badge = request.query_params.get('badge', None)
        # parking = request.query_params.get('parking', None)

        if Role.has_role(request.user, Officer):
            if not badge:
                return Response({'params': 'badge is required'}, status=status.HTTP_400_BAD_REQUEST)
            #tickets = self.officer_request(tickets, badge)
            regex = '{0}{{8}}-{0}{{4}}-{0}{{4}}-{0}{{4}}-{0}{{12}}'.format('[a-f0-9]')
            if not bool(re.search(regex, badge)):
                return Response('Bad badge id', status=status.HTTP_406_NOT_ACCEPTABLE)
            tickets = tickets.filter(vehicle__badge__uuid=badge)
            #print('tickets:', tickets)
            now = timezone.now()
            tickets = tickets.filter(end__gte=now).filter(start__lte=now)

        elif Role.has_role(request.user, Driver):
            #if not parking:
            #    return Response({'params': 'parking is required'}, status=status.HTTP_400_BAD_REQUEST)
            tickets = self.driver_request(tickets, request.user.id)
        else:
            return Response({'user':'Bad role'}, status=status.HTTP_403_FORBIDDEN)

        serializer = TicketResponseSerializer(tickets, many=True)
        return Response(serializer.data)
    
    def driver_request(self, tickets, user_id):
        driver = Driver.objects.get(pk=user_id)
        # tickets = tickets.filter(vehicle__owner=driver).filter(parking__id=parking)
        tickets = tickets.filter(vehicle__owner=driver)
        now = timezone.now()
        return tickets.filter(end__gte=now)

    def officer_request(self, tickets, badge):
        regex = '{0}{{8}}-{0}{{4}}-{0}{{4}}-{0}{{4}}-{0}{{12}}'.format('[a-f0-9]')
        if not bool(re.search(regex, badge)):
            return Response('Bad badge id', status=status.HTTP_406_NOT_ACCEPTABLE)
        tickets = tickets.filter(vehicle__badge__uuid=badge)
        #print('tickets:', tickets)
        now = timezone.now()
        return tickets.filter(end__gte=now).filter(start__lte=now)

    def post(self, request, format=None):
        if not Role.has_role(request.user, Driver):
            return Response({'user':'Bad role'}, status=status.HTTP_403_FORBIDDEN)
        serializer = TicketSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except NotEnoughMoney:
            return Response({'user': 'Not enough money'}, status=status.HTTP_403_FORBIDDEN)
        except TicketNotInSchedule:
            return Response({'ticket': 'Ticket start date is later than schedule end date'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except NoSchedule:
            return Response({'schedule': 'No schedule for given date'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

