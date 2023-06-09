import base64
import datetime
import io
import openpyxl
import pandas as pd

from rest_framework.response import Response
from rest_framework import generics, status

from django.db import IntegrityError, transaction

from openpyxl.worksheet.datavalidation import DataValidation

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from applications.base.models import Comuna, Pais, Region
from applications.empresa.models import Cargo, CentroCosto, Empresa, GrupoCentroCosto, Sucursal 

from applications.empresa.api.serializer import (
    CargaLogoEmpresaSerializer
    , CargaMasivaConfiguracionEmpresaSerializer
    , CargoActivaSerializer
    , CargoSerializers
    , CentroCostoSerializers
    , EmpresaSerializers
    , EmpresaActivaSerializer
    , GrupoCentroCostoSerializers
    , SucursalActivaSerializer
    , SucursalSerializers
)

# Define el objeto Parameter para el encabezado Authorization
header_param = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Token Bearer",
)

""" AQUI SE CREA EL CRUD DE EMPRESA """
class EmpresaCreateAPIView(generics.CreateAPIView):
    serializer_class = EmpresaSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="My Operation ID",
        operation_description="My Operation Description",
        security=[{"Bearer": []}]
    )
    def post(self, request, format=None):
        serializer = EmpresaSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_to_page = {
                "data_serializer": serializer.data
            }

            return Response(response_to_page, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmpresaListApiView(generics.ListAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Listar Empresas",
        operation_description='Obtener listado de empresas registradas.',
        responses={200: EmpresaSerializers(many=True)},
        security=[{"Bearer": []}]
    )
    def list(self, request, *args, **kwargs):
        try:
            get_all_empresas = Empresa.objects.filter(emp_activa='S')
            data = list(get_all_empresas.values())
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class EmpresaDetailApiView(generics.RetrieveAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Buscar empresa",
        operation_description="Se obtiene obtiene toda la información de una empresa en particular",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        object_empresa = self.queryset.filter(emp_id=self.kwargs['pk'])
        data = list(object_empresa.values())
        return Response(data, status=status.HTTP_201_CREATED)

class EmpresaRetriveUpdateView(generics.UpdateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Editar empresa",
        operation_description="Se actualiza toda la información de una empresa en particular",
        security=[{"Bearer": []}]
    )   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        empresa = Empresa.objects.get(emp_id=pk)
        empresa_serializer = self.serializer_class(empresa, data=request.data)
        if empresa_serializer.is_valid():
            empresa_serializer.save()
            return Response(empresa_serializer.data, status=status.HTTP_200_OK)
        return Response(empresa_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmpresaDeleteView(generics.UpdateAPIView):
    serializer_class = EmpresaActivaSerializer
    queryset = Empresa.objects.all()

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Eliminar empresa",
        operation_description="Se actualiza el campo emp_activa de una empresa en particular, en donde se cambia a N indicando que la empresa no esta activa",
        security=[{"Bearer": []}]
    )   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            pk = int(kwargs['pk'])
            empresa = Empresa.objects.get(emp_id=pk)
            empresa.emp_activa = request.data['empresa_activa']
            empresa.save()

            data = {
                "emp_codigo": empresa.emp_codigo,
                "status": "OK",
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

""" AQUI SE CREA EL CRUD DE EMPRESA """

""" AQUI SE CREA EL CRUD DE Sucursal """
class SucursalCreateAPIView(generics.CreateAPIView):
    serializer_class = SucursalSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="My Operation ID",
        operation_description="My Operation Description",
        security=[{"Bearer": []}]
    )
    def post(self, request, format=None):
        serializer = SucursalSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_to_page = {
                "data_serializer": serializer.data
            }

            return Response(response_to_page, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SucursalListApiView(generics.ListAPIView):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Listar sucursales",
        operation_description='Obtener listado de sucursales registradas.',
        responses={200: EmpresaSerializers(many=True)},
        security=[{"Bearer": []}]
    )
    def list(self, request, *args, **kwargs):
        try:
            get_all_sucursal = Sucursal.objects.filter(suc_estado='S')
            data = list(get_all_sucursal.values())
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class SucursalDetailApiView(generics.RetrieveAPIView):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Buscar sucursal",
        operation_description="Se obtiene obtiene toda la información de una sucursal en particular",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        object_sucursal = self.queryset.filter(emp_id=self.kwargs['pk'])
        data = list(object_sucursal.values())
        return Response(data, status=status.HTTP_201_CREATED)

class SucursalRetriveUpdateView(generics.UpdateAPIView):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Editar sucursal",
        operation_description="Se actualiza toda la información de una sucursal en particular",
        security=[{"Bearer": []}]
    )   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        sucursal = Sucursal.objects.get(suc_id=pk)
        sucursal_serializer = self.serializer_class(sucursal, data=request.data)
        if sucursal_serializer.is_valid():
            sucursal_serializer.save()
            return Response(sucursal_serializer.data, status=status.HTTP_200_OK)
        return Response(sucursal_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SucursalDeleteView(generics.UpdateAPIView):
    serializer_class = SucursalActivaSerializer
    queryset = Sucursal.objects.all()

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Eliminar empresa",
        operation_description="Se actualiza el campo suc_estado de una sucursal en particular, en donde se cambia a N indicando que la sucursal no esta activa",
        security=[{"Bearer": []}]
    )   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            pk = int(kwargs['pk'])
            sucursal = Sucursal.objects.get(suc_id=pk)
            sucursal.suc_estado = request.data['sucursal_activa']
            sucursal.save()

            data = {
                "suc_codigo": sucursal.suc_codigo,
                "status": "OK",
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

""" AQUI SE CREA EL CRUD DE Sucursal """

""" AQUI SE CREA EL CRUD DE CARGOS """

class CargoCreateAPIView(generics.CreateAPIView):
    serializer_class = CargoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Crear cargo",
        operation_description="Se crea el cargo por empresa",
        security=[{"Bearer": []}]
    )
    def post(self, request, format=None):
        serializer = CargoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_to_page = {
                "data_serializer": serializer.data
            }

            return Response(response_to_page, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CargoListApiView(generics.ListAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Listar cargos",
        operation_description='Obtener listado de cargos registradas.',
        security=[{"Bearer": []}]
    )
    def list(self, request, *args, **kwargs):
        try:
            get_all_cargos = Cargo.objects.filter(car_activa='S', empresa__emp_id = self.kwargs['pk'])
            data = list(get_all_cargos.values())
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
class CargoDetailApiView(generics.RetrieveAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Buscar sucursal",
        operation_description="Se obtiene obtiene toda la información de un cargo en particular",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        object_cargo = self.queryset.filter(car_id=self.kwargs['pk'])
        data = list(object_cargo.values())
        return Response(data, status=status.HTTP_201_CREATED)
        
class CargoRetriveUpdateView(generics.UpdateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Editar cargo",
        operation_description="Se actualiza toda la información de un cargo en particular",
        security=[{"Bearer": []}]
    )   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        emp_id = int(kwargs['emp_id'])
        cargo = Cargo.objects.filter(car_id=pk, empresa__emp_id = emp_id)
        cargo_serializer = self.serializer_class(cargo, data=request.data)
        if cargo_serializer.is_valid():
            cargo_serializer.save()
            return Response(cargo_serializer.data, status=status.HTTP_200_OK)
        return Response(cargo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CargoDeleteView(generics.UpdateAPIView):
    serializer_class = CargoActivaSerializer
    queryset = Cargo.objects.all()

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Eliminar cargo",
        operation_description="Se actualiza el campo car_activa de un cargo en particular, en donde se cambia a N indicando que la sucursal no esta activa",
        security=[{"Bearer": []}]
    )   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            pk = int(kwargs['pk'])
            cargo = Cargo.objects.get(suc_id=pk)
            cargo.car_activa = request.data['car_activa']
            cargo.save()

            data = {
                "car_id": cargo.car_id,
                "status": "OK",
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

""" AQUI SE CREA EL CRUD DE CARGOS """

""" AQUI SE CREA EL CRUD DE GRUPO DE CENTRO DE COSTOS """

class GrupoCentroCostoCreateAPIView(generics.CreateAPIView):
    serializer_class = GrupoCentroCostoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Crear centro de costo",
        operation_description="Se crea el centro de costo",
        security=[{"Bearer": []}]
    )
    def post(self, request, format=None):
        serializer = GrupoCentroCostoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_to_page = {
                "data_serializer": serializer.data
            }

            return Response(response_to_page, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GrupoCentroCostoListApiView(generics.ListAPIView):
    queryset = GrupoCentroCosto.objects.all()
    serializer_class = GrupoCentroCostoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Listar los centro de costos",
        operation_description='Obtener listado de centro de costos.',
        responses={200: GrupoCentroCostoSerializers(many=True)},
        security=[{"Bearer": []}]
    )
    def list(self, request, *args, **kwargs):
        try:
            get_all_grupo_centro_costos = self.queryset.filter(gcencost_activo='S')
            data = list(get_all_grupo_centro_costos.values())
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class GrupoCentroCostoDetailApiView(generics.RetrieveAPIView):
    queryset = GrupoCentroCosto.objects.all()
    serializer_class = GrupoCentroCostoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Buscar grupo centro de costo",
        operation_description="Se obtiene obtiene toda la información de un grupo centro de costo en particular",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        object_centro_costos = self.queryset.filter(gcencost_id=self.kwargs['pk'])
        data = list(object_centro_costos.values())
        return Response(data, status=status.HTTP_201_CREATED)

class GrupoCentroCostoRetriveUpdateView(generics.UpdateAPIView):
    queryset = GrupoCentroCosto.objects.all()
    serializer_class = GrupoCentroCostoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Editar grupo centro de costo",
        operation_description="Se actualiza toda la información de un grupo centro de costo en particular",
        security=[{"Bearer": []}]
    )   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        grupo_centro_costo = self.queryset.filter(gcencost_id=pk)
        grupo_centro_costo_serializer = self.serializer_class(grupo_centro_costo, data=request.data)
        if grupo_centro_costo_serializer.is_valid():
            grupo_centro_costo_serializer.save()
            return Response(grupo_centro_costo_serializer.data, status=status.HTTP_200_OK)
        return Response(grupo_centro_costo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GrupoCentroCostoDeleteView(generics.UpdateAPIView):
    queryset = GrupoCentroCosto.objects.all()
    serializer_class = GrupoCentroCostoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Eliminar grupo de centro de costo",
        operation_description="Se actualiza el campo gcencost_activo de un grupo de centro de costo en particular, en donde se cambia a N indicando que el grupo de centro de costo no esta activo",
        security=[{"Bearer": []}]
    )   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            pk = int(kwargs['pk'])
            gcencost = GrupoCentroCosto.objects.get(gcencost_id=pk)
            gcencost.gcencost_activo = request.data['gcencost_activo']
            gcencost.save()

            data = {
                "suc_codigo": gcencost.gcencost_codigo,
                "status": "OK",
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

""" AQUI SE CREA EL CRUD DE GRUPO DE CENTRO DE COSTOS """

""" AQUI SE CREA EL CRUD DE CENTRO DE COSTOS """

class CentroCostoCreateAPIView(generics.CreateAPIView):
    serializer_class = CentroCostoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Crear centro de costo",
        operation_description="Se crea el centro de costo",
        security=[{"Bearer": []}]
    )
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_to_page = {
                "data_serializer": serializer.data
            }

            return Response(response_to_page, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CentroCostoListApiView(generics.ListAPIView):
    queryset = CentroCosto.objects.all()
    serializer_class = CentroCostoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Listar los centro de costos",
        operation_description='Obtener listado de centro de costos.',
        responses={200: CentroCostoSerializers(many=True)},
        security=[{"Bearer": []}]
    )
    def list(self, request, *args, **kwargs):
        try:
            get_all_centro_costos = self.queryset.filter(cencost_activo='S')
            data = list(get_all_centro_costos.values())
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class CentroCostoDetailApiView(generics.RetrieveAPIView):
    queryset = CentroCosto.objects.all()
    serializer_class = CentroCostoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Buscar centro de costo",
        operation_description="Se obtiene obtiene toda la información de un centro de costo en particular",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        object_centro_costos = self.queryset.filter(cencost_id=self.kwargs['pk'])
        data = list(object_centro_costos.values())
        return Response(data, status=status.HTTP_201_CREATED)

class CentroCostoRetriveUpdateView(generics.UpdateAPIView):
    queryset = CentroCosto.objects.all()
    serializer_class = CentroCostoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Editar centro de costo",
        operation_description="Se actualiza toda la información de un centro de costo en particular",
        security=[{"Bearer": []}]
    )   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        centro_costo = self.queryset.filter(gcencost_id=pk)
        centro_costo_serializer = self.serializer_class(centro_costo, data=request.data)
        if centro_costo_serializer.is_valid():
            centro_costo_serializer.save()
            return Response(centro_costo_serializer.data, status=status.HTTP_200_OK)
        return Response(centro_costo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CentroCostoDeleteView(generics.UpdateAPIView):
    queryset = CentroCosto.objects.all()
    serializer_class = CentroCostoSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Eliminar de centro de costo",
        operation_description="Se actualiza el campo cencost_activo de un de centro de costo en particular, en donde se cambia a N indicando que el centro de costo no esta activo",
        security=[{"Bearer": []}]
    )   
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            pk = int(kwargs['pk'])
            cencost = self.queryset.get(cencost_id=pk)
            cencost.cencost_activo = request.data['cencost_activo']
            cencost.save()

            data = {
                "suc_codigo": cencost.gcencost_codigo,
                "status": "OK",
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as inst:
            data = {
                "type_error": type(inst)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
""" AQUI SE CREA EL CRUD DE CENTRO DE COSTOS """

class DescargarPlantillaConfiguracionEmpresaCreateAPIView(generics.CreateAPIView):
    serializer_class = CargaMasivaConfiguracionEmpresaSerializer

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Descarga plantilla confuracion empresa",
        operation_description="Este endpoint es para descargar una plantilla en Excel para poder cargar de forma masiva elementos de una empresa, el FRONT debe convertir el base64 en un archivo excel",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):

        # Define las opciones para la lista desplegable
        
        # Define las cabeceras de cada hoja
        cabeceras_cargos = ['nombre cargo']
        cabeceras_sucursales = ['codigo', 'nombre', 'direccion', 'pais', 'region', 'comuna']
        cabeceras_grupo_cc = ['nombre gcc', 'codigo gcc']
        cabeceras_cc = ['codigo gcc', 'nombre cc', 'codigo cc']
        cabeceras_col_oculta = ['comunas', 'regiones']

        # Crea un DataFrame vacío para cada hoja del Excel
        df_cargos = pd.DataFrame(columns=cabeceras_cargos)
        df_sucursales = pd.DataFrame(columns=cabeceras_sucursales)
        df_grupo_cc = pd.DataFrame(columns=cabeceras_grupo_cc)
        df_cc = pd.DataFrame(columns=cabeceras_cc)
        df_co = pd.DataFrame(columns=cabeceras_col_oculta)

        # Crea un objeto ExcelWriter para escribir en el archivo Excel

        #Fecha actual
        now = datetime.datetime.now()
        # filename_excel = now.strftime('%Y%m%d%H%M%S') + '.xlsx'
        filename_excel ='plantilla_carga_masiva.xlsx'
        writer = pd.ExcelWriter(f'{filename_excel}', engine='xlsxwriter')

        # Escribe cada DataFrame en una hoja del archivo Excel
        df_cargos.to_excel(writer, sheet_name='cargos', index=False)
        df_sucursales.to_excel(writer, sheet_name='sucursales', index=False)
        df_grupo_cc.to_excel(writer, sheet_name='grupo centros costos', index=False)
        df_cc.to_excel(writer, sheet_name='centros costos', index=False)
        df_co.to_excel(writer, sheet_name='BD', index=False)

        # Asigna las cabeceras a cada DataFrame
        df_cargos.columns = cabeceras_cargos
        df_sucursales.columns = cabeceras_sucursales
        df_grupo_cc.columns = cabeceras_grupo_cc
        df_cc.columns = cabeceras_cc
        df_co.columns = cabeceras_col_oculta

        # Guarda el archivo Excel
        writer.save()

        # Abre el archivo Excel existente
        workbook = openpyxl.load_workbook(filename=filename_excel)

        sheet_cc = workbook['BD']

        object_comunas = Comuna.objects.all()
        cont = 2
        for comunas in object_comunas:
            sheet_cc[f'A{cont}'] = comunas.com_nombre
            sheet_cc[f'B{cont}'] = comunas.region.re_nombre
            cont += 1

        # Oculta la hoja
        # sheet_cc.sheet_state = 'hidden'

        workbook.save(filename_excel)

        # seleccionamos la hoja
        sheet = workbook['sucursales']

        cantidad_filas = 22
        # Crear una lista de opciones para la lista desplegable de pais
        object_pais = Pais.objects.all()
        array_paises = []
        for pais in object_pais:
            array_paises.append(pais.pa_nombre)

        validation = DataValidation(type="list", formula1=f'"{",".join(array_paises)}"')
        validation.add(f'D2:D{cantidad_filas}')
        sheet.add_data_validation(validation)

        # Crear una lista de opciones para la lista desplegable de regiones
        object_region = Region.objects.all()
        array_regiones = []
        for region in object_region:
            array_regiones.append(region.re_nombre)

        validation_regiones = DataValidation(type="list", formula1=f'"{",".join(array_regiones)}"')
        validation_regiones.add(f'E2:E{cantidad_filas}')
        sheet.add_data_validation(validation_regiones)

        # Guardamos el archivo con los cambios
        workbook.save(filename_excel)

        # Codifica el archivo en base64
        with open(filename_excel, 'rb') as file:
            base64_encoded_file = base64.b64encode(file.read()).decode('utf-8').replace('\n', '')

        # Retorna la respuesta con el archivo en base64
        return Response({
            "archivo_base64": base64_encoded_file
        }, status=status.HTTP_201_CREATED)


class CargaMasivaConfiguracionEmpresaCreateAPIView(generics.CreateAPIView):
    serializer_class = CargaMasivaConfiguracionEmpresaSerializer

    def get_queryset(self):
        pass

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Leer excel para garga masiva de datos de una empresa",
        operation_description="Este endpoint es para cargar datos masivos de elementos de una empresa, en donde se pueden cargar cargos, centros de costos, grupos de centros de costos y sucursales",
        security=[{"Bearer": []}]
    )
    def post(self, request, *args, **kwargs):

        # Obtener el ID de la empresa
        try:
            pk = int(kwargs['pk'])
        except ValueError:
            transaction.set_rollback(True)
            return Response({'error': 'El ID de la empresa debe ser un número válido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el archivo Excel
        try:
            bytes_excel = base64.b64decode(request.data['excel_carga_masiva'])
        except KeyError:
            transaction.set_rollback(True)
            return Response({'error': 'No se encontró el archivo Excel en la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            transaction.set_rollback(True)
            return Response({'error': 'El archivo Excel no se pudo decodificar correctamente.'}, status=status.HTTP_400_BAD_REQUEST)

        # Leer el archivo Excel
        excel_file = io.BytesIO(bytes_excel)
        df_excel = pd.read_excel(excel_file, sheet_name=None)
        hojas_excel = df_excel.keys()

        datos_por_hoja = {}
        for hoja in hojas_excel:
            # Lee los datos de la hoja actual
            # skiprows omite la primera fila
            df_hoja = pd.read_excel(excel_file, sheet_name=hoja, skiprows=0)

            # Guarda los datos de la hoja actual en un array
            datos_hoja = []
            for index, row in df_hoja.iterrows():
                datos_hoja.append(row.to_dict())

            # Agrega los datos de la hoja actual al diccionario
            datos_por_hoja[hoja] = datos_hoja

        # Recorre el diccionario nuevo para poder agregar elementos a los modelos correspondientes
        for key, value in datos_por_hoja.items():
            if key == "cargos":
                for _val in value:
                    for k, v in _val.items():
                        # Crear el objeto Cargo y guardar en la base de datos
                        cargo = Cargo()
                        cargo.car_nombre = v
                        try:
                            cargo.save()
                            cargo.empresa.set(Empresa.objects.filter(emp_id=pk))
                        except IntegrityError:
                            transaction.set_rollback(True)
                            return Response({'error': 'Error al guardar el objeto Cargo.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            if key == "sucursales":
                for _val in value:
                    try:
                        sucursal = Sucursal()
                        sucursal.suc_codigo = _val['codigo']
                        sucursal.suc_descripcion = _val['nombre']
                        sucursal.empresa = Empresa.objects.get(emp_id=pk)
                        sucursal.suc_direccion = _val['direccion']
                        sucursal.pais = Pais.objects.get(pa_nombre = _val['pais'])
                        sucursal.region = Region.objects.get(re_nombre = _val['region'])
                        sucursal.comuna = Comuna.objects.get(com_nombre = _val['comuna'])
                        sucursal.save()
                    except (IntegrityError, KeyError) as e:
                        transaction.set_rollback(True)
                        return Response({'error': 'Error al guardar el objeto Sucursal.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if key == "grupo centros costos":
                for _val in value:
                    try:
                        gccosto = GrupoCentroCosto()
                        gccosto.gcencost_nombre = _val['nombre gcc']
                        gccosto.gcencost_codigo = _val['codigo gcc']
                        gccosto.empresa = Empresa.objects.get(emp_id=pk)
                        gccosto.save()
                    except (IntegrityError, KeyError) as e:
                        transaction.set_rollback(True)
                        return Response({'error': 'Error al guardar el objeto Grupo Centro Costo.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if key == "centros costos":
                for _val in value:
                    try:
                        ccosto = CentroCosto()
                        ccosto.grupocentrocosto = GrupoCentroCosto.objects.get(gcencost_codigo=_val['codigo gcc'])
                        ccosto.cencost_nombre = _val['nombre cc']
                        ccosto.cencost_codigo = _val['codigo cc']
                        ccosto.save()
                    except (IntegrityError, KeyError) as e:
                        transaction.set_rollback(True)
                        return Response({'error': 'Error al guardar el objeto Centro Costo.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(datos_por_hoja, status=status.HTTP_201_CREATED)

class CargaLogoEmpresaCreateAPIView(generics.CreateAPIView):
    serializer_class = CargaLogoEmpresaSerializer

    def get_queryset(self):
        return None
        
    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Leer imagen de una empresa",
        operation_description="Este endpoint es para cargar la imagen de una empresa",
        security=[{"Bearer": []}]
    )
    def post(self, request, *args, **kwargs):

        # Obtener el ID de la empresa
        try:
            pk = int(kwargs['pk'])
        except ValueError:
            return Response({'error': 'El ID de la empresa debe ser un número válido.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            empresa = Empresa.objects.get(emp_id = pk)
            empresa.emp_imagenempresa = request.data['logo_empresa']
            empresa.save()

        except (IntegrityError, KeyError) as e:
            transaction.set_rollback(True)
            return Response({'error': 'Error al guardar la imagen.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as inst:
            transaction.set_rollback(True)
            return Response({'error': 'Error al guardar la imagen.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            "success": True
        }, status=status.HTTP_201_CREATED)

class ObtenerLogoEmpresaCreateAPIView(generics.CreateAPIView):
    serializer_class = CargaLogoEmpresaSerializer

    def get_queryset(self):
        return None

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Obtener logo empresa",
        operation_description="Este endpoint es para obtener el base64 de la imagen de la empresa para asi poder cargarla en el front",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):

        # Obtener el ID de la empresa
        try:
            pk = int(kwargs['pk'])
        except ValueError:
            return Response({'error': 'El ID de la empresa debe ser un número válido.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            empresa = Empresa.objects.get(emp_id = pk)
            logo_empresa = empresa.emp_imagenempresa

        except (IntegrityError, KeyError) as e:
            return Response({'error': 'Error al guardar la imagen.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as inst:
            return Response({'error': 'Error al guardar la imagen.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Retorna la respuesta con el archivo en base64
        return Response({
            "logo_empresa": logo_empresa
        }, status=status.HTTP_201_CREATED)
