from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from django.conf import settings
from accounts.models import *
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db.models import Sum
from .enums import *
from accounts.utils import TextUtils
from accounts.enums import Sms
from accounts.webServices import SmsWebServices
import datetime
import logging

logger = logging.getLogger("django")

MERCHANT = '0c5db223-a20f-4789-8c88-56d78e29ff63'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
email = ''  # Optional
mobile = ''  # Optional
CallbackURL = '/payment/verify/'


# compare amount of request with courses
def is_valid(courses_id_list, amount, discount):
    courses = Course.objects.filter(id__in=courses_id_list)
    total_price = 0
    for course in courses:
        total_price += course.get_amount_payable()
    if discount is not None:
        total_price = total_price - compute_discount(courses_id_list, total_price, discount)
    return True if int(total_price) == amount else False


class SendRequest(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def post(self, request):
        user = request.user
        courses_id_list = request.data["total_id"].split()
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
        if courses_id_list and is_valid(courses_id_list, amount, discount):
            # handel free courses
            if amount == 0:
                for course_id in courses_id_list:
                    user.courses.add(course_id)
                user.save()
                if request.accepted_renderer.format == 'html':
                    return render(request, 'dashboard/success_shopping.html')
                return Response({'massage': 'خرید موفق'}, status=status.HTTP_201_CREATED)

            # request to zarinpal
            else:
                description = pay_description(courses_id_list, amount, discount, request)
                try:
                    url = request.data['url']
                except:
                    url = request.scheme + "://" + request.get_host() + CallbackURL
                result = client.service.PaymentRequest(
                    MERCHANT, amount, description, email, mobile, url)
                if result.Status == 100:
                    new_pay = Pay_History.objects.create(purchaser=request.user, amount=amount,
                                                         courses=request.data["total_id"])
                    if request.accepted_renderer.format == 'html':
                        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
                    else:
                        return Response({'url': 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)})
                else:
                    if request.accepted_renderer.format == 'html':
                        return render(request, 'dashboard/unsuccess_shopping.html', {'error': str(result.Status)})
                    else:
                        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            if request.accepted_renderer.format == 'html':
                return redirect('/dashboard/shopping/')  # what's up noob :)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class Verify(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        try:
            new_pay = Pay_History.objects.filter(purchaser=request.user, submit_date__isnull=True).first()
        except:
            if request.accepted_renderer.format == 'html':
                return render(request, 'dashboard/success_shopping.html', {'RefID': "تراکنش انجام شده"})
            return Response({'RefID': "تراکنش انجام شده"}, status=status.HTTP_226_IM_USED)
        now = datetime.datetime.now()
        new_pay.submit_date = now
        if request.GET.get('Status') == 'OK':
            result = client.service.PaymentVerification(
                MERCHANT, request.GET['Authority'], new_pay.amount)
            if result.Status == 100:
                courses_id_list = new_pay.courses.split()
                user = request.user
                for course_id in courses_id_list:
                    user.courses.add(course_id)
                    user.save()
                    new_pay.is_successful = True
                    new_pay.payment_code = str(result.RefID)
                    new_pay.save()

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
                    logger.error("danger: " + e)
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

    def post(self, request):
        courses_id_list = request.data["total_id"].split()
        code = request.data['code']
        query = discount_query(code)
        # query &= (Q(courses__id__in=courses_id_list) | Q(courses=None))
        try:
            if request.session.get('event_discount'):
                discount = Discount()
                discount.percent = Events[request.session.get('event_discount') + "_DISCOUNT"].value
            else:
                discount = Discount.objects.get(query)
        except:
            return Response(status.HTTP_406_NOT_ACCEPTABLE)
        amount = int(request.data["total_pr"])
        discount_amount = compute_discount(courses_id_list, amount, discount)
        if discount_amount == 0:
            return Response(status.HTTP_406_NOT_ACCEPTABLE)
        amount = amount - discount_amount
        return Response({'amount': amount})


# query to find discount
def discount_query(code):
    now = datetime.datetime.now()
    query = Q(start_date__lte=now)
    query &= Q(code=code)
    query &= (Q(end_date__gte=now) | Q(end_date=None))
    return query


def compute_discount(courses_id_list, amount, discount):
    if discount.id is None or discount.courses.count() == 0:
        return amount * discount.percent / 100
    else:
        courses = Course.objects.filter(id__in=courses_id_list, discount__id=discount.id)
        sum_amount = 0
        for course in courses:
            sum_amount += course.get_amount_payable()
        return sum_amount * discount.percent / 100


# pay desc for zarin pal
# in this method use replacer for create dynamic text
def pay_description(courses_id_list, amount, discount, request):
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
        discount_text = None
    text = TextUtils.replacer(text, [TextUtils.convert_list_to_string(
        list(Course.objects.filter(id__in=courses_id_list).values_list('title', flat=True))), discount_text,
        request.user.get_full_name()])
    return text
