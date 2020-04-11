from django.urls import path

from .views import dashboard, edit_profile, lessons, shopping , filemanager , success_shopping , unsuccess_shopping
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('lessons/', lessons, name="lessons"),
    path('edit-profile/', edit_profile, name="edit_profile"),
    path('shopping/', shopping, name="shopping"),
    path('shopping/success-shopping' , success_shopping , name="success_shopping"),
    path('shopping/unsuccess-shopping' , unsuccess_shopping , name="unsuccess_shopping"),
    path('shopping/filemanager/' , filemanager , name="filemanager"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
