
import base64
import datetime
import io
import openpyxl
import pandas as pd

from rest_framework.response import Response
from rest_framework import generics, status

from django.db import IntegrityError, transaction

from openpyxl.worksheet.datavalidation import DataValidation
from applications.base.models import Comuna, Pais, Region

from applications.empresa.api.serialize import BulkLoadExcelSerializer
from applications.empresa.models import Cargo, CentroCosto, Empresa, GrupoCentroCosto, Sucursal


class DownloadBranchUploadTemplateCreateAPIView(generics.CreateAPIView):
    serializer_class = BulkLoadExcelSerializer

    def get(self, request, *args, **kwargs):

        # Define las opciones para la lista desplegable
        
        # Define las cabeceras de cada hoja
        cabeceras_cargos = ['nombre cargo']
        cabeceras_sucursales = ['nombre', 'direccion', 'pais', 'region', 'comuna']
        cabeceras_grupo_cc = ['nombre gcc']
        cabeceras_cc = ['nombre cc', 'nombre gcc']
        cabeceras_col_oculta = ['comunas', 'regiones']

        # Crea un DataFrame vacío para cada hoja del Excel
        df_cargos = pd.DataFrame(columns=cabeceras_cargos)
        df_sucursales = pd.DataFrame(columns=cabeceras_sucursales)
        df_grupo_cc = pd.DataFrame(columns=cabeceras_grupo_cc)
        df_cc = pd.DataFrame(columns=cabeceras_cc)
        df_co = pd.DataFrame(columns=cabeceras_col_oculta)

        # Crea un objeto ExcelWriter para escribir en el archivo Excel

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
        validation.add(f'C2:C{cantidad_filas}')
        sheet.add_data_validation(validation)

        # Crear una lista de opciones para la lista desplegable de regiones
        object_region = Region.objects.all()
        array_regiones = []
        for region in object_region:
            array_regiones.append(region.re_nombre)

        validation_regiones = DataValidation(type="list", formula1=f'"{",".join(array_regiones)}"')
        validation_regiones.add(f'D2:D{cantidad_filas}')
        sheet.add_data_validation(validation_regiones)

        # Crear una lista de opciones para la lista desplegable de comunas
        """array_comunas = []
        for comunas in object_comunas:
            array_comunas.append(comunas.com_nombre)

        validation_comunas = DataValidation(type="list", formula1=f'"{",".join(array_comunas)}"')
        validation_comunas.add(f'E2:E{cantidad_filas}')
        sheet.add_data_validation(validation_comunas)"""

        # Guardamos el archivo con los cambios
        workbook.save(filename_excel)

        # Codifica el archivo en base64
        with open(filename_excel, 'rb') as file:
            base64_encoded_file = base64.b64encode(file.read()).decode('utf-8').replace('\n', '')

        # Retorna la respuesta con el archivo en base64
        return Response({
            "archivo_base64": base64_encoded_file
        }, status=status.HTTP_201_CREATED)


class BulkLoadExcelPositionCreateAPIView(generics.CreateAPIView):
    serializer_class = BulkLoadExcelSerializer

    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):

        # Obtener el ID de la empresa
        try:
            pk = int(kwargs['pk'])
        except ValueError:
            transaction.set_rollback(True)
            return Response({'error': 'El ID de la empresa debe ser un número válido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el archivo Excel
        try:
            bytes_excel = base64.b64decode(request.data['archivo_base64'])
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
                        gccosto.empresa = Empresa.objects.get(emp_id=pk)
                        gccosto.save()
                    except (IntegrityError, KeyError) as e:
                        transaction.set_rollback(True)
                        return Response({'error': 'Error al guardar el objeto Grupo Centro Costo.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if key == "centros costos":
                for _val in value:
                    try:
                        ccosto = CentroCosto()
                        ccosto.grupocentrocosto = GrupoCentroCosto.objects.get(gcencost_nombre=_val['nombre gcc'])
                        ccosto.cencost_nombre = _val['nombre cc']
                        ccosto.save()
                    except (IntegrityError, KeyError) as e:
                        transaction.set_rollback(True)
                        return Response({'error': 'Error al guardar el objeto Centro Costo.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(datos_por_hoja, status=status.HTTP_201_CREATED)