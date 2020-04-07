from django.urls import path

from .views import dashboard, edit_profile, lessons, shopping , filemanager
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('lessons/', lessons, name="lessons"),
    path('edit_profile/', edit_profile, name="edit_profile"),
    path('shopping/', shopping, name="shopping"),
    path('lessons/files/<str:code>' , filemanager )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
