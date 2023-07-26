from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from applications.remuneracion.views import control_panel

app_name = 'remun_app'

urlpatterns = [
    path('panel-control/', control_panel, name='control_panel'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)