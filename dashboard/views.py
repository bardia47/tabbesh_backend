from django.shortcuts import render , redirect
from accounts.models import User

# Create your views here.


# Profile Section

def profile(request):
    if request.method == 'POST':

        # # Gender Check
        # if request.POST['gender_select'] == '1':
        #     gender_check = True
        # else:
        #     gender_check = False

        user = request.user
        user.save()
        return render(request , 'dashboard\profile_page.html')

    else:

        if request.user.is_authenticated:
            return render(request , 'dashboard\profile_page.html')
        else:
            return redirect('signin')


def dashboard(request):
    return render(request , 'dashboard\dashboard.html')