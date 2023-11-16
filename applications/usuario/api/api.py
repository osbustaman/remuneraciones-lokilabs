
from applications.empresa.models import Afp
from applications.usuario.models import Colaborador, Contact, FamilyResponsibilities
from applications.usuario.api.serializer import AfpSerializer, PersonalDataSerializer

from django.contrib.auth.models import User
from django.db.models import F, Value, CharField, Q
from django.db.models.functions import Concat

from rest_framework.response import Response
from rest_framework import generics, status, serializers
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from applications.base.models import Comuna, Region

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

            serialized_data["pais"] = data_objects[0].pais_id
            serialized_data["region"] = data_objects[0].region_id
            serialized_data["comuna"] = data_objects[0].comuna_id

            response_data = {
                "pk": id_user,
                "data": serialized_data
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
            )

            list_user = []
            for value in list_objects:
                list_user.append({
                    "user_id": value.id_user,
                    "id_col": value.id_col,
                    "full_name": value.full_name.title(),
                    "cargo": value.cargo_nombre.title(),
                    "centro_costo_nombre": value.centro_costo_nombre.title(),
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