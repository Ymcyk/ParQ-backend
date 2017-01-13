import re
from datetime import datetime

from django.utils.timezone import make_aware

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from schedule.periods import Day

from parkings.models import Parking
from ParQ.utils import occurrence_to_schedule 

from .serializers import ScheduleSerializer
from .exceptions import *

@api_view(['GET'])
def schedule_list(request, format=None):
    req_date = request.query_params.get('date', None)
    req_parking = request.query_params.get('parking', None)
    if req_date and req_parking:
        regex = '(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
        match = re.search(regex, req_date)
        if not match:
             return Response({'params': 'Bad date format'}, 
                status=status.HTTP_400_BAD_REQUEST)
        date = make_aware(datetime(int(match.group('year')),
                                   int(match.group('month')),
                                   int(match.group('day'))))
        print('aware_date:', date)
        try:
            parking = Parking.objects.get(pk=req_parking)
        except Parking.DoesNotExist:
            return Response({'parking': 'Parking with this id does not exist'},
                    status=status.HTTP_406_NOT_ACCEPTABLE)
        #occurrences = schedule_for_parking(parking, date)
        #print('occurrences:', occurrences)
        try:
            schedule = parking.schedule_lot.get_schedule_for_date(date)
            serializer = ScheduleSerializer(schedule)
            return Response(serializer.data)
        except NoSchedule:
            return Response(status=status.HTTP_204_NO_CONTENT)

        #if len(occurrences) == 0:
        #    return Response(status=status.HTTP_204_NO_CONTENT)
        #else:
        #    schedule = occurrence_to_schedule(occurrences[0])
        #    serializer = ScheduleSerializer(schedule)
        #    return Response(serializer.data)
    else:
        return Response({'params': 'Date and parking params are required'}, 
                status=status.HTTP_400_BAD_REQUEST)

#def schedule_for_parking(parking, date):
    #schedules = parking.schedule_lot.schedule_set.all()
    
    #occurrences = Day(schedules, date).get_occurrences()
    #return occurrences
