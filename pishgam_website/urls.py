"""pishgam_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home.views import home, page_not_found
from accounts.views import *
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Tabesh API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('404-page-not-found/', page_not_found, name="page-not-found"),
    path('signup/', SignUp.as_view(), name="signup"),
    path('signin/', SignIn.as_view(), name='signin'),
    path('signin/forget-password/', ForgetPassword.as_view(), name='forget_password'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='api_token_auth'),
    path('signout/', SignOut.as_view() , name='signout'),
    path('dashboard/', include('dashboard.urls')),
    path('payment/', include('zarinpal.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
#handler403 = sign_up_required
admin.site.site_header = "صفحه ادمین"
admin.site.site_title = "صفحه ادمین"
admin.site.index_title = "صفحه ادمین"
