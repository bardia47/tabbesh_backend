from django.urls import path 
from .views import dashboard , edit_profile
urlpatterns = [
    path('edit_profile' , edit_profile , name="edit_profile" ),
    path('' , dashboard , name='dashboard'),
]
