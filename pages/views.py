from django.shortcuts import render
from django.views import View

class Index(View):
    def get(self, request):
        parking = Parking.objects.all()[0]
        schedules = parking.schedule_lot.schedule_set.all()
        context = {
                'title': 'ParQ',
                }
        return render(request, 'pages/index.html', context)

