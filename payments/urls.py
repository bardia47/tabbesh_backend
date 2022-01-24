from django.urls import path
from payments.views.view_installment import *
from rest_framework.routers import DefaultRouter
from .views.view_compute_discount import ComputeDiscountView
#from .views.view_installment import InstallmentViewSet
from .views.view_send_request import SendRequest
from .views.view_verify_request import VerifyView
router = DefaultRouter()
#router.register('installments',InstallmentViewSet)

urlpatterns = [
    path('request/', SendRequest.as_view(), name='payment_request'),
    path('verify/', VerifyView.as_view(), name='payment_verify'),
    path('compute-discount/', ComputeDiscountView.as_view(), name='compute_discount'),
  #  path('shopping-cart/', shopping_cart, name="shopping_cart"),

]
urlpatterns += router.urls
