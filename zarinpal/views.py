from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from accounts.models import Course

MERCHANT = '0c5db223-a20f-4789-8c88-56d78e29ff63'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
description = "توضیحات مربوطه"  # Required
email = ''   # Optional
mobile = ''   # Optional
CallbackURL = 'http://tabbesh.ir/payment/verify/'  # 'http://localhost:8000/payment/verify/'  # Important: need to edit for really server.
amount = 1000  # Toman / Required
user = None
courses_id_list = []


def is_valid(c, a):
    courses = Course.objects.filter(id__in=c)
    total_price = 0
    for course in courses:
        total_price += course.amount
    return True if total_price == a else False


def send_request(request):
    global amount
    global user
    global courses_id_list
    global description
    user = request.user
    courses_id_list = request.POST.get("total_id").split()

    if courses_id_list and is_valid(c=courses_id_list, a=amount):
        amount = int(request.POST.get("total_pr"))
        description = "List of courses id ==> " + str(courses_id_list) + " Total price ==> " + str(amount)

        # handel free courses
        if amount == 0:
            for course_id in courses_id_list:
                user.payments.add(course_id)
            user.save()
            return redirect('success_shopping')

        # request to zarinpal
        else:
            result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
            if result.Status == 100:
                return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
            else:
                # return HttpResponse('Error code: ' + str(result.Status))
                return render(request, 'dashboard/unsuccess_shopping.html', {'error': str(result.Status)})
    else:
        return redirect('shopping')  # what's up noob :)


def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
            for course_id in courses_id_list:
                user.payments.add(course_id)
            user.save()
            return render(request, 'dashboard/success_shopping.html', {'RefID': str(result.RefID)})
        elif result.Status == 101:
            # return HttpResponse('Transaction submitted : ' + str(result.Status))
            return render(request, 'dashboard/success_shopping.html', {'RefID': "تراکنش انجام شده"})
        else:
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
            return render(request, 'dashboard/unsuccess_shopping.html', {'error': str(result.Status)})
    else:
        # return HttpResponse('Transaction failed or canceled by user')
        return redirect('unsuccess_shopping')
