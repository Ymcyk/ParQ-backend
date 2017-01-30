from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse
from wsgiref.util import FileWrapper
#import mimetypes

from users.models import Driver
from badges.models import Badge

class Index(View):
    def get(self, request):
        context = {
                'title': 'ParQ',
                'nbar': 'index',
                }
        return render(request, 'pages/index.html', context)

class MyAccount(View):
    def get(self, request, *args, **kwargs):

        context = {
                'nbar': 'myaccount'
                }

        context['vehicles'] = []

        try:
            driver = Driver.objects.get(pk=request.user.id)
        except Driver.DoesNotExist:
            return render(request, 'pages/myaccount.html', context)

        context['vehicles'] = driver.vehicle_set.all()

        return render(request, 'pages/myaccount.html', context)

def download_qr(request, id):
    badge =  get_object_or_404(Badge, pk=id)
    badge_url = badge.path_to_file()
    try:
        wrapper = FileWrapper(open(badge_url, 'rb'))
    except FileNotFoundError:
        badge.generate_image()
        wrapper = FileWrapper(open(badge_url, 'rb'))
    response = HttpResponse(wrapper, content_type='image/png')
    return response
