from django.urls import path
from applications.base.api.api import (
    AdminUserCreateAPIView,
    ClienteCreateAPIView, 
    ClientesListApiView,  
    ClienteRetriveUpdateView,
    ClienteDeleteView,
    ClientesDetailApiView,
    PdfContratoClientApiView,
    PdfDataClientApiView
)


app_name = 'base_app'

urlpatterns = [
    path('api/add/cliente/', ClienteCreateAPIView.as_view(), name='add-cliente'),
    path('api/edit/cliente/<pk>/', ClienteRetriveUpdateView.as_view(), name='edit-cliente'), 
    path('api/delete/cliente/<pk>/', ClienteDeleteView.as_view(), name='delete-cliente'), 
    path('api/detail/clientes/<pk>/', ClientesDetailApiView.as_view(), name='detail-cliente'),  
    path('api/pdf/cliente/<pk>/', PdfDataClientApiView.as_view(), name='datos-cliente'),
    path('api/contrato/cliente/<pk>/', PdfContratoClientApiView.as_view(), name='contrato-cliente'),
    path('api/get/all/clientes/', ClientesListApiView.as_view(), name='get-all-clientes'),
    path('add/user/admin/<pk>/', AdminUserCreateAPIView.as_view(), name='add_admin_user'),                           
]