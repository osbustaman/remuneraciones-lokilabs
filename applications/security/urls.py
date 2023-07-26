from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


app_name = 'security_app'

urlpatterns = [
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)