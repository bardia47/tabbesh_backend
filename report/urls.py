from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path('/<str:name>/', Report.as_view(),name="student_list"),
    path('class-list/<str:code>/', ClassList.as_view(), name="student_list"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
