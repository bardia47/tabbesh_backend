from django.urls import path 
from .views import profile , dashboard
urlpatterns = [
    path('profile/' , profile , name = 'profile'),
    path('' , dashboard , name='dashboard'),
]
