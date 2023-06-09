from django.urls import path

from applications.usuario.api.api import (
    ApvAhorroVoluntarioColaboradorCreateAPIView
    , ApvAhorroVoluntarioColaboradorDetailApiView
    , ColaboradorCreateAPIView
    , ColaboradorUpdateAPIView
    , ColaboradorDetailApiView
    , DatosPrevisionalesColaboradorCreateAPIView
    , DatosPrevisionalesColaboradorDetailApiView
    , UsuarioEmpresaDatosLaboralesCreateAPIView
    , UsuarioEmpresaDatosLaboralesDetailApiView
    , UsuarioEmpresaDatosLaboralesUpdateView
    , FiniquitoColaboradorCreateAPIView
)


app_name = 'usuario_app'

urlpatterns = [
    path('colaborador/add/', ColaboradorCreateAPIView.as_view(), name='add-colaborador'),
    path('colaborador/edit/<pk>/', ColaboradorUpdateAPIView.as_view(), name='edit-colaborador'),
    path('colaborador/search/<pk>/', ColaboradorDetailApiView.as_view(), name='search-colaborador'),
    
    path('colaborador/add/labor-data/<user_id>/', UsuarioEmpresaDatosLaboralesCreateAPIView.as_view(), name='add-labor-data-colaborador'),
    path('colaborador/edit/labor-data/<pk>/', UsuarioEmpresaDatosLaboralesUpdateView.as_view(), name='edit-labor-data-colaborador'),
    path('colaborador/search/labor-data/<pk>/', UsuarioEmpresaDatosLaboralesDetailApiView.as_view(), name='search-labor-data-colaborador'),

    path('colaborador/add/datos-previsionales/<user_id>/', DatosPrevisionalesColaboradorCreateAPIView.as_view(), name='add-datos-previsionales'),
    path('colaborador/search/datos-previsionales/<user_id>/', DatosPrevisionalesColaboradorDetailApiView.as_view(), name='search-datos-previsionales'),

    path('colaborador/add/apv/ahorro-voluntario/<user_id>/', ApvAhorroVoluntarioColaboradorCreateAPIView.as_view(), name='add-apv-ahorro-voluntario'),
    path('colaborador/search/apv/ahorro-voluntario/<user_id>/', ApvAhorroVoluntarioColaboradorDetailApiView.as_view(), name='search-apv-ahorro-voluntario'),




    path('colaborador/add/dato/finiquito/<user_id>/', FiniquitoColaboradorCreateAPIView.as_view(), name='add-finiquito'),
]