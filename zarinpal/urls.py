from django.urls import path
from .views import *


urlpatterns = [
    path('request/', SendRequest.as_view(), name='payment_request'),
    path('verify/', Verify.as_view(), name='payment_verify'),
]
