from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from applications.base.models import Comuna, Pais, Region
from applications.base.utils import validarRut

from applications.usuario.models import Colaborador, Contact


class UserForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
        'autocomplete': 'off'
    }
    
    tags_input_readonly = {
        'class': 'form-control',
        'autocomplete': 'off',
        'readonly': 'readonly'
    }

    tags_input_select = {
        'class': 'form-control',
    }

    username = forms.CharField(label="Usuario",
                               widget=forms.TextInput(attrs=tags_input_readonly), required=True)
    first_name = forms.CharField(label="Nombres",
                                 widget=forms.TextInput(attrs=tags_input_general), required=True)
    last_name = forms.CharField(label="Apellidos",
                                widget=forms.TextInput(attrs=tags_input_general), required=True)
    email = forms.EmailField(label="Email",
                             widget=forms.TextInput(attrs=tags_input_general), required=True)
    password = forms.CharField(label="Contraseña",
                               widget=forms.PasswordInput(attrs=tags_input_readonly), required=False)

    def clean_username(self):
        data = self.cleaned_data["username"]

        if not validarRut(data):
            self.add_error('username', "El rut no es valido")
        return data
        
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]


class ColaboradorForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
        'autocomplete': 'off'
    }

    tags_input_select = {
        'class': 'form-control',
    }

    tags_input_file = {
        'class': 'custom-file-input',
    }

    tags_input_date = {
        "class": "form-control fc-datepicker",
        "placeholder": "DD-MM-YYYY",
    }

    tags_input_select2 = {
        'class': 'form-control select2-show-search',
    }


    col_rut = forms.CharField(label="Rut", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    col_extranjero = forms.ChoiceField(initial=0, label='Extranjero?', choices=Colaborador.OPCIONES,
                                       widget=forms.Select(attrs=tags_input_select), required=True)
    col_nacionalidad = forms.CharField(label="Nacionalidad", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    col_sexo = forms.ChoiceField(initial=0, label='Sexo', choices=Colaborador.SEXO,
                                 widget=forms.Select(attrs=tags_input_select), required=True)
    col_fechanacimiento = forms.DateField(input_formats=["%d-%m-%Y"], label="Fecha nacimiento",
                                          widget=forms.DateInput(format="%d-%m-%Y",
                                                                 attrs=tags_input_date), required=True)
    col_estadocivil = forms.ChoiceField(initial=1, label='Estado Civil', choices=Colaborador.ESTADO_CIVIL,
                                        widget=forms.Select(attrs=tags_input_select), required=True)
    col_direccion = forms.CharField(label="Dirección", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    pais = forms.ModelChoiceField(label="País", required=True,
                                  queryset=Pais.objects.all(), widget=forms.Select(attrs=tags_input_select2))
    region = forms.ModelChoiceField(label="Región", required=True,
                                    queryset=Region.objects.all(), widget=forms.Select(attrs=tags_input_select2))
    comuna = forms.ModelChoiceField(label="Comuna", required=True,
                                    queryset=Comuna.objects.all(), widget=forms.Select(attrs=tags_input_select2))
    col_estudios = forms.ChoiceField(label="Tipo estudios", choices=Colaborador.TIPO_ESTUDIOS,
                                     widget=forms.Select(attrs=tags_input_select), required=True)
    col_estadoestudios = forms.ChoiceField(
        label="Estado estudios", choices=Colaborador.ESTADO_ESTUDIOS, widget=forms.Select(attrs=tags_input_select), required=True)
    col_titulo = forms.CharField(label="Titulo", widget=forms.TextInput(
        attrs=tags_input_general), required=False)

    col_licenciaconducir = forms.ChoiceField(initial=0, label='Licencia conducir', choices=Colaborador.OPCIONES,
                                             widget=forms.Select(attrs=tags_input_select), required=True)
    col_tipolicencia = forms.CharField(label="Clase", widget=forms.TextInput(
        attrs=tags_input_general), required=False)
    
    def clean_col_rut(self):
        data = self.cleaned_data["col_rut"]

        if not validarRut(data):
            self.add_error('col_rut', "El rut no es valido")
        return data

    class Meta:
        model = Colaborador
        fields = [
            'col_rut',
            'col_extranjero',
            'col_nacionalidad',
            'col_sexo',
            'col_fechanacimiento',
            'col_estadocivil',
            'col_direccion',
            'pais',
            'region',
            'comuna',
            'col_estudios',
            'col_estadoestudios',
            'col_titulo',
            'col_licenciaconducir',
            'col_tipolicencia'
        ]


class ContactForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
        'autocomplete': 'off'
    }

    tags_input_select = {
        'class': 'form-control',
    }

    con_contact_type = forms.ChoiceField(initial=0, label='Tipo de Contacto', choices=Contact.TYPE,
                                             widget=forms.Select(attrs=tags_input_select), required=True)
    con_mail_contact = forms.EmailField(label="Correo",
                                widget=forms.TextInput(attrs=tags_input_general), required=False)
    con_phone_contact = forms.CharField(label="Teléfono",
                                widget=forms.TextInput(attrs=tags_input_general), required=False)
    cont_name_contact = forms.CharField(label="Nombre Contacto",
                                widget=forms.TextInput(attrs=tags_input_general), required=True)
        
    class Meta:
        model = Contact
        fields = [
            'con_contact_type',
            'con_mail_contact',
            'con_phone_contact',
            'cont_name_contact',
        ]

