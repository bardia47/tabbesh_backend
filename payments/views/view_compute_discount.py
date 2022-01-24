from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dashboard.models import Installment
from dashboard.models.discount import Discount
from payments.enums import *
from core.utils.textutils import TextUtils
from payments.serializers.serializer_shopping import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import datetime
import json


# compute discount code
class ComputeDiscountView(APIView):

    def get_discount(self, request):
        code = request.GET.get('code')
        query = discount_query(code)
        if request.session.get('event_discount'):
            discount = Discount()
            discount.percent = Events[request.session.get('event_discount') + "_DISCOUNT"].value
        else:
            discount = Discount.objects.get(query)
        return discount

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(name='total_id', in_=openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING,
                          description='this is list of installment id', format='[1,2,3,5]'),
        openapi.Parameter(name='code', in_=openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING,
                          description='this is discount code'),
        openapi.Parameter(name='total_pr', in_=openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING,
                          description='this is sum amount of installments')
    ]
    )
    def get(self, request):
        installments_list = json.loads(request.GET.get("totalId"))
        try:
            discount = self.get_discount(request)
        except:
            return Response({'message': PaymentMassages.discountErrorMassage.value},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        amount = int(float(request.GET.get('total_pr')))
        discount_amount = compute_discount(installments_list, amount, discount)
        if discount_amount == 0:
            return Response({'message': PaymentMassages.discountErrorMassage.value},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        amount = amount - discount_amount
        return Response({'amount': amount, 'message': PaymentMassages.discountMassage.value})


# query to find discount
def discount_query(code):
    now = datetime.datetime.now()
    query = Q(start_date__lte=now)
    query &= Q(code=code)
    query &= (Q(end_date__gte=now) | Q(end_date=None))
    return query


def compute_discount(installments_id_list, amount, discount):
    if discount.id is None or discount.courses.count() == 0:
        return amount * discount.percent / 100
    else:
        installments = Installment.objects.filter(id__in=installments_id_list, course__discount__id=discount.id)
        sum_amount = 0
        for installment in installments:
            sum_amount += installment.amount_payable
        return sum_amount * discount.percent / 100


# pay desc for zarinpal
# in this method use replacer for create dynamic text
def pay_description(installments_id_list, discount, request):
    text = ZarinPal.descriptionText.value
    if discount:
        discount_text = ZarinPal.dicountText.value.format(*[discount.code])
    else:
        discount_text = ''
    text = text.format(*[TextUtils.convert_list_to_string(
        list(Course.objects.filter(installment__in=installments_id_list).values_list('title', flat=True))),
        discount_text,
        request.user.get_full_name()])
    return text
