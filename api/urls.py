from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

from users.views import register_driver, driver_detail, current_user, ParQAuthToken 
from badges.views import VehicleDetail, VehicleList
from parkings.views import ParkingList, TicketList
from paypal.views import payment_list 
from charges.views import schedule_list

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/', ParQAuthToken.as_view()),
    url(r'^register/$', register_driver),
    url(r'^drivers/(?P<pk>[0-9]+)$', driver_detail),
    url(r'^vehicles/$', VehicleList.as_view()),
    url(r'^vehicles/(?P<pk>[0-9]+)$', VehicleDetail.as_view()),
    url(r'^parkings/$', ParkingList.as_view()),
    url(r'^tickets/$', TicketList.as_view()),
    url(r'^current/$', current_user),
    url(r'^payments/$', payment_list),
    url(r'^schedules/$', schedule_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)

