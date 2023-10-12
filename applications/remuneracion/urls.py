from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from applications.remuneracion.api.api import ApiAddConcept

from applications.remuneracion.views import calculate_salaries, control_panel, render_pdf, download_pdf

app_name = 'remun_app'

urlpatterns = [
    path('panel-control/', control_panel, name='control_panel'),


    path('calculate-salaries/', calculate_salaries, name='calculate_salaries'),
    path('render-pdf/', render_pdf, name='render_pdf'),
    path('simulation-liquidation-salary/<str:pdf_filename>', download_pdf, name='download_pdf'),


    path('calculate-salaries/', calculate_salaries, name='calculate_salaries'),


    #API
    path('add-concept', ApiAddConcept.as_view(), name='add_concept'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)