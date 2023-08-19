from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from applications.security.views import error404


app_name = 'security_app'

urlpatterns = [
    path('error404/', error404, name='error404'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)