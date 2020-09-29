from django.urls import path
from .views import *
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
    # path('shopping/', GetShoppingViewSet.as_view({'get': 'list'}), name="shopping"),
    path('shopping/', Shopping.as_view(), name="shopping"),
    path('shopping_cart/', shopping_cart , name="shopping_cart"),
    path('lessons/files/<str:code>/', FileManager.as_view({'post': 'create', 'get': 'retrieve'}),
         name='retrieve_files'),
    path('lessons/files/<str:code>/<int:document_id>/', UpdateFile.as_view({'post': 'update', 'get': 'destroy'}),
         name='update'),
    path('lessons/list/<str:code>/', ClassList.as_view(), name="student_list"),
    path('lessons/teacher_course_panel/<str:code>/', teacher_course_panel, name="teacher_course_panel"),
    path('lessons/student_course_panel/<str:code>/', student_course_panel, name="student_course_panel"),
    path('lessons/user-installments/<str:code>/', UserInstallmentsViewSet.as_view(),
         name="user_installments"),

]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
