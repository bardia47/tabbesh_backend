from django.urls import path

from .views import dashboard, edit_profile, lessons, shopping , filemanager , change_avatar , change_profile , change_password
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('lessons/', lessons, name="lessons"),
    path('shopping/', shopping, name="shopping"),
    path('filemanager/' , filemanager , name="filemanager"),
    path('edit_profile/', edit_profile, name="edit_profile"),
    path('edit_profile/change-avatar', change_avatar, name="change_avatar"),
    path('edit_profile/change-profile', change_profile, name="change_profile"),
    path('edit_profile/change_password', change_password, name="change_password"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
