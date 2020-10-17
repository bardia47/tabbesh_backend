from django.shortcuts import render
from django.shortcuts import redirect
from zeep import Client
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status, viewsets
from .enums import *
from core.utils import TextUtils
from accounts.enums import Sms
from core.webServices import SmsWebServices
from django.urls import reverse
from .serializers import *
from core.filters import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import datetime
import logging
import json

# TODO change app name to payments

logger = logging.getLogger("django")
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')


# compare amount of request with courses
def is_valid(installments_id_list, amount, discount):
    installments = Installment.objects.filter(id__in=installments_id_list)
    total_price = 0
    for installment in installments:
        total_price += installment.get_amount_payable()
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
                return render(request, 'dashboard/success_shopping.html')
                # return Response({'message': 'خرید موفق'}, status=status.HTTP_201_CREATED)

            # request to zarinpal
            else:
                description = pay_description(installments_id_list, amount, discount, request)
                try:
                    url = request.data['url']
                except:
                    # url = request.scheme + "://" + request.get_host() + reverse('payment_verify')
                    url = request.build_absolute_uri(reverse('payment_verify'))
                result = client.service.PaymentRequest(
                    MERCHANT.merchant.value, amount, description, '', '', url)
                if result.Status == 100:
                    new_pay = Pay_History.objects.create(purchaser=request.user, amount=amount,
                                                         installments=TextUtils.convert_list_to_string(
                                                             installments_id_list, " "))
                    # if request.accepted_renderer.format == 'html':
                    return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
                    # else:
                    #     return Response({'url': 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)})
                else:
                    # if request.accepted_renderer.format == 'html':
                    return render(request, 'dashboard/unsuccess_shopping.html', {'error': str(result.Status)})
                # else:
                #     return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            # if request.accepted_renderer.format == 'html':
            return redirect('/dashboard/shopping/')  # what's up noob :)
        # return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class Verify(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        try:
            new_pay = Pay_History.objects.filter(purchaser=request.user, submit_date__isnull=True).first()
            if new_pay is None:
                raise Exception('تراکنش انجام شده')
        except:
            if request.accepted_renderer.format == 'html':
                return render(request, 'dashboard/success_shopping.html', {'RefID': "تراکنش انجام شده"})
            return Response({'RefID': "تراکنش انجام شده"}, status=status.HTTP_226_IM_USED)
        now = datetime.datetime.now()
        new_pay.submit_date = now
        if request.GET.get('Status') == 'OK':
            result = client.service.PaymentVerification(
                MERCHANT.merchant.value, request.GET.get('Authority'), new_pay.amount)
            if result.Status == 100:
                installment_id_list = new_pay.installments.split()
                user = request.user
                for installment_id in installment_id_list:
                    user.installments.add(installment_id)
                user.save()
                new_pay.is_successful = True
                new_pay.payment_code = str(result.RefID)
                new_pay.save()
                # this try is for events
                try:
                    event = Event.objects.get(user__id=request.user.id, is_active=True)
                    event.is_active = False
                    event.save()
                    related_user = event.related_user
                    related_user.credit += float(Events[event.type + "_AMOUNT"].value)
                    related_user.save()
                    to = "0" + related_user.phone_number
                    text = TextUtils.replacer(Sms.increaseCreditText.value, [str(Events[event.type + "_AMOUNT"].value),
                                                                             str(int(related_user.credit))])
                    sendSms = SmsWebServices.send_sms(to, text, None)
                    if sendSms is not None:
                        logger.error("danger: " + sendSms)
                    del request.session['event_discount']
                except Exception as e:
                    logger.error("this pay don't have event")
                if request.accepted_renderer.format == 'html':
                    return render(request, 'dashboard/success_shopping.html', {'RefID': str(result.RefID)})
                return Response({'RefID': str(result.RefID)})
            elif result.Status == 101:
                # return HttpResponse('Transaction submitted : ' + str(result.Status))
                new_pay.is_successful = True
                new_pay.save()
                if request.accepted_renderer.format == 'html':
                    return render(request, 'dashboard/success_shopping.html', {'RefID': "تراکنش انجام شده"})
                return Response({'RefID': "تراکنش انجام شده"}, status=status.HTTP_226_IM_USED)
            else:
                new_pay.save()
                # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
                if request.accepted_renderer.format == 'html':
                    return render(request, 'dashboard/unsuccess_shopping.html', {'error': str(result.Status)})
                return Response({'error': "پرداخت ناموفق"}, status.HTTP_406_NOT_ACCEPTABLE)

        else:
            new_pay.save()
            # return HttpResponse('Transaction failed or canceled by user')
            if request.accepted_renderer.format == 'html':
                return render(request, 'dashboard/unsuccess_shopping.html')
            return Response({'error': "پرداخت ناموفق"}, status.HTTP_406_NOT_ACCEPTABLE)


# compute discount code
class ComputeDiscount(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

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
        installments_list = json.loads(request.GET.get("total_id"))
        code = request.GET.get('code')
        query = discount_query(code)
        # query &= (Q(courses__id__in=courses_id_list) | Q(courses=None))
        try:
            if request.session.get('event_discount'):
                discount = Discount()
                discount.percent = Events[request.session.get('event_discount') + "_DISCOUNT"].value
            else:
                discount = Discount.objects.get(query)
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
            sum_amount += installment.get_amount_payable()
        return sum_amount * discount.percent / 100


# pay desc for zarin pal
# in this method use replacer for create dynamic text
def pay_description(installments_id_list, amount, discount, request):
    text = ZarinPal.descriptionText.value

    if request.session.get('event_discount'):
        event = Event.objects.get(type=request.session.get('event_discount'), user__id=request.user.id)
        related_user = ''
        if event.related_user is not None:
            related_user = TextUtils.replacer(ZarinPal.relatedPersonText.value, [event.related_user.get_full_name()])
        discount_text = TextUtils.replacer(ZarinPal.eventText.value, [
            event.get_type_display(), related_user,
            str(discount.percent)])
    elif discount:
        discount_text = TextUtils.replacer(ZarinPal.dicountText.value, [discount.code])
    else:
        discount_text = ''
    text = TextUtils.replacer(text, [TextUtils.convert_list_to_string(
        list(Course.objects.filter(installment__in=installments_id_list).values_list('title', flat=True))),
        discount_text,
        request.user.get_full_name()])
    return text


def shopping_cart(request):
    try:
        # for first pay of introducing
        event = Event.objects.get(user__id=request.user.id, type=Event.Introducing, is_active=True)
        request.session['event_discount'] = event.type
    except:
        pass
    return render(request, 'dashboard/shopping-cart.html')


class GetInstallmentViewSet(viewsets.ModelViewSet):
    """
                add list of installmentIds to params
          """
    queryset = Course.objects.all()
    serializer_class = ShoppingCartSerializer
    filter_backends = [ListFilter]
    search_fields = ['id']
    SEARCH_PARAM = 'id'
    http_method_names = ['get', ]
    pagination_class = None

    def get_queryset(self):
        if (self.request.GET.get(self.SEARCH_PARAM) not in (None, '')):
            return super(GetInstallmentViewSet, self).get_queryset()
        now = datetime.datetime.now()
        installments = Installment.objects.filter(Q(start_date__gt=now) | Q(
            end_date__gt=now + datetime.timedelta(
                days=InstallmentModelEnum.installmentDateBefore.value))).exclude(user=self.request.user)
        courses = self.request.user.courses().filter(installment__in=installments).distinct()
        return courses
