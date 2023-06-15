from django import forms
from django.contrib.auth.models import User

from applications.base.models import Cliente, Comuna, Pais, Region
from applications.base.utils import validarRut


class ClientForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
    }

    tags_input_date = {
        "class": "form-control",
    }

    nombre_cliente = forms.CharField(label="Nombre del cliente (empresa)*", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    rut_cliente = forms.CharField(label="Rut del cliente*", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    imagen_cliente = forms.ImageField(label="Subir logo del cliente", widget=forms.FileInput(
        attrs=tags_input_general), required=False)
    cliente_activo = forms.ChoiceField(initial='S', label='Cliente activo', choices=Cliente.OPCIONES,
                                      widget=forms.Select(attrs=tags_input_general), required=False)
    fecha_ingreso = forms.DateField(input_formats=["%d-%m-%Y"], label="Fecha de ingreso*",
                                    widget=forms.DateInput(format="%d-%m-%Y",
                                                           attrs=tags_input_date), required=True)
    fecha_termino = forms.DateField(input_formats=["%d-%m-%Y"], label="Fecha de termino*",
                                    widget=forms.DateInput(format="%d-%m-%Y",
                                                           attrs=tags_input_date), required=False)
    cantidad_usuarios = forms.IntegerField(
        label="Cantidad de usuarios*", widget=forms.TextInput(attrs=tags_input_general), required=True)
    nombre_representante = forms.CharField(label="Nombre del representante*", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    rut_representante = forms.CharField(label="Rut del representante*", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    correo_representante = forms.EmailField(label="Email cliente*", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    telefono_representante = forms.CharField(label="Teléfono de cliente*", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    direccion_representante = forms.CharField(label="Nombre del cliente*", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    pais = forms.ModelChoiceField(label="País", required=False,
                                  queryset=Pais.objects.all(), widget=forms.Select(attrs=tags_input_general))
    region = forms.ModelChoiceField(label="Región", required=False,
                                    queryset=Region.objects.all(), widget=forms.Select(attrs=tags_input_general))
    comuna = forms.ModelChoiceField(label="Comuna", required=False,
                                    queryset=Comuna.objects.all(), widget=forms.Select(attrs=tags_input_general))

    def clean_rut_cliente(self):
        data = self.cleaned_data["rut_cliente"]

        if not validarRut(data):
            self.add_error('rut_cliente', "El rut no es valido")
        return data

    def clean_rut_representante(self):
        data = self.cleaned_data["rut_representante"]

        if not validarRut(data):
            self.add_error('rut_representante', "El rut no es valido")
        return data

    def clean_cantidad_usuarios(self):
        data = self.cleaned_data["cantidad_usuarios"]

        if data <= 0:
            self.add_error('cantidad_usuarios', "La cantidad de usuarios debe ser mayor a cero")

        return data

    def clean_fecha_termino(self):
        fecha_ingreso = self.cleaned_data["fecha_ingreso"]
        fecha_termino = self.cleaned_data["fecha_termino"]

        if fecha_termino and fecha_termino <= fecha_ingreso:
            self.add_error('fecha_termino', "La fecha de término debe ser posterior a la fecha de ingreso")

        return fecha_termino

    class Meta:
        model = Cliente
        fields = (
            "nombre_cliente"
            , "rut_cliente"
            , "imagen_cliente"
            , "cliente_activo"
            , "fecha_ingreso"
            , "fecha_termino"
            , "cantidad_usuarios"
            , "nombre_representante"
            , "rut_representante"
            , "correo_representante"
            , "telefono_representante"
            , "direccion_representante"
            , "pais"
            , "region"
            , "comuna"
        )


class AdminUserForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
    }

    username = forms.CharField(widget=forms.TextInput(attrs=tags_input_general), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs=tags_input_general), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs=tags_input_general), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs=tags_input_general), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs=tags_input_general), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']