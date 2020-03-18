from django.urls import path 
from .views import dashboard , edit_profile , lessons
urlpatterns = [
    path('' , dashboard , name='dashboard'),
    path('lessons' , lessons , name="lessons" ),
    path('edit_profile' , edit_profile , name="edit_profile" ),
]
