from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from applications.remuneracion.views import calculate_salaries, control_panel, render_pdf

app_name = 'remun_app'

urlpatterns = [
    path('panel-control/', control_panel, name='control_panel'),


    path('calculate-salaries/', calculate_salaries, name='calculate_salaries'),
    path('render-pdf/', render_pdf, name='render_pdf'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)