from django.contrib import admin
from django.urls import path, include
from home.views import *
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
                  path('admin/clearcache/', include('clearcache.urls')),
                  path('admin/', admin.site.urls),
                  path('', include('home.urls')),
                  path('signup/', SignUp.as_view(), name="signup"),
                  path('signin/', SignIn.as_view(), name='signin'),
                  path('signin/forget-password/', ForgetPassword.as_view(), name='forget_password'),
                  path('api/token/', MyTokenObtainPairView.as_view(), name='api_token_auth'),
                  path('signout/', SignOut.as_view(), name='signout'),
                  path('dashboard/', include('dashboard.urls')),
                  path('payment/', include('zarinpal.urls')),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
# handler403 = sign_up_required
admin.site.site_header = "صفحه ادمین"
admin.site.site_title = "صفحه ادمین"
admin.site.index_title = "صفحه ادمین"
