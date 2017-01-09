"""ParQ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

from users.views import register_driver, driver_detail, current_user, ParQAuthToken 
from badges.views import vehicle_detail, vehicle_list
from parkings.views import parking_list, ticket_list
from paypal.views import payment_list 
from charges.views import schedule_list

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api-token-auth/', ParQAuthToken.as_view()),
    url(r'^register/$', register_driver),
    url(r'^drivers/(?P<pk>[0-9]+)$', driver_detail),
    url(r'^vehicles/$', vehicle_list),
    url(r'^vehicles/(?P<pk>[0-9]+)$', vehicle_detail),
    url(r'^parkings/$', parking_list),
    url(r'^tickets/$', ticket_list),
    url(r'^current/$', current_user),
    url(r'^payments/$', payment_list),
    url(r'^schedules/$', schedule_list),
    #url(r'^admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# logowanie, zostanie zwrócony token
# curl --data "username=pateto&password=piotr213243" localhost:8000/api-token-auth/

# żądanie GET
# curl -i -H "Accept: application/json" "localhost:8000/drivers/"

# dodawania kierowcy
# curl -H "Content-Type: application/json" -X POST -d '{"user":{"username":"ymcyk", "email":"thepateto@gmail.com", "password":"piotr213243"}}' http://localhost:8000/register/

