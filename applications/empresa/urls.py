from django.urls import path
from applications.empresa.api.api import (
    CargoCreateAPIView,
    CargoDeleteView,
    CargoDetailApiView,
    CargoListApiView,
    CargoRetriveUpdateView,
    EmpresaCreateAPIView
    , EmpresaListApiView
    , EmpresaDetailApiView
    , EmpresaRetriveUpdateView
    , EmpresaDeleteView
    , SucursalCreateAPIView
    , SucursalListApiView
    , SucursalDetailApiView
    , SucursalRetriveUpdateView
    , SucursalDeleteView
    , GrupoCentroCostoCreateAPIView
    , GrupoCentroCostoListApiView
    , GrupoCentroCostoDetailApiView
    , GrupoCentroCostoRetriveUpdateView
    , GrupoCentroCostoDeleteView
    , CentroCostoCreateAPIView
    , CentroCostoListApiView
    , CentroCostoDetailApiView
    , CentroCostoRetriveUpdateView
    , CentroCostoDeleteView
    , CargaMasivaConfiguracionEmpresaCreateAPIView
    , DescargarPlantillaConfiguracionEmpresaCreateAPIView
    , CargaLogoEmpresaCreateAPIView
    , ObtenerLogoEmpresaCreateAPIView
)

app_name = 'empresa_app'

urlpatterns = [
    path('empresa/add/', EmpresaCreateAPIView.as_view(), name='add-empresa'),
    path('empresa/listar/', EmpresaListApiView.as_view(), name='listar-empresas'),
    path('empresa/buscar/<pk>/', EmpresaDetailApiView.as_view(), name='buscar-empresa'),
    path('empresa/editar/<pk>/', EmpresaRetriveUpdateView.as_view(), name='editar-empresa'),
    path('empresa/eliminar/<pk>/', EmpresaDeleteView.as_view(), name='eliminar-empresa'),

    path('sucursal/add/', SucursalCreateAPIView.as_view(), name='add-sucursal'),
    path('sucursal/list/', SucursalListApiView.as_view(), name='list-sucursal'),
    path('sucursal/buscar/<pk>/', SucursalDetailApiView.as_view(), name='buscar-sucursal'),
    path('sucursal/editar/<pk>/', SucursalRetriveUpdateView.as_view(), name='editar-sucursal'),
    path('sucursal/eliminar/<pk>/', SucursalDeleteView.as_view(), name='eliminar-sucursal'),

    path('cargo/add/', CargoCreateAPIView.as_view(), name='add-cargo'),
    path('cargo/list/', CargoListApiView.as_view(), name='list-cargo'),
    path('cargo/buscar/<pk>/', CargoDetailApiView.as_view(), name='buscar-cargo'),
    path('cargo/editar/<pk>/<emp_id>/', CargoRetriveUpdateView.as_view(), name='editar-cargo'),
    path('cargo/eliminar/<pk>/', CargoDeleteView.as_view(), name='eliminar-cargo'),

    path('grupocentrocosto/add/', GrupoCentroCostoCreateAPIView.as_view(), name='add-grupocentrocosto'),
    path('grupocentrocosto/list/', GrupoCentroCostoListApiView.as_view(), name='list-grupocentrocosto'),
    path('grupocentrocosto/buscar/<pk>/', GrupoCentroCostoDetailApiView.as_view(), name='buscar-grupocentrocosto'),
    path('grupocentrocosto/editar/<pk>/', GrupoCentroCostoRetriveUpdateView.as_view(), name='editar-grupocentrocosto'),
    path('grupocentrocosto/eliminar/<pk>/', GrupoCentroCostoDeleteView.as_view(), name='eliminar-grupocentrocosto'),

    path('centrocosto/add/', CentroCostoCreateAPIView.as_view(), name='add-centrocosto'),
    path('centrocosto/list/', CentroCostoListApiView.as_view(), name='list-centrocosto'),
    path('centrocosto/buscar/<pk>/', CentroCostoDetailApiView.as_view(), name='buscar-centrocosto'),
    path('centrocosto/editar/<pk>/', CentroCostoRetriveUpdateView.as_view(), name='editar-centrocosto'),
    path('centrocosto/eliminar/<pk>/', CentroCostoDeleteView.as_view(), name='eliminar-centrocosto'),

    path('config/cargamasiva/empresa/<pk>/', CargaMasivaConfiguracionEmpresaCreateAPIView.as_view(), name='carga-masiva-configuracion-empresa'),
    path('config/descarga/plantillaexcel/config/empresa/', DescargarPlantillaConfiguracionEmpresaCreateAPIView.as_view(), name='descarga-plantilla-configuracion-empresa'),
    path('config/logo/empresa/<pk>/', CargaLogoEmpresaCreateAPIView.as_view(), name='logo-empresa'),
    path('config/obtener/logo/empresa/<pk>/', ObtenerLogoEmpresaCreateAPIView.as_view(), name='obtenert-logo-empresa'),
]