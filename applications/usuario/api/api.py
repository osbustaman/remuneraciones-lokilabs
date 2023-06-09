import logging
from django.http import Http404

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth.models import User
from applications.base.models import TablaGeneral
from applications.base.utils import indicadores_economicos
from applications.empresa.models import Afp, Salud

from applications.usuario.api.serializer import (
    ApvAhorroVoluntarioUsuarioEmpresaDatosLaboralesSerializers
    , ColaboradorSerializers
    , DatosPrevisionalesUsuarioEmpresaDatosLaboralesSerializers
    , FiniquitoUsuarioEmpresaDatosLaboralesSerializers
    , UsuarioEmSerializers
    , UsuarioEmpresaDatosLaboralesSerializers
    , UsuarioSerializers
)
from applications.usuario.api.utils import get_key_colaborador_data, get_tope_seguro_cesantia
from applications.usuario.models import Colaborador, Haberes, UsuarioEmpresa

# Define el objeto Parameter para el encabezado Authorization
header_param = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Token Bearer",
)

"""
ETAPA 1 DEL LLENADO DE UN COLABORADOR
"""
class ColaboradorCreateAPIView(generics.CreateAPIView):

    # Especifica el serializador para la clase Colaborador
    serializer_class = ColaboradorSerializers

    # Especifica el serializador para la clase Usuario  
    user_serializer_class = UsuarioSerializers  

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Registrar datos personales de colaborador",
        operation_description="Este código define una vista de creación para la entidad 'Colaborador'. Se utiliza el serializador"
                                +"'ColaboradorSerializers' para validar los datos enviados en la petición POST. Además, también se utiliza"
                                +"el serializador 'UsuarioSerializers' para validar los datos del usuario asociado al colaborador.\n"
                                +"Después de validar los datos, se llama al método save() del serializador 'ColaboradorSerializers'" 
                                +"para guardar el colaborador en la base de datos. Luego, se crea una respuesta que contiene los "
                                +"datos del colaborador y del usuario asociado, y se envía con el código de estado HTTP 201 (Created).\n"
                                +"También se utiliza la librería Swagger para documentar la API.",
        security=[{"Bearer": []}]
    )
    def post(self, request, *args, **kwargs):
        # Crea una instancia del serializador de colaborador con los datos de la petición
        colaborador_serializer = self.serializer_class(data=request.data)
        
        # Crea una instancia del serializador de usuario con los datos del campo 'user' en la petición
        user_serializer = self.user_serializer_class(data=request.data['user'])

        # Valida que los datos sean válidos
        colaborador_serializer.is_valid(raise_exception=True)
        user_serializer.is_valid(raise_exception=True)
        
        # Guarda el colaborador en la base de datos y asigna la instancia de colaborador creada a una variable
        colaborador = colaborador_serializer.save()

        usuario = {
            "col_id": colaborador.user.id,
            "username": colaborador.user.username,
            "first_name": colaborador.user.first_name,
            "last_name": colaborador.user.last_name,
            "email": colaborador.user.email,
            "col_extranjero": colaborador.col_extranjero,
            "col_rut": colaborador.col_rut,
            "col_sexo": colaborador.col_sexo,
            "col_fechanacimiento": colaborador.col_fechanacimiento,
            "col_estadocivil": colaborador.col_estadocivil,
            "col_direccion": colaborador.col_direccion,
            "pais": colaborador.pais.pa_id,
            "region": colaborador.region.re_id,
            "comuna": colaborador.comuna.com_id,
            "col_tipousuario": colaborador.col_tipousuario,
            "col_profesion": colaborador.col_profesion,
            "col_titulo": colaborador.col_titulo,
            "col_formapago": colaborador.col_formapago,
            "banco": colaborador.banco.ban_id,
            "col_tipocuenta": colaborador.col_tipocuenta,
            "col_cuentabancaria": colaborador.col_cuentabancaria,
            "col_usuarioactivo": colaborador.col_usuarioactivo,
            "col_licenciaconducir": colaborador.col_licenciaconducir,
            "col_tipolicencia": colaborador.col_tipolicencia,
            "col_fotousuario": colaborador.col_fotousuario,
        }

        #usuario = colaborador.user

        # Crea un diccionario con los datos del colaborador y el usuario
        response_data = {
            "usuario": usuario
            #'colaborador': colaborador_serializer.data,  # Obtiene los datos serializados del colaborador
            #'user': vars(user_serializer)['_kwargs']['data'],  # Obtiene los datos serializados del usuario
        }

        # Retorna una respuesta con los datos y el código de estado HTTP 201 (Created)
        return Response(response_data, status=status.HTTP_201_CREATED)

class ColaboradorUpdateAPIView(generics.UpdateAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializers
    user_serializer_class = UsuarioSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="My Operation ID",
        operation_description="Este código define una vista de Django para actualizar un objeto Colaborador\n"
                              +"existente utilizando el método PUT para procesar las solicitudes HTTP enviadas a esta vista.\n"
                              +"La vista primero obtiene la instancia del Colaborador a actualizar mediante el\n"
                              +"método get_object(). Luego, se obtienen los datos de la solicitud desde los parámetros\n"
                              +"de colaborador y usuario.\n\n"

                              +"Los datos recibidos son validados utilizando el serializador ColaboradorSerializers. Si se\n"
                              +"recibieron datos de usuario, estos también son validados y actualizados utilizando el\n"
                              +"serializador UsuarioSerializers.\n\n"

                              +"Finalmente, se guarda el objeto Colaborador actualizado en la base de datos y se genera una\n" 
                              +"respuesta HTTP que incluye los datos actualizados de Colaborador y Usuario (si se recibieron datos de Usuario).",
        security=[{"Bearer": []}]
    )
    def put(self, request, *args, **kwargs):
        # Obtener la instancia de Colaborador a actualizar
        colaborador_instance = self.get_object()

        # Obtener los datos de la solicitud
        colaborador_data = request.data
        user_data = request.data['user']

        # Validar los datos de la solicitud
        colaborador_serializer = self.serializer_class(colaborador_instance, data=colaborador_data, partial=True)
        colaborador_serializer.is_valid(raise_exception=True)

        # Si se recibieron datos de usuario, validarlos y actualizarlos
        if user_data:
            user_instance = colaborador_instance.user
            user_instance.username = request.data['user']['username']
            user_instance.first_name = request.data['user']['first_name']
            user_instance.last_name = request.data['user']['last_name']
            user_instance.email = request.data['user']['email']
            user_instance.set_password(request.data['user']['password'])
            user_instance.save()

        # Guardar los cambios en el modelo de Colaborador
        colaborador_serializer.save()

        # Armar la respuesta con los datos actualizados de Colaborador y Usuario
        response_data = {
            'colaborador': colaborador_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

class ColaboradorDetailApiView(generics.RetrieveAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializers
    user_serializer_class = UsuarioSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Obtener detalle colaborador",
        operation_description=   "Esta vista utiliza el método GET para obtener un objeto Colaborador de la base de datos a través de su identificador único y devolver su representación serializada en formato JSON.\n\n" 
                               + "La función get() utiliza el método get_object() heredado de la clase generics.RetrieveAPIView para obtener la instancia del objeto Colaborador correspondiente a través del identificador único en la URL.\n\n"
                               + "A continuación, la función serializa el objeto Colaborador utilizando el serializador definido en serializer_class. El objeto serializado se convierte en formato JSON y se devuelve en la respuesta HTTP con un estado de HTTP 200 OK.",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        # Obtener la instancia de Colaborador a través de su identificador único
        colaborador_instance = self.get_object()

        # Serializar la instancia de Colaborador para convertirla en un objeto JSON
        colaborador_serializer = self.serializer_class(colaborador_instance)

        # Devolver la respuesta con el objeto JSON y un estado HTTP 200 OK
        return Response(colaborador_serializer.data, status=status.HTTP_200_OK)

"""
ETAPA 2 DEL LLENADO DE DATOS LABORALES DE UN COLABORADOR
"""
class UsuarioEmpresaDatosLaboralesCreateAPIView(generics.CreateAPIView):
    serializer_class = UsuarioEmpresaDatosLaboralesSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Crear datos laborales de usuario de empresa",
        operation_description="Crea datos laborales de un usuario de empresa, validando la información recibida y devolviendo la respuesta correspondiente.",
        security=[{"Bearer": []}]
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            # Validar si el serializer es válido, en caso contrario lanza una excepción y devuelve una respuesta de error
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                "data_serializer": serializer.data,
                "seguro_cesantia": get_tope_seguro_cesantia(request.data['ue_tipocontrato'])
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            # Capturar la excepción de validación del serializer y devolver la respuesta de error correspondiente
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Capturar cualquier otra excepción y devolver una respuesta de error genérica, además de registrar el error en el log
            logging.exception(f"Error en la vista {self.__class__.__name__}")
            return Response({'detail': 'Ha ocurrido un error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsuarioEmpresaDatosLaboralesDetailApiView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsuarioEmSerializers

    # Agregamos la documentación de Swagger para esta vista
    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Obtener información de empresa para usuario colaborador",
        operation_description="Este código define una vista documentada con Swagger en Django para obtener información de la empresa de un colaborador en particular. La vista utiliza una instancia de colaborador obtenida a través del ID de usuario en la URL para acceder al objeto UsuarioEmpresa del colaborador. Si hay algún error, se lanza una excepción Http404. Si todo sale bien, la información de UsuarioEmpresa se convierte en un diccionario y se devuelve en formato JSON con un código de estado HTTP 201 (creado). La documentación de Swagger incluye un manual_parameter para el token de autenticación y una descripción detallada de la operación.",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        try:
            # Obtenemos la instancia del colaborador a partir del ID de usuario en la URL
            colaborador_instance = self.get_object()

            # Obtenemos el objeto UsuarioEmpresa del colaborador
            usuario_empresa_object = UsuarioEmpresa.objects.filter(user=colaborador_instance)

            # Obtenemos una lista con los valores del objeto UsuarioEmpresa
            usuario_empresa = list(usuario_empresa_object.values())

            # Creamos un diccionario para guardar los valores de UsuarioEmpresa
            dic_usuario_empresa = {}

            # Iteramos sobre los valores de UsuarioEmpresa y los agregamos al diccionario
            for value in usuario_empresa:
                for key, val in value.items():
                    if key in get_key_colaborador_data():
                        dic_usuario_empresa[key] = val
            
            # Retornamos la información de UsuarioEmpresa en un diccionario
            return Response(dic_usuario_empresa, status=status.HTTP_201_CREATED)

        # Si el colaborador no existe, retornamos un error 404
        except Http404:
            return Response({"detail": "El colaborador no existe"}, status=status.HTTP_404_NOT_FOUND)

        # Si ocurre cualquier otra excepción, retornamos un error 500
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsuarioEmpresaDatosLaboralesUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuarioEmSerializers
    user_empresa_serializer = UsuarioEmpresaDatosLaboralesSerializers

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="Editar cargo",
        operation_description="Se actualiza toda la información de un cargo en particular",
        security=[{"Bearer": []}]
    )   
    def update(self, request, *args, **kwargs):
        # Obtenemos la instancia del colaborador a partir del ID de usuario en la URL
        colaborador_instance = self.get_object()

        # Obtenemos el objeto UsuarioEmpresa del colaborador
        usuario_empresa_object = UsuarioEmpresa.objects.filter(user=colaborador_instance)

        usuario_empresa_serializer = self.user_empresa_serializer(usuario_empresa_object[0], data=request.data['usuario_empresa'])
        if usuario_empresa_serializer.is_valid():
            usuario_empresa_serializer.save()

            # Creamos un diccionario para guardar los valores de UsuarioEmpresa
            dic_usuario_empresa = {}

             # Iteramos sobre los valores de UsuarioEmpresa y los agregamos al diccionario
            for value in usuario_empresa_object:
                for key, val in vars(value).items():
                    if key in get_key_colaborador_data():
                        dic_usuario_empresa[key] = val

            return Response(dic_usuario_empresa, status=status.HTTP_200_OK)
        return Response(usuario_empresa_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
ETAPA 3 DEL LLENADO DE UN COLABORADOR DATOS PREVISIONALES
"""
class DatosPrevisionalesColaboradorCreateAPIView(generics.CreateAPIView):

    queryset = UsuarioEmpresa.objects.all()
    serializer_class = DatosPrevisionalesUsuarioEmpresaDatosLaboralesSerializers 
    lookup_field = 'user_id'

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="",
        operation_description="",
        security=[{"Bearer": []}]
    )
    def post(self, request, *args, **kwargs):
        try:
            ue_cotizacion = 0

            # Obtener el objeto UsuarioEmpresa correspondiente al ID de usuario especificado
            usuario_empresa = UsuarioEmpresa.objects.get(user__id=int(self.kwargs['user_id']))
            
            # Obtener los objetos Afp y Salud correspondientes a los IDs enviados en la petición
            afp_id = request.data.get('afp')
            salud_id = request.data.get('salud')
            try:
                usuario_empresa.afp = Afp.objects.get(afp_id=afp_id)
            except Afp.DoesNotExist:
                response_data = {
                    "mensaje": f"No se encontró la AFP con ID {afp_id}"
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            try:
                usuario_empresa.salud = Salud.objects.get(sa_id=salud_id)
            except Salud.DoesNotExist:
                response_data = {
                    "mensaje": f"No se encontró la salud con ID {salud_id}"
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Validar que si la salud no es FONASA, se especifiquen valores para ue_ufisapre y ue_funisapre
            if not salud_id == 1:
                ue_ufisapre = request.data.get('ue_ufisapre')
                ue_funisapre = request.data.get('ue_funisapre')
                if ue_ufisapre is None or ue_funisapre is None:
                    response_data = {
                        "mensaje": "Para salud distintas de FONASA, debe especificar ue_ufisapre y ue_funisapre"
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                usuario_empresa.ue_ufisapre = ue_ufisapre
                usuario_empresa.ue_funisapre = ue_funisapre

                # Calcular la cotización de UF para la Unidad de Empleador (UE)
                uf = indicadores_economicos("uf")
                fecha_actual = uf['serie'][0]['fecha']
                valor_actual = uf['serie'][0]['valor']
                ue_cotizacion = round(float(usuario_empresa.ue_ufisapre) * float(valor_actual), 0)

            usuario_empresa.save()

            # Crea un diccionario con los datos del colaborador y el usuario
            response_data = {
                "user": usuario_empresa.user.id,
                "afp": usuario_empresa.afp.afp_id,
                "salud": usuario_empresa.salud.sa_id,
                "ue_ufisapre": usuario_empresa.ue_ufisapre,
                "ue_funisapre": usuario_empresa.ue_funisapre,
                "ue_cotizacion": ue_cotizacion,
            }

            # Retorna una respuesta con los datos y el código de estado HTTP 201 (Created)
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except ValueError:
            response_data = {
                "mensaje": "Datos inválidos en la petición"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        except UsuarioEmpresa.DoesNotExist:
            response_data = {
                "mensaje": "No se encontró el usuario especificado"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
        
        except (KeyError, TypeError):
            response_data = {
                "mensaje": "Petición mal formada"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
        
class DatosPrevisionalesColaboradorDetailApiView(generics.RetrieveAPIView):
    serializer_class = DatosPrevisionalesUsuarioEmpresaDatosLaboralesSerializers 
    lookup_field = 'user_id'

    def get_queryset(self):
        return None

    # Agregamos la documentación de Swagger para esta vista
    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="",
        operation_description="",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):

        try:
            # Obtener el objeto UsuarioEmpresa correspondiente al ID de usuario especificado
            usuario_empresa = UsuarioEmpresa.objects.filter(user__id=int(self.kwargs['user_id'])).first()

            # Calcular la cotización de UF para la Unidad de Empleador (UE)
            uf = indicadores_economicos("uf")
            fecha_actual = uf['serie'][0]['fecha']
            valor_actual = uf['serie'][0]['valor']
            ue_cotizacion = round(float(usuario_empresa.ue_ufisapre) * float(valor_actual), 0)

            # Crea un diccionario con los datos del colaborador y el usuario
            response_data = {
                "user": usuario_empresa.user.id,
                "afp": usuario_empresa.afp.afp_id,
                "salud": usuario_empresa.salud.sa_id,
                "ue_ufisapre": usuario_empresa.ue_ufisapre,
                "ue_funisapre": usuario_empresa.ue_funisapre,
                "ue_cotizacion": ue_cotizacion,
            }

            # Retornamos la información de UsuarioEmpresa en un diccionario
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except AttributeError as err:
            response_data = {
                "mensaje": err.args[0]
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        except UsuarioEmpresa.DoesNotExist:
            response_data = {
                "mensaje": "No se encontró el usuario especificado"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


"""
ETAPA 4 DEL LLENADO DE APV Y AHORRO VOLUNTARIO
"""
class ApvAhorroVoluntarioColaboradorCreateAPIView(generics.CreateAPIView):

    queryset = UsuarioEmpresa.objects.all()
    serializer_class = ApvAhorroVoluntarioUsuarioEmpresaDatosLaboralesSerializers 
    lookup_field = 'user_id'

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="",
        operation_description="",
        security=[{"Bearer": []}]
    )
    def post(self, request, *args, **kwargs):
        
        try:
            # Obtener el objeto UsuarioEmpresa correspondiente al ID de usuario especificado
            usuario_empresa = UsuarioEmpresa.objects.get(user__id=int(self.kwargs['user_id']))

            if request.data['ue_tieneapv'] == "S":
                usuario_empresa.ue_tieneapv = request.data['ue_tieneapv']
                usuario_empresa.ue_tipomontoapv = request.data['ue_tipomontoapv']
                usuario_empresa.ue_entidad_apv = request.data['ue_entidad_apv']
                usuario_empresa.ue_cotizacionvoluntaria = request.data['ue_cotizacionvoluntaria']

            else:
                usuario_empresa.ue_tieneapv = "N"

            if request.data['ue_tieneahorrovoluntario'] == "S":
                usuario_empresa.ue_tieneahorrovoluntario = request.data['ue_tieneahorrovoluntario']
                usuario_empresa.ue_ahorrovoluntario = request.data['ue_ahorrovoluntario']

            else:
                usuario_empresa.ue_tieneahorrovoluntario = "N"
            usuario_empresa.save()

            # Crea un diccionario con los datos del colaborador y el usuario
            response_data = {
                "ue_user_id": int(self.kwargs['user_id']),
                "ue_tieneapv": usuario_empresa.ue_tieneapv,
                "ue_tipomontoapv": usuario_empresa.ue_tipomontoapv,
                "ue_entidad_apv": usuario_empresa.ue_entidad_apv,
                "ue_cotizacionvoluntaria": usuario_empresa.ue_cotizacionvoluntaria,
                "ue_tieneahorrovoluntario": usuario_empresa.ue_tieneahorrovoluntario,
                "ue_ahorrovoluntario": usuario_empresa.ue_ahorrovoluntario
            }

            # Retorna una respuesta con los datos y el código de estado HTTP 201 (Created)
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except ValueError:
            response_data = {
                "mensaje": "Datos inválidos en la petición"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        except UsuarioEmpresa.DoesNotExist:
            response_data = {
                "mensaje": "No se encontró el usuario especificado"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
        
        except (KeyError, TypeError):
            response_data = {
                "mensaje": "Petición mal formada"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class ApvAhorroVoluntarioColaboradorDetailApiView(generics.RetrieveAPIView):

    serializer_class = DatosPrevisionalesUsuarioEmpresaDatosLaboralesSerializers 
    lookup_field = 'user_id'

    def get_queryset(self):
        return None

    # Agregamos la documentación de Swagger para esta vista
    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="",
        operation_description="",
        security=[{"Bearer": []}]
    )
    def get(self, request, *args, **kwargs):
        
        try:
            # Obtener el objeto UsuarioEmpresa correspondiente al ID de usuario especificado
            usuario_empresa = UsuarioEmpresa.objects.get(user__id=int(self.kwargs['user_id'])) 
        # Crea un diccionario con los datos del colaborador y el usuario
            response_data = {
                "ue_user_id": int(self.kwargs['user_id']),
                "ue_tieneapv": usuario_empresa.ue_tieneapv,
                "ue_tipomontoapv": usuario_empresa.ue_tipomontoapv,
                "ue_entidad_apv": usuario_empresa.ue_entidad_apv,
                "ue_cotizacionvoluntaria": usuario_empresa.ue_cotizacionvoluntaria,
                "ue_tieneahorrovoluntario": usuario_empresa.ue_tieneahorrovoluntario,
                "ue_ahorrovoluntario": usuario_empresa.ue_ahorrovoluntario
            }

            # Retorna una respuesta con los datos y el código de estado HTTP 201 (Created)
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except ValueError:
            response_data = {
                "mensaje": "Datos inválidos en la petición"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        except UsuarioEmpresa.DoesNotExist:
            response_data = {
                "mensaje": "No se encontró el usuario especificado"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
        
        except (KeyError, TypeError):
            response_data = {
                "mensaje": "Petición mal formada"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
"""
ETAPA 5 DEL LLENADO DE DATOS DE FINIQUITO
"""
class FiniquitoColaboradorCreateAPIView(generics.CreateAPIView):

    queryset = UsuarioEmpresa.objects.all()
    serializer_class = FiniquitoUsuarioEmpresaDatosLaboralesSerializers 
    lookup_field = 'user_id'

    @swagger_auto_schema(
        manual_parameters=[header_param],
        operation_id="",
        operation_description="",
        security=[{"Bearer": []}]
    )
    def post(self, request, *args, **kwargs):
        try:
            # Obtener el objeto UsuarioEmpresa correspondiente al ID de usuario especificado
            usuario_empresa = UsuarioEmpresa.objects.get(user__id=int(self.kwargs['user_id']))
            usuario_empresa.ue_tiponoticacion = request.data['ue_tiponoticacion']
            usuario_empresa.ue_fechanotificacioncartaaviso = request.data['ue_fechanotificacioncartaaviso']
            usuario_empresa.ue_fechatermino = request.data['ue_fechatermino']


            tablaGeneral = TablaGeneral.objects.get(
                tg_nombretabla = 'tb_causas_legales_finiquito',
                tg_idelemento = request.data['ue_causal']
                )

            usuario_empresa.ue_causal = tablaGeneral
            usuario_empresa.ue_fundamento = request.data['ue_fundamento']

            usuario_empresa.save()

        except ValueError:
            response_data = {
                "mensaje": "Datos inválidos en la petición"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        except UsuarioEmpresa.DoesNotExist:
            response_data = {
                "mensaje": "No se encontró el usuario especificado"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
        
        except (KeyError, TypeError):
            response_data = {
                "mensaje": "Petición mal formada"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 