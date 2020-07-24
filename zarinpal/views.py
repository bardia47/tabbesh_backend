from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from django.conf import settings
from accounts.models import Course,Pay_History
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status

import datetime
MERCHANT = '0c5db223-a20f-4789-8c88-56d78e29ff63'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
email = ''  # Optional
mobile = ''  # Optional
CallbackURL = '/payment/verify/'


def is_valid(courses_id_list, amount):
    courses = Course.objects.filter(id__in=courses_id_list)
    total_price = 0
    for course in courses:
        total_price += course.amount
    return True if total_price == amount else False


class SendRequest(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    
    def post(self, request):
        user = request.user
        courses_id_list = request.data["total_id"].split()
        try:
            amount = int(request.data["total_pr"])
        except:
            if request.accepted_renderer.format == 'html':
                return render(request, 'dashboard/unsuccess_shopping.html')
            return Response({'massage':'خرید ناموفق'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if courses_id_list and is_valid(courses_id_list, amount):
            description = "List of courses id ==> " + \
                str(courses_id_list) + " Total price ==> " + str(amount)
            # handel free courses
            if amount == 0:
                for course_id in courses_id_list:
                    user.courses.add(course_id)
                user.save()
                if request.accepted_renderer.format == 'html':
                    return render(request, 'dashboard/success_shopping.html')
                return Response({'massage':'خرید موفق'},status=status.HTTP_201_CREATED)
               
        # request to zarinpal
            else:
                    url = request.scheme+"://"+request.get_host() + CallbackURL
                    result = client.service.PaymentRequest(
                        MERCHANT, amount, description, email, mobile, url)
                    if result.Status == 100:
                        new_pay = Pay_History.objects.create(purchaser=request.user, amount=amount, courses=request.POST.get("total_id"))
                        if request.accepted_renderer.format == 'html':
                            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
                        else:
                            return Response({'url':'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)})
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
            new_pay = Pay_History.objects.filter(purchaser=request.user,submit_date__isnull=True).first()
        except:
            if request.accepted_renderer.format == 'html':
                return render(request, 'dashboard/success_shopping.html', {'RefID': "تراکنش انجام شده"})
            return Response({'RefID': "تراکنش انجام شده"},status=status.HTTP_226_IM_USED)
        now = datetime.datetime.now()
        new_pay.submit_date=now
        if request.GET.get('Status') == 'OK':
            result = client.service.PaymentVerification(
                MERCHANT, request.GET['Authority'], new_pay.amount)
            if result.Status == 100:
                courses_id_list=new_pay.courses.split()
                user = request.user
                for course_id in courses_id_list:
                    user.courses.add(course_id)
                    user.save()
                    new_pay.is_successful=True
                    new_pay.payment_code=str(result.RefID)
                    new_pay.save()
                if request.accepted_renderer.format == 'html':
                    return render(request, 'dashboard/success_shopping.html', {'RefID': str(result.RefID)})
                return Response({'RefID': str(result.RefID)})
            elif result.Status == 101:
            # return HttpResponse('Transaction submitted : ' + str(result.Status))
                new_pay.is_successful=True
                new_pay.save()
                if request.accepted_renderer.format == 'html':
                    return render(request, 'dashboard/success_shopping.html', {'RefID': "تراکنش انجام شده"})
                return Response({'RefID': "تراکنش انجام شده"},status=status.HTTP_226_IM_USED)
            else:
                new_pay.save()
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
                if request.accepted_renderer.format == 'html':
                    return render(request, 'dashboard/unsuccess_shopping.html', {'error': str(result.Status)})
                return Response({'error': str(result.Status)},status.HTTP_406_NOT_ACCEPTABLE)

        else:
            new_pay.save()
        # return HttpResponse('Transaction failed or canceled by user')
            if request.accepted_renderer.format == 'html':
                return render(request, 'dashboard/unsuccess_shopping.html')
            return Response({'error': str(result.Status)},status.HTTP_406_NOT_ACCEPTABLE)

