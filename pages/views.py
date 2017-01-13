from django.shortcuts import render
from django.views import View

from parkings.models import Parking

class Index(View):
    def get(self, request):
        parking = Parking.objects.all()[0]
        schedules = parking.schedule_lot.schedule_set.all()
        context = {
                'parking': parking,
                'schedules': schedules,
                }
        return render(request, 'pages/index.html', context)

