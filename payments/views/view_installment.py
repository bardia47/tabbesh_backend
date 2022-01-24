from rest_framework import viewsets
from dashboard.models import Installment, Course
from payments.serializers.serializer_shopping import *
from core.filters import *

import datetime

#
#
# class InstallmentViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#                 add list of installmentIds to params
#           """
#     queryset = Course.objects.all()
#     serializer_class = ShoppingCartSerializer
#     filter_backends = [ListFilter]
#     search_fields = ['id']
#     SEARCH_PARAM = 'id'
#     pagination_class = None
#
#     def get_queryset(self):
#         if self.request.GET.get(self.SEARCH_PARAM) not in (None, '','[]'):
#             return super(InstallmentViewSet, self).get_queryset()
#         now = datetime.datetime.now()
#         installments = Installment.objects.all().exclude(user=self.request.user)
#         courses = self.request.user.courses().filter(installment__in=installments).distinct()
#         return courses
