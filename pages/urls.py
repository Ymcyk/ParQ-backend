from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name='pages'
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^myaccount/$', login_required(views.MyAccount.as_view()), name='myaccount'),
    url(r'^downloadqr/(?P<id>[0-9]+)$', login_required(views.download_qr), name='downloadqr'),
]
