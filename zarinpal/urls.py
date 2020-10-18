from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('get-installment', GetInstallmentViewSet)

urlpatterns = [
    path('request/', SendRequest.as_view(), name='payment_request'),
    path('verify/', Verify.as_view(), name='payment_verify'),
    path('compute-discount/', ComputeDiscount.as_view(), name='compute_discount'),
    path('shopping-cart/', shopping_cart, name="shopping_cart"),

]
urlpatterns += router.urls
