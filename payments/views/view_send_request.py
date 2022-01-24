from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from dashboard.models import Installment
from dashboard.models.discount import Discount
from payments.enums import *
from core.utils.textutils import TextUtils
# from accounts.enums import Sms
# from core.webServices import SmsWebServices
from django.urls import reverse

from payments.models.pay_history import Pay_History
import logging
import json

from payments.views.view_compute_discount import compute_discount

logger = logging.getLogger("django")


# compare amount of request with courses
def is_valid(installments_id_list, amount, discount):
    installments = Installment.objects.filter(id__in=installments_id_list)
    total_price = 0
    for installment in installments:
        total_price += installment.amount_payable
    if discount:
        total_price = total_price - compute_discount(installments_id_list, total_price, discount)
    return True if int(total_price) == amount else False


class SendRequest(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def post(self, request):
        user = request.user
        installments_id_list = json.loads(request.data["total_id"])
        try:
            amount = int(float(request.data["total_pr"]))
            code = request.data['code']
            if request.session.get('event_discount'):
                discount = Discount()
                discount.percent = Events[request.session.get('event_discount') + "_DISCOUNT"].value
            else:
                if code and code != '':
                    query = discount_query(code)
                    # query &= (Q(courses__id__in=courses_id_list) | Q(courses=None))
                    discount = Discount.objects.get(query)
                else:
                    discount = None
        except:
            discount = None
        if installments_id_list and is_valid(installments_id_list, amount, discount):
            # handel free courses
            if amount == 0:
                for installment_id in installments_id_list:
                    user.installments.add(installment_id)
                user.save()
                # if request.accepted_renderer.format == 'html':
                return Response({'message': 'خرید موفق'}, status=status.HTTP_201_CREATED)
            # request to zarinpal
            else:
                description = pay_description(installments_id_list, amount, discount, request)
                try:
                    url = request.data['url']
                except:
                    url = request.build_absolute_uri(reverse('payment_verify'))
                result = client.service.PaymentRequest(
                    MERCHANT.merchant.value, amount, description, '', '', url)
                if result.Status == 100:
                    Pay_History.objects.create(purchaser=request.user, amount=amount,
                                               installments=TextUtils.convert_list_to_string(
                                                   installments_id_list, " "))
                    return Response({'url': 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)})
                else:
                     return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
