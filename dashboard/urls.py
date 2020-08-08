from django.urls import path
from .views import  *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('get-lessons', GetLessonsViewSet)
router.register('get-shopping', GetShoppingViewSet)

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('lessons/', Lessons.as_view(), name="lessons"),
    path('app_profile/', AppProfile.as_view(), name="app_profile"),
    path('edit_profile/', EditProfile.as_view(), name="edit_profile"),
#     path('edit_profile/change-avatar', change_avatar, name="change_avatar"),
#     path('edit_profile/change-profile', change_profile, name="change_profile"),
#     path('edit_profile/change_password',
#          change_password, name="change_password"),
    path('shopping/', Shopping.as_view(), name="shopping"),
    path('lessons/files/<str:code>/', filemanager),
]

urlpatterns += router.urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
