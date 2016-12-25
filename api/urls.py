from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from users.views import DriverDetail

urlpatterns = [
    url(r'^drivers/(?P<pk>[0-9]+)$', DriverDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
