"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from applications.account_base.api.api import Login, Logout

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourcompany.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('', include('applications.account_base.urls')),
    path('', include('applications.base.urls')),
    path('', include('applications.remuneracion.urls')),
    path('', include('applications.empresa.urls')),
    path('', include('applications.configurations.urls')),
    path('', include('applications.usuario.urls')),
    path('', include('applications.security.urls')),

    #path('api/attendance/', include('applications.attendance.urls')),
    path('', include('applications.attendance.urls')),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
