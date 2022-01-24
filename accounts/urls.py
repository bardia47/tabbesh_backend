from django.urls import path, include
from accounts.views.view_send_sms import SendSmsView
from accounts.views.view_signin import *
from accounts.views.view_reset_password import *
from accounts.views.view_signup import *
from accounts.views.view_temp_code import *
from accounts.views.view_logout import *
from accounts.views.view_list.view_city_list import *
from accounts.views.view_list.view_grade_list import *

urlpatterns = [
        path('user/',include([
            path('send-sms/', SendSmsView.as_view(), name='send_sms'),
            path('validate-temp-code/', TempCodeView.as_view(), name='validate-temp-code'),
            path('signup/', SignupView.as_view({'post': 'create'}),
                 name='signup'),
            path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
            path('logout/',LogoutView.as_view(),name='logout'),
            path('reset-password/', ResetPasswordView.as_view({'patch': 'partial_update'}),
                 name='reset_password'),
        ])),
        path('list/',include([
            path('cities/',CityListView.as_view()),
            path('grades/',GradeListView.as_view())
        ]))
]