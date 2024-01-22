import datetime
from applications.base.api.serializer import UserSerializer
from applications.base.utils import validarRut, validate_mail
from applications.empresa.models import Afp, Cargo, CentroCosto, Empresa, Sucursal
from applications.security.models import Rol
from applications.usuario.models import Colaborador, Contact, FamilyResponsibilities, UsuarioEmpresa
from applications.usuario.api.serializer import (
    AfpSerializer
    , CentroCostosSerializer
    , CentroSucursalSerializer
    , ComunsSerializer,
    LaboralDataPersonalSerializer
    , PersonalDataSerializer
    , CargosSerializer
)

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F, Value, CharField, Q
from django.db.models.functions import Concat
from django.urls import reverse

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics, status, serializers
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from applications.base.models import Comuna, Pais, Region


@permission_classes([AllowAny])
class LoadPersonlaDataPage(generics.GenericAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        try:
            user_id = int(self.kwargs.get(self.lookup_field))
            data_user = User.objects.get(id=user_id)
            return data_user
        except User.DoesNotExist:
            return False

    def get(self, request, *args, **kwargs):

        data_user = self.get_queryset()

        if not data_user:
            raise NotFound(detail="Colaborador no encontrado")
        
        try:
            get_serializer = self.serializer_class(data_user)
            return Response(get_serializer.data, status=status.HTTP_200_OK)
        except NotFound as ex:
            return Response({"message": str(ex)}, status=status.HTTP_404_NOT_FOUND)




@permission_classes([AllowAny])
class EditLaboralDataPersonalApiView(generics.UpdateAPIView):
    serializer_class = LaboralDataPersonalSerializer

    def get_queryset(self):
        user_id = int(self.kwargs.get(self.lookup_field))
        objects_user_company = UsuarioEmpresa.objects.filter(user_id=user_id)
        return objects_user_company

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            raise NotFound(detail="Colaborador no encontrado")

        serializer = self.get_serializer(queryset.first(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            ue_fechatermino = request.data.get('ue_fechatermino')
            if ue_fechatermino:
                first_object = queryset.first()
                first_object.ue_fechatermino = datetime.datetime.strptime(ue_fechatermino, '%Y-%m-%d').date()
                first_object.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class GetListDataPageDatosLaborales(generics.ListAPIView):

    serializer_class = LaboralDataPersonalSerializer
    
    def get_queryset(self):
        try:
            user_id = int(self.kwargs.get(self.lookup_field))
        except ValueError:
            return Response({"message": "Falta parametro de usuario para ejecutar el proceso"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            queryset = UsuarioEmpresa.objects.filter(user_id = user_id)
        except UsuarioEmpresa.DoesNotExist:
            return Response({"message": "No existe colaborador asociado"}, status=status.HTTP_404_NOT_FOUND)
        except TypeError as ex:
            return Response({"message": str(ex)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_404_NOT_FOUND)
        
        return queryset

    def get(self, request, *args, **kwargs):

        try:
            queryset= self.get_queryset()
            serializer = self.get_serializer(queryset, many = True)
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_404_NOT_FOUND)
        
        tipo_contrato_dict = {key: value for key, value in UsuarioEmpresa.TIPO_CONTRATO}
        type_job_dict = {key: value for key, value in UsuarioEmpresa.TIPO_TRABAJADOR}
        state_job_dict = {key: value for key, value in UsuarioEmpresa.ESTATE_JOB}
        worker_sector_dict = {key: value for key, value in UsuarioEmpresa.WORKER_SECTOR}
        all_days_dict = {key: value for key, value in UsuarioEmpresa.ALL_DAYS}

        serializer.data[0]["ue_fechatermino"] = queryset.first().ue_fechatermino

        data_page = {
            "tipo_contrato_dict": tipo_contrato_dict,
            "type_job_dict": type_job_dict,
            "state_job_dict": state_job_dict,
            "worker_sector_dict": worker_sector_dict,
            "all_days_dict": all_days_dict,
            "data_colaborator": serializer.data,
        }
        return Response(data_page, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class GetSucursalApiView(generics.ListAPIView):
    serializer_class = CentroSucursalSerializer

    def get_object(self):
        list_sucursal = Sucursal.objects.filter(suc_estado = "S")
        return list_sucursal

    def get(self, request, *args, **kwargs):
        list_sucursal = self.get_object()
        dict_sucursal = list(list_sucursal.values())
        return Response(dict_sucursal, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class GetCentroCostosApiView(generics.ListAPIView):
    serializer_class = CentroCostosSerializer

    def get_object(self):
        list_ccostos = CentroCosto.objects.filter(cencost_activo = "S")
        return list_ccostos

    def get(self, request, *args, **kwargs):
        list_ccostos = self.get_object()
        dict_ccostos = list(list_ccostos.values())
        return Response(dict_ccostos, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class GetCargosApiView(generics.ListAPIView):
    serializer_class = CargosSerializer

    def get_object(self):
        list_cargos = Cargo.objects.filter(car_activa = "S")
        return list_cargos

    def get(self, request, *args, **kwargs):
        list_cargos = self.get_object()
        dict_cargos = list(list_cargos.values())
        return Response(dict_cargos, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class GetComunsListApiView(generics.ListAPIView):
    queryset = Comuna.objects.all()
    serializer_class = ComunsSerializer

    def get_object(self):
        region_id = int(self.kwargs.get(self.lookup_field))
        list_comunas = Comuna.objects.filter(region__re_id = region_id)

        if not list_comunas:
            return Response({"message": "No existen comunas asociadas a la región"}, status=status.HTTP_404_NOT_FOUND)
        return list_comunas
    
    def get(self, request, *args, **kwargs):
        list_comunas = self.get_object()
        dict_comunas = list(list_comunas.values())
        return Response(dict_comunas, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class LoadPersonalDataPageView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):

        objects_countries = Pais.objects.all()
        objects_regions = Region.objects.all()

        sexo_dict = {key: value for key, value in Colaborador.SEXO}
        estado_civil_dict = {key: value for key, value in Colaborador.ESTADO_CIVIL}
        opciones_dict = {key: value for key, value in Colaborador.OPCIONES}
        estados_estudios_dict = {key: value for key, value in Colaborador.ESTADO_ESTUDIOS}
        tipo_estudios_dict = {key: value for key, value in Colaborador.TIPO_ESTUDIOS}

        object_rol = Rol.objects.filter(rol_active = 'S', rol_client = 'S')

        response_data = {
            "countries": list(objects_countries.values()),
            "regions": list(objects_regions.values()),
            "listado_roles": list(object_rol.values()),
            "sexo_dict": sexo_dict,
            "estado_civil_dict": estado_civil_dict,
            "opciones_dict": opciones_dict,
            "estados_estudios_dict": estados_estudios_dict,
            "tipo_estudios_dict": tipo_estudios_dict,
        }
        return Response(response_data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class PersonalDataCreateView(generics.CreateAPIView):
    serializer_class = PersonalDataSerializer

    def get_object(self, request):
        obj = Colaborador.objects.filter(col_rut=request.data['col_rut']).first()
        return obj

    def post(self, request, *args, **kwargs):

        """
        Actualiza un colaborador existente.
        
        :param self: instancia de la clase.
        :param request: objeto de solicitud HTTP.
        :param args: argumentos posicionales adicionales.
        :param kwargs: argumentos de palabra clave adicionales.
        :return: respuesta HTTP con los resultados de la actualización o mensajes de error.
        """

        user_colaborator = self.get_object(request)

        if user_colaborator:
            return Response({"message": "El colaborador ya existe"}, status=status.HTTP_409_CONFLICT)

        if not validarRut(request.data['col_rut']):
            return Response({"message": "Rut no válido"}, status=status.HTTP_404_NOT_FOUND)
        
        if not validate_mail(request.data['email']):
            return Response({"message": "Correo no válido"}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualización del modelo User
        try:
            user = User()
            user.username = request.data['col_rut']
            user.last_name = request.data['nombres']
            user.first_name = request.data['apellidos']
            user.email = request.data['email']
            user.is_staff = True
            user.is_superuser = False
            user.set_password(request.data['col_rut'])
            user.save()
        except User.DoesNotExist:
            transaction.set_rollback(True)
            return Response({"message": "Colaborador no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Validación y actualización del modelo Colaborador
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            try:
                object_colaborador = Colaborador()
                object_colaborador.user = user
                object_colaborador.col_rut = request.data['col_rut']
                object_colaborador.col_extranjero = request.data['col_extranjero']
                object_colaborador.col_nacionalidad = request.data['col_nacionalidad']
                object_colaborador.col_sexo = request.data['col_sexo']
                object_colaborador.col_fechanacimiento = request.data['col_fechanacimiento']
                object_colaborador.col_estadocivil = request.data['col_estadocivil']
                object_colaborador.col_direccion = request.data['col_direccion']
                object_colaborador.pais = Pais.objects.get(pa_id = request.data['pais'])
                object_colaborador.region = Region.objects.get(re_id = request.data['region'])
                object_colaborador.comuna = Comuna.objects.get(com_id = request.data['comuna'])
                object_colaborador.col_estudios = request.data['col_estudios']
                object_colaborador.col_estadoestudios = request.data['col_estadoestudios']
                object_colaborador.col_titulo = request.data['col_titulo']
                object_colaborador.col_licenciaconducir = request.data['col_licenciaconducir']
                object_colaborador.col_tipolicencia = request.data['col_tipolicencia']
                object_colaborador.col_tipousuario = Rol.objects.get(rol_id = request.data['col_tipousuario'])

                object_colaborador.save()

                object_empresa = Empresa.objects.get(emp_id = int(request.session['la_empresa']))
                usuario_empresa = UsuarioEmpresa()
                usuario_empresa.user = user
                usuario_empresa.empresa = object_empresa
                usuario_empresa.save()

                response_data = {
                    "user_id": user.id,
                    "col_id": object_colaborador.col_id,
                }

                return Response(response_data, status=status.HTTP_201_CREATED)
            except Colaborador.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"message": "Colaborador no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            except Pais.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"message": "Pais no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            except Region.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"message": "Región no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            except Comuna.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"message": "Comuna no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            except Rol.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"message": "Rol no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        transaction.set_rollback(True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class PersonalDataEditView(generics.UpdateAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = PersonalDataSerializer

    def get_object(self):
        user_id = self.kwargs.get(self.lookup_field)
        obj = Colaborador.objects.filter(user_id=user_id).first()
        return obj

    def put(self, request, *args, **kwargs):

        """
        Actualiza un colaborador existente.
        
        :param self: instancia de la clase.
        :param request: objeto de solicitud HTTP.
        :param args: argumentos posicionales adicionales.
        :param kwargs: argumentos de palabra clave adicionales.
        :return: respuesta HTTP con los resultados de la actualización o mensajes de error.
        """


        instance = self.get_object()

        if not validarRut(request.data['col_rut']):
            return Response({"message": "Rut no válido"}, status=status.HTTP_404_NOT_FOUND)
        
        if not validate_mail(request.data['email']):
            return Response({"message": "Correo no válido"}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualización del modelo User
        try:
            user = User.objects.get(username=request.data['col_rut'])
            user.last_name = request.data['nombres']
            user.first_name = request.data['apellidos']
            user.email = request.data['email']
            user.save()
        except User.DoesNotExist:
            return Response({"message": "Colaborador no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Validación y actualización del modelo Colaborador
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():

            try:
                object_colaborador = Colaborador.objects.get(user=user)
                object_colaborador.col_extranjero = request.data['col_extranjero']
                object_colaborador.col_nacionalidad = request.data['col_nacionalidad']
                object_colaborador.col_sexo = request.data['col_sexo']
                object_colaborador.col_fechanacimiento = request.data['col_fechanacimiento']
                object_colaborador.col_estadocivil = request.data['col_estadocivil']
                object_colaborador.col_direccion = request.data['col_direccion']
                object_colaborador.pais = Pais.objects.get(pa_id = request.data['pais'])
                object_colaborador.region = Region.objects.get(re_id = request.data['region'])
                object_colaborador.comuna = Comuna.objects.get(com_id = request.data['comuna'])
                object_colaborador.col_estudios = request.data['col_estudios']
                object_colaborador.col_estadoestudios = request.data['col_estadoestudios']
                object_colaborador.col_titulo = request.data['col_titulo']
                object_colaborador.col_licenciaconducir = request.data['col_licenciaconducir']
                object_colaborador.col_tipolicencia = request.data['col_tipolicencia']
                object_colaborador.col_tipousuario = Rol.objects.get(rol_id = request.data['col_tipousuario'])

                object_colaborador.save()
            except Colaborador.DoesNotExist:
                return Response({"message": "Colaborador no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            except Pais.DoesNotExist:
                return Response({"message": "Pais no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            except Region.DoesNotExist:
                return Response({"message": "Región no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            except Comuna.DoesNotExist:
                return Response({"message": "Comuna no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            except Rol.DoesNotExist:
                return Response({"message": "Rol no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class ApiLoadPageColaborator(generics.ListAPIView):
    """
    
    """

    def get(self, request, *args, **kwargs):

        object_pais = Pais.objects.all()
        dicc_paises = list(object_pais.values())

        object_region = Region.objects.all()
        dicc_region = list(object_region.values())

        sexo_dict = {key: value for key, value in Colaborador.SEXO}
        estado_civil_dict = {key: value for key, value in Colaborador.ESTADO_CIVIL}
        opciones_dict = {key: value for key, value in Colaborador.OPCIONES}
        estados_estudios_dict = {key: value for key, value in Colaborador.ESTADO_ESTUDIOS}
        tipo_estudios_dict = {key: value for key, value in Colaborador.TIPO_ESTUDIOS}


        object_rol = Rol.objects.filter(rol_active = 'S', rol_client = 'S')
        dicc_object_rol = list(object_rol.values())

        response_data = {
            "paises": dicc_paises,
            "regiones": dicc_region,
            "sexo_dict": sexo_dict,
            "estado_civil_dict": estado_civil_dict,
            "opciones_dict": opciones_dict,
            "estados_estudios_dict": estados_estudios_dict,
            "tipo_estudios_dict": tipo_estudios_dict,
            "object_rol_dict": dicc_object_rol
        }

        return Response(response_data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class ApiGetPersonalData(generics.GenericAPIView):

    queryset = Colaborador.objects.all()
    serializer_class = PersonalDataSerializer

    def get(self, request, *args, **kwargs):
        try:
            id_user = int(kwargs['pk'])

            data_objects = Colaborador.objects.filter(
                user_id=id_user
            ).annotate(
                id_user=F('user__id'),
                rut=F('user__colaborador__col_rut'),
                extranjero=F('user__colaborador__col_extranjero'),
                nacionalidad=F('user__colaborador__col_nacionalidad'),
                sexo=F('user__colaborador__col_sexo'),
                fechanacimiento=F('user__colaborador__col_fechanacimiento'),
                estadocivil=F('user__colaborador__col_estadocivil'),
                direccion=F('user__colaborador__col_direccion'),
                estudios=F('user__colaborador__col_estudios'),
                estadoestudios=F('user__colaborador__col_estadoestudios'),
                titulo=F('user__colaborador__col_titulo'),
                licenciaconducir=F('user__colaborador__col_licenciaconducir'),
                tipolicencia=F('user__colaborador__col_tipolicencia'),
                tipousuario=F('user__colaborador__col_tipousuario')
            )

            if not data_objects.exists():
                return Response({"error": "Usuario no existe"}, status=status.HTTP_404_NOT_FOUND)

            # Serializar los datos obtenidos
            serializer = self.serializer_class(data=data_objects, many=True)
            serializer.is_valid()  # Validar los datos
            serialized_data = serializer.data  # Obtener los datos serializados

            serialized_data[0]["pais"] = data_objects[0].pais_id
            serialized_data[0]["region"] = data_objects[0].region_id
            serialized_data[0]["comuna"] = data_objects[0].comuna_id
            serialized_data[0]["first_name"] = data_objects[0].user.first_name
            serialized_data[0]["last_name"] = data_objects[0].user.last_name
            serialized_data[0]["email"] = data_objects[0].user.email

            object_pais = Pais.objects.all()
            object_regions = Region.objects.filter(pais = data_objects[0].pais)
            object_comuns = Comuna.objects.filter(region = data_objects[0].region)

            response_data = {
                "pk": id_user,
                "data": serialized_data,
                "regions": list(object_regions.values()),
                "comuns": list(object_comuns.values()),
                "countries": list(object_pais.values())
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except TypeError:
            response_data = {
                "error": "El registro del colaborador esta incompleto"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([AllowAny])
class AfpDetailApiView(generics.RetrieveAPIView):
    queryset = Afp.objects.all()
    serializer_class = AfpSerializer

    def get(self, request, *args, **kwargs):
        try:
            object = self.queryset.filter(afp_id=self.kwargs['pk'])
            if object.exists():
                data = list(object.values())
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                raise IndexError("La AFP no existe")
        except IndexError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class ListColaborate(generics.ListAPIView):
    queryset = None

    def get(self, request, *args, **kwargs):
        try:
            list_objects = Colaborador.objects.filter(
                user__usuarioempresa__empresa_id=self.kwargs['pk']
            ).annotate(
                id_user=F('user__id'),
                id_col=F('user__colaborador__col_id'),
                rut=F('user__colaborador__col_rut'),
                full_name=Concat('user__first_name', Value(' '), 'user__last_name'),
                cargo_nombre=F('user__usuarioempresa__cargo__car_nombre'),
                centro_costo_nombre=F('user__usuarioempresa__centrocosto__cencost_nombre'),
            ).order_by('full_name', 'rut')

            list_user = []
            for value in list_objects:
                list_user.append({
                    "user_id": value.id_user,
                    "id_col": value.id_col,
                    "full_name": value.full_name.title(),
                    "cargo": value.cargo_nombre.title() if value.cargo_nombre and value.cargo_nombre.strip() else "Sin asignar",
                    "centro_costo_nombre": value.centro_costo_nombre.title() if value.centro_costo_nombre and value.centro_costo_nombre.strip() else "Sin asignar",
                    "rut": value.rut,
                })

            return Response(list_user, status=status.HTTP_200_OK)
        except IndexError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class ApiGetDataUserPage(generics.ListAPIView):
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            object = self.queryset.filter(id=self.kwargs['pk'])
            if object.exists():
                object = object.first()
                last_name = (object.last_name).split(" ")

                object_colaborator = Colaborador.objects.get(user = object)

                object_contact = Contact.objects.filter(
                    Q(user=object) & (Q(con_contact_type=1))
                ).first()

                object_contact_phone = Contact.objects.filter(
                    Q(user=object) & (Q(con_contact_type=3) | Q(con_contact_type=4))
                ).first()

                object_regiones = Region.objects.all()
                regiones_dict_list = list(object_regiones.values())

                object_comunas = Comuna.objects.filter(region = object_colaborator.region)
                object_comunas_dict_list = list(object_comunas.values())

                objects_family_dict_list = FamilyResponsibilities.objects.filter(user = object)

                family_dict_list = []
                for value in objects_family_dict_list:
                    family_dict_list.append({
                        "fr_id": value.fr_id,
                        "fr_firstname": value.fr_firstname,
                        "fr_lastname": value.fr_lastname,
                        "fr_rut": value.fr_rut,
                        "fr_fechanacimiento": value.fr_fechanacimiento,
                        "fr_sexo": value.get_fr_sexo_display(),
                        "fr_relationship": value.get_fr_relationship_display()
                    })

                data = {
                    "username": object.username,
                    "first_name": object.first_name,
                    "first_last_name": last_name[0] if len(last_name) > 0 else '',
                    "second_last_name": last_name[1] if len(last_name) > 1 else '',
                    "col_fechanacimiento": object_colaborator.col_fechanacimiento,
                    "col_sexo": object_colaborator.get_col_sexo_display().title(),
                    "col_estadocivil": str(object_colaborator.col_estadocivil),
                    "phone_user": object_contact_phone.con_phone_contact if object_contact_phone and object_contact_phone.con_phone_contact else '',
                    #"phone_user": "",
                    "email_corporativo": object.email,
                    "email_personal": object_contact.con_mail_contact if object_contact and hasattr(object_contact, 'con_mail_contact') and object_contact.con_mail_contact else '@',
                    #"email_personal": "",
                    "col_direccion": object_colaborator.col_direccion,
                    "col_region": object_colaborator.region.re_id,
                    "col_comuna": object_colaborator.comuna.com_id,
                    "col_banco": object_colaborator.banco.ban_nombre,
                    "col_formapago": object_colaborator.col_formapago,
                    "col_formapago_name": object_colaborator.get_col_formapago_display(),
                    "col_tipocuenta_name": object_colaborator.get_col_tipocuenta_display(),
                    "col_cuentabancaria": object_colaborator.col_cuentabancaria,
                    "regiones_list_dict": regiones_dict_list,
                    "comunas_dict_list": object_comunas_dict_list,
                    "objects_family_dict_list": family_dict_list,
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                raise IndexError("El usuario no existe")
        except Colaborador.DoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Contact.DoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IndexError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)