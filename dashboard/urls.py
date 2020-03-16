from django.urls import path 
from .views import profile , dashboard , edit_profile
urlpatterns = [
    path('edit_profile' , edit_profile , name="edit_profile" ),
    path('profile/' , profile , name = 'profile'),
    path('' , dashboard , name='dashboard'),
]
