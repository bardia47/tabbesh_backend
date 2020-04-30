from django.urls import path
from .views import  *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('lessons/', lessons, name="lessons"),
    path('edit_profile/', edit_profile, name="edit_profile"),
    path('edit_profile/change-avatar', change_avatar, name="change_avatar"),
    path('edit_profile/change-profile', change_profile, name="change_profile"),
    path('edit_profile/change_password',
         change_password, name="change_password"),
    path('shopping/', shopping, name="shopping"),
    path('shopping/success-shopping', success_shopping, name="success_shopping"),
    path('shopping/unsuccess-shopping',
         unsuccess_shopping, name="unsuccess_shopping"),
    path('lessons/files/<str:code>', filemanager),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
