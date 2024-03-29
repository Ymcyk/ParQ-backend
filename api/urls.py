from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

from users.views import RegisterDriver, CurrentUser, ParQAuthToken 
from badges.views import VehicleDetail, VehicleList
from parkings.views import ParkingList, TicketList
from paypal.views import payment_list 
from charges.views import ScheduleList

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/', ParQAuthToken.as_view()),
    url(r'^register/$', RegisterDriver.as_view()),
    url(r'^vehicles/$', VehicleList.as_view()),
    url(r'^vehicles/(?P<pk>[0-9]+)$', VehicleDetail.as_view()),
    url(r'^parkings/$', ParkingList.as_view()),
    url(r'^tickets/$', TicketList.as_view()),
    url(r'^current/$', CurrentUser.as_view()),
    url(r'^payments/$', payment_list),
    url(r'^schedules/$', ScheduleList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

