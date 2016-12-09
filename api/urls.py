from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from users.views import DriverList

urlpatterns = [
    url(r'^drivers/$', DriverList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
