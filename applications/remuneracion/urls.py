from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from applications.remuneracion.api.api import ApiAddConcept, ApiConceptUserDeleteView, ApiAddMountConceptUser, ApiGenerateLiquidationUserDeleteView, ApiGetMonthlyPreviredData, ApiGetSystemVariables, ApiSaveSystemVariables

from applications.remuneracion.views import calculate_salaries, control_panel, forecast_indicators, render_pdf, download_pdf, previred_forecast_indicators

app_name = 'remun_app'

urlpatterns = [
    path('panel-control/', control_panel, name='control_panel'),

    path('calculate-salaries/', calculate_salaries, name='calculate_salaries'),
    path('render-pdf/', render_pdf, name='render_pdf'),
    path('simulation-liquidation-salary/<str:pdf_filename>', download_pdf, name='download_pdf'),
    path('indicadores-previsionales', previred_forecast_indicators, name='previred_forecast_indicators'),
    path('variables-remuneraciones', forecast_indicators, name='forecast_indicators'),
    

    #API
    path('add-concept', ApiAddConcept.as_view(), name='add_concept'),
    path('concept-user-delete/<str:user_id>/<str:concept_id>', ApiConceptUserDeleteView.as_view(), name='conceptuser_delete'),
    path('add-mount/<str:user_id>/<str:concept_id>', ApiAddMountConceptUser.as_view(), name='add_mount'),
    path('generate-liquidation/<int:user_id>', ApiGenerateLiquidationUserDeleteView.as_view(), name='generate_liquidation'),

    path('api-get-indicadores-previsionales', ApiGetMonthlyPreviredData.as_view(), name='get_monthly_previred_data'),
    path('api-create-variables-sistema', ApiSaveSystemVariables.as_view(), name='get_save_system_variables'),
    path('api-get-variables-sistema', ApiGetSystemVariables.as_view(), name='get_system_variables'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)