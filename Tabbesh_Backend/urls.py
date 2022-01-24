from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from accounts.views import *
from enum import Enum

schema_view = get_schema_view(
    openapi.Info(
        title="Tabbesh API",
        default_version='v1',
        description="this is swagger for tabbesh API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


class Apps(Enum):
    ADMIN = 'admin'
    USERS = ''
    DASHBOARD = 'dashboard'
    HOME = 'home'
    PAYMENTS = 'payments'

    def __str__(self):
        if self.value:
            return 'api/'+self.value+'/'
        return 'api/'



urlpatterns = [
    path(Apps.ADMIN.__str__(), admin.site.urls),
    path(Apps.USERS.__str__(), include('accounts.urls')),
    path(Apps.DASHBOARD.__str__(), include('dashboard.urls')),
    path(Apps.HOME.__str__(), include('home.urls')),
    path(Apps.PAYMENTS.__str__(), include('payments.urls')),

    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
