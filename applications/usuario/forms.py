from django import forms
from django.contrib.auth.forms import User
from applications.base.models import Comuna, Pais, Region
from applications.base.utils import validarRut
from applications.empresa.models import (
    Afp, Apv, Banco, CajasCompensacion, Cargo, CentroCosto, Salud, Sucursal
)
from applications.security.models import Rol

from applications.usuario.models import Colaborador, Contact, FamilyResponsibilities, UsuarioEmpresa


class FormsForecastData(forms.ModelForm):
    tags_input_general = {
        'class': 'form-control',
        'autocomplete': 'off'
    }

    tags_input_select = {
        'class': 'form-control',
    }

    tags_input_select2 = {
        'class': 'form-control select2-show-search',
    }

    tags_input_date = {
        "class": "form-control fc-datepicker",
        "placeholder": "DD-MM-YYYY",
    }

    afp = forms.ModelChoiceField(label="AFPs", required=True,
                                 queryset=Afp.objects.filter(afp_activo="S"), widget=forms.Select(attrs=tags_input_select))
    salud = forms.ModelChoiceField(label="Salud", required=True,
                                   queryset=Salud.objects.filter(sa_activo="S"), widget=forms.Select(attrs=tags_input_select))
    ue_ufisapre = forms.FloatField(label="Monto UF",
                                   widget=forms.TextInput(attrs=tags_input_general), required=False)
    ue_funisapre = forms.CharField(label="FUN Isapre",
                                   widget=forms.TextInput(attrs=tags_input_general), required=False)
    ue_cotizacion = forms.FloatField(label="Cotización",
                                     widget=forms.TextInput(attrs=tags_input_general), required=False)
    ue_tieneapv = forms.ChoiceField(initial=0, label='Tiene APVI', choices=UsuarioEmpresa.OPCIONES,
                                    widget=forms.Select(attrs=tags_input_select), required=False)
    apv = forms.ModelChoiceField(label="APV", required=False,
                                 queryset=Apv.objects.filter(apv_activo="S"), widget=forms.Select(attrs=tags_input_select))
    ue_contributiontype = forms.ChoiceField(initial=0, label='Tipo de contribución', choices=UsuarioEmpresa.CONTRIBUTION_TYPE,
                                            widget=forms.Select(attrs=tags_input_select), required=False)
    ue_taxregime = forms.ChoiceField(initial=0, label='Régimen tributario', choices=UsuarioEmpresa.TAX_REGIME,
                                     widget=forms.Select(attrs=tags_input_select), required=False)
    ue_shape = forms.ChoiceField(initial=0, label='Forma del aporte', choices=UsuarioEmpresa.SHAPE,
                                 widget=forms.Select(attrs=tags_input_select), required=False)
    ue_apvamount = forms.FloatField(label="Monto",
                                    widget=forms.TextInput(attrs=tags_input_general), required=False)
    ue_paymentperioddate = forms.DateField(input_formats=["%d-%m-%Y"], label="Fecha Periodo pago",
                                                 widget=forms.DateInput(format="%d-%m-%Y",
                                                                        attrs=tags_input_date), required=False)
    caja_compensacion = forms.ModelChoiceField(label="Caja de compensacion", required=False,
                                               queryset=CajasCompensacion.objects.filter(cc_activo="S"), widget=forms.Select(attrs=tags_input_select))

    def clean_caja_compensacion(self):
        data = self.data["caja_compensacion"]
        if not data:
            self.add_error('caja_compensacion', "Debe escojer una caja de compensación")

    
    def clean_ue_tieneapv(self):
        data = self.data["ue_tieneapv"]

        if data == 'S':
            data_apv = self.data["apv"]
            data_ue_contributiontype = self.data["ue_contributiontype"]
            data_ue_taxregime = self.data["ue_taxregime"]
            data_ue_shape = self.data["ue_shape"]
            data_ue_apvamount = self.data["ue_apvamount"]
            data_ue_paymentperioddate = self.data["ue_paymentperioddate"]

            if len(data_apv) == 0:
                self.add_error('apv', "Debe escojer una APV")

            if int(data_ue_contributiontype) == 0:
                self.add_error('ue_contributiontype', "Debe escojer un tipo de contibución")

            if int(data_ue_taxregime) == 0:
                self.add_error('ue_taxregime', "Debe escojer un regimen tributario")

            if int(data_ue_shape) == 0:
                self.add_error('ue_shape', "Debe escojer una forma de aporte")

            if len(data_ue_apvamount) == 0 or float(data_ue_apvamount) == 0:
                self.add_error('ue_apvamount', "Debe escojer un monto")

            if len(data_ue_paymentperioddate) == 0:
                self.add_error('ue_paymentperioddate', "Debe escojer una fecha de periodo de pago")

        return data
    
    
    class Meta:
        model = UsuarioEmpresa
        fields = [
            'afp',
            'salud',
            'ue_ufisapre',
            'ue_funisapre',
            'ue_cotizacion',
            'ue_tieneapv',
            'apv',
            'ue_contributiontype',
            'ue_taxregime',
            'caja_compensacion',
            'ue_shape',
            'ue_apvamount',
            'ue_paymentperioddate'
        ]


class FormsPayments(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
        'autocomplete': 'off'
    }

    tags_input_select = {
        'class': 'form-control',
    }

    tags_input_select2 = {
        'class': 'form-control select2-show-search',
    }

    col_formapago = forms.ChoiceField(initial='', label='Forma de pago', choices=Colaborador.FORMA_PAGO,
                                      widget=forms.Select(attrs=tags_input_select), required=True)
    banco = forms.ModelChoiceField(label="Bancos", required=False,
                                   queryset=Banco.objects.filter(ban_activo="S"), widget=forms.Select(attrs=tags_input_select))
    col_tipocuenta = forms.ChoiceField(initial='', label='Tipo Cuenta', choices=Colaborador.TIPO_CUENTA_BANCARIA,
                                       widget=forms.Select(attrs=tags_input_select), required=False)
    col_cuentabancaria = forms.CharField(label="Cuenta bancaria",
                                         widget=forms.TextInput(attrs=tags_input_general), required=False)

    def clean_col_tipocuenta(self):
        data = len(self.cleaned_data.get("col_tipocuenta", None))
        data_col_formapago = int(self.cleaned_data.get("col_formapago", None))
        data_banco = self.cleaned_data.get("banco", None)

        if data_col_formapago == 4:
            if data == 0:
                self.add_error('col_tipocuenta',
                               "Debe escojer el tipo de cuenta")

            if not data_banco:
                self.add_error('banco', "Debe escojer el banco")

        return data

    class Meta:
        model = Colaborador
        fields = [
            'col_formapago',
            'banco',
            'col_tipocuenta',
            'col_cuentabancaria'
        ]


class DatosLaboralesForm(forms.ModelForm):
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

    tags_input_select2 = {
        'class': 'form-control select2-show-search',
    }

    tags_input_date = {
        "class": "form-control fc-datepicker",
        "placeholder": "DD-MM-YYYY",
    }

    cargo = forms.ModelChoiceField(label="Cargo", required=True,
                                   queryset=Cargo.objects.filter(car_activa="S"), widget=forms.Select(attrs=tags_input_select))
    centrocosto = forms.ModelChoiceField(label="Centro de Costo", required=True,
                                         queryset=CentroCosto.objects.filter(cencost_activo="S"), widget=forms.Select(attrs=tags_input_select))
    sucursal = forms.ModelChoiceField(label="Sucursal", required=True,
                                      queryset=Sucursal.objects.filter(suc_estado="S"), widget=forms.Select(attrs=tags_input_select))
    ue_fechacontratacion = forms.DateField(input_formats=["%d-%m-%Y"], label="Fecha Contratación",
                                           widget=forms.DateInput(format="%d-%m-%Y",
                                                                  attrs=tags_input_date), required=True)
    ue_fecharenovacioncontrato = forms.DateField(input_formats=["%d-%m-%Y"], label="Fecha Primer Contrato",
                                                 widget=forms.DateInput(format="%d-%m-%Y",
                                                                        attrs=tags_input_date), required=True)
    ue_fechatermino = forms.DateField(input_formats=["%d-%m-%Y"], label="Fecha Término Contrato",
                                      widget=forms.DateInput(format="%d-%m-%Y",
                                                             attrs=tags_input_date), required=False)
    ue_tipocontrato = forms.ChoiceField(initial=0, label='Tipo Contrato', choices=UsuarioEmpresa.TIPO_CONTRATO,
                                        widget=forms.Select(attrs=tags_input_select), required=True)
    ue_tipotrabajdor = forms.ChoiceField(initial=0, label='Tipo Trabajador', choices=UsuarioEmpresa.TIPO_TRABAJADOR,
                                         widget=forms.Select(attrs=tags_input_select), required=True)
    ue_estate = forms.ChoiceField(initial=0, label='Estado', choices=UsuarioEmpresa.ESTATE_JOB,
                                  widget=forms.Select(attrs=tags_input_select), required=True)

    class Meta:
        model = UsuarioEmpresa
        fields = [
            'cargo',
            'centrocosto',
            'sucursal',
            'ue_fechacontratacion',
            'ue_fecharenovacioncontrato',
            'ue_fechatermino',
            'ue_tipocontrato',
            'ue_tipotrabajdor',
            'ue_estate'
        ]


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
    col_tipousuario = forms.ChoiceField(
        label="Tipo de usuario", choices=Colaborador.TIPO_USUARIO, widget=forms.Select(attrs=tags_input_select), required=True)

    rol = forms.ModelChoiceField(label="Rol colaborador", required=True,
                                  queryset=Rol.objects.filter(rol_active = 'S', rol_client = 'S'), widget=forms.Select(attrs=tags_input_select))
    
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
            'col_tipolicencia',
            "col_tipousuario",
            "rol"
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


class FamilyResponsibilitiesForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
        'autocomplete': 'off'
    }

    tags_input_select = {
        'class': 'form-control',
    }

    tags_input_date = {
        "class": "form-control fc-datepicker",
        "placeholder": "DD-MM-YYYY",
    }


    fr_rut = forms.CharField(label="Rut", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    fr_sexo = forms.ChoiceField(label="Sexo", choices=FamilyResponsibilities.SEXO,
                                             widget=forms.Select(attrs=tags_input_select), required=True)
    fr_relationship = forms.ChoiceField(label="Parentezco", choices=FamilyResponsibilities.RELATIONSSHIP,
                                             widget=forms.Select(attrs=tags_input_select), required=True)
    fr_firstname = forms.CharField(label="Nombres", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    fr_lastname = forms.CharField(label="Apellidos", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    fr_fechanacimiento = forms.DateField(input_formats=["%d-%m-%Y"], label="Fecha nacimiento",
                                          widget=forms.DateInput(format="%d-%m-%Y",
                                                                 attrs=tags_input_date), required=True)

    def clean_fr_rut(self):
        data = self.cleaned_data["fr_rut"]

        if not validarRut(data):
            self.add_error('fr_rut', "El rut no es valido")
        return data

    class Meta:
        model = FamilyResponsibilities
        fields = [
            'fr_rut',
            'fr_sexo',
            'fr_relationship',
            'fr_firstname',
            'fr_lastname',
            'fr_fechanacimiento',
        ]