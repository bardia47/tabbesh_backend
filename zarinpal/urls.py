from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^request/$', views.send_request, name='payment_request'),
    url(r'^verify/$', views.verify, name='payment_verify'),
]
