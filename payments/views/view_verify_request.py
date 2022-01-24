from django.shortcuts import render
from zeep import Client
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.webservices.skyroomwebservice import SkyRoomWebService
from payments.enums import *

from payments.models.pay_history import Pay_History
import datetime

client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')


class VerifyView(APIView):

    # ##check events of pay
    # def check_event(self, request):
    #     try:
    #         event = Event.objects.get(user__id=request.user.id, is_active=True)
    #         event.is_active = False
    #         event.save()
    #         related_user = event.related_user
    #         related_user.credit += float(Events[event.type + "_AMOUNT"].value)
    #         related_user.save()
    #         to = "0" + related_user.phone_number
    #         text = TextUtils.replacer(Sms.increaseCreditText.value, [str(Events[event.type + "_AMOUNT"].value),
    #                                                                  str(int(related_user.credit))])
    #         send_sms = SmsWebServices.send_sms(to, text, None)
    #         if send_sms is not None:
    #             logger.error("danger: " + send_sms)
    #         del request.session['event_discount']
    #     except:
    #         logger.error("this pay don't have event")

    def get(self, request):
        try:
            new_pay = Pay_History.objects.filter(purchaser=request.user, submit_date__isnull=True).first()
            if new_pay is None:
                raise Exception('تراکنش انجام شده')
        except:
            return Response({'RefID': "تراکنش انجام شده"}, status=status.HTTP_226_IM_USED)
        now = datetime.datetime.now()
        new_pay.submit_date = now
        if request.GET.get('Status') == 'OK':
            result = client.service.PaymentVerification(
                MERCHANT.merchant.value, request.GET.get('Authority'), new_pay.amount)
            if result.Status == 100:
                installment_id_list = new_pay.installments.split()
                user = request.user
                flag = False
                # check that we need to create a sky room account for this user or not
                if user.installments.first() is None:
                    flag = True
                for installment_id in installment_id_list:
                    user.installments.add(installment_id)
                user.save()
                new_pay.is_successful = True
                new_pay.payment_code = str(result.RefID)
                new_pay.save()
                check_sky_room = True
                if flag:
                    check_sky_room = webServices.create_sky_room_obj(user)
                # this try is for events
                self.check_event(request)
                if request.accepted_renderer.format == 'html':
                    if check_sky_room is SkyRoomWebService.no_error.value:
                        return render(request, 'dashboard/success_shopping.html', {'RefID': str(result.RefID)})
                    elif check_sky_room is SkyRoomWebService.success.value:
                        return render(request, 'dashboard/success_shopping.html',
                                      {'RefID': str(result.RefID), 'success': SkyRoomWebService.success_message.value})
                    else:
                        return render(request, 'dashboard/success_shopping.html',
                                      {'RefID': str(result.RefID), 'error': ''})
                return Response({'RefID': str(result.RefID)})
            elif result.Status == 101:
                new_pay.is_successful = True
                new_pay.save()
                return Response({'RefID': "تراکنش انجام شده"}, status=status.HTTP_226_IM_USED)
            else:
                new_pay.save()
                return Response({'error': "پرداخت ناموفق"}, status.HTTP_406_NOT_ACCEPTABLE)

        else:
            new_pay.save()
            return Response({'error': "پرداخت ناموفق"}, status.HTTP_406_NOT_ACCEPTABLE)
