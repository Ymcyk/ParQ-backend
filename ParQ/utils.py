import pytz

from django.conf import settings

ew_timezone = pytz.timezone('Europe/Warsaw')

def utc_to_warsaw(utc_dt):
    return utc_dt.astimezone(ew_timezone)

def warsaw_to_utc(ew_dt):
    return ew_dt.astimezone(pytz.utc)

def naive_to_utc(naive):
    return pytz.utc.localize(naive)

def occurrence_to_schedule(occurrence):
    schedule = occurrence.event.schedule
    schedule.start = occurrence.start
    schedule.end = occurrence.end
    return schedule
