
from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^request/$', SendRequest.as_view(), name='payment_request'),
    url(r'^verify/$', Verify.as_view(), name='payment_verify'),
]
