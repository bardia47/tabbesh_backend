from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from django.conf import settings
from accounts.models import Course,Pay_History
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


def send_request(request):
    user = request.user
    courses_id_list = request.POST.get("total_id").split()
    try:
        amount = int(request.POST.get("total_pr"))
    except:
        return redirect('unsuccess_shopping')

    if courses_id_list and is_valid(courses_id_list, amount):
        description = "List of courses id ==> " + \
            str(courses_id_list) + " Total price ==> " + str(amount)
        # handel free courses
        if amount == 0:
            for course_id in courses_id_list:
                user.courses.add(course_id)
            user.save()
            return redirect('success_shopping')

        # request to zarinpal
        else:
            url = request.scheme+"://"+request.get_host() + CallbackURL
            result = client.service.PaymentRequest(
                MERCHANT, amount, description, email, mobile, url)
            if result.Status == 100:
                new_pay = Pay_History.objects.create(purchaser=request.user, amount=amount, courses=request.POST.get("total_id"))
                return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
            else:
                return render(request, 'dashboard/unsuccess_shopping.html', {'error': str(result.Status)})
    else:
        return redirect('shopping')  # what's up noob :)


def verify(request):
    try:
        new_pay = Pay_History.objects.filter(purchaser=request.user,submit_date__isnull=True).first()
    except:
        return render(request, 'dashboard/success_shopping.html', {'RefID': "تراکنش انجام شده"})
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
            return render(request, 'dashboard/success_shopping.html', {'RefID': str(result.RefID)})
        elif result.Status == 101:
            # return HttpResponse('Transaction submitted : ' + str(result.Status))
            new_pay.is_successful=True
            new_pay.save()
            return render(request, 'dashboard/success_shopping.html', {'RefID': "تراکنش انجام شده"})
        else:
            new_pay.save()
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
            return render(request, 'dashboard/unsuccess_shopping.html', {'error': str(result.Status)})
    else:
        new_pay.save()
        # return HttpResponse('Transaction failed or canceled by user')
        return redirect('unsuccess_shopping')
