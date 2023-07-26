from django import forms

from applications.base.models import Comuna, Pais, Region
from applications.base.utils import validarRut
from applications.empresa.models import CajasCompensacion, Cargo, CentroCosto, Empresa, GrupoCentroCosto, MutualSecurity, Sucursal

class CentroCostoForm(forms.ModelForm):
    tags_input_general = {
        'class': 'form-control',
    }

    tags_input_readonly = {
        'class': 'form-control',
        'readonly': 'readonly'
    }

    cencost_nombre= forms.CharField(label="Nombre CC", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    cencost_codigo = forms.CharField(label="Código CC", widget=forms.TextInput(
        attrs=tags_input_readonly), required=False)
    cencost_activo = forms.ChoiceField(initial='S', label='CC Activo?', choices=GrupoCentroCosto.OPCIONES,
                                      widget=forms.Select(attrs=tags_input_general), required=False)

    class Meta:
        model = CentroCosto
        fields = (
            "cencost_nombre"
            , "cencost_codigo"
            , "cencost_activo"
        )

class GrupoCentroCostoForm(forms.ModelForm):
    tags_input_general = {
        'class': 'form-control',
    }

    tags_input_readonly = {
        'class': 'form-control',
        'readonly': 'readonly'
    }

    gcencost_nombre = forms.CharField(label="Nombre Grupo CC", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    gcencost_codigo = forms.CharField(label="Código Grupo CC", widget=forms.TextInput(
        attrs=tags_input_readonly), required=False)
    gcencost_activo = forms.ChoiceField(initial='S', label='Grupo CC Activo?', choices=GrupoCentroCosto.OPCIONES,
                                      widget=forms.Select(attrs=tags_input_general), required=False)

    class Meta:
        model = GrupoCentroCosto
        fields = (
            "gcencost_nombre"
            , "gcencost_codigo"
            , "gcencost_activo"
        )

class CargoForm(forms.ModelForm):
    tags_input_general = {
        'class': 'form-control',
    }

    car_nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_general), required=True)

    class Meta:
        model = Cargo
        fields = (
            "car_nombre",
        )

class SucursalForm(forms.ModelForm):
    tags_input_general = {
        'class': 'form-control',
    }

    tags_input_readonly = {
        'class': 'form-control',
        'readonly': 'readonly'
    }

    tags_input_select2 = {
        'class': 'form-control select2-show-search',
    }

    

    suc_codigo = forms.CharField(label="Código", widget=forms.TextInput(
        attrs=tags_input_readonly), required=False)
    suc_descripcion = forms.CharField(label="Descripción", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    suc_direccion = forms.CharField(label="Dirección", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    pais = forms.ModelChoiceField(label="País", required=True,
                                  queryset=Pais.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    region = forms.ModelChoiceField(label="Región", required=True,
                                    queryset=Region.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    comuna = forms.ModelChoiceField(label="Comuna", required=True,
                                    queryset=Comuna.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    suc_estado = forms.ChoiceField(initial='S', label='Sucursal Activa?', choices=Sucursal.OPCIONES,
                                      widget=forms.Select(attrs=tags_input_general), required=False)
    
    class Meta:
        model = Sucursal
        fields = (
            "suc_codigo"
            , "suc_descripcion"
            , "suc_direccion"
            , "pais"
            , "region"
            , "comuna"
            , "suc_estado"
        )

class EmpresaForm(forms.ModelForm):

    tags_input_general = {
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

    emp_rut = forms.CharField(label="Rut Empresa", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_nombrerepresentante = forms.CharField(label="Nombre del Representante", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_rutrepresentante = forms.CharField(label="Rut del Representante", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_isestatal = forms.ChoiceField(initial='S', label='Es Estatal?', choices=Empresa.OPCIONES,
                                      widget=forms.Select(attrs=tags_input_general), required=False)
    emp_razonsocial = forms.CharField(label="Razón Social", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_giro = forms.CharField(label="Giro", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_direccion = forms.CharField(label="Dirección", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_numero = forms.IntegerField(label="Número", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_piso = forms.CharField(label="Piso", widget=forms.TextInput(
        attrs=tags_input_general), required=False)
    emp_dptooficina = forms.CharField(label="Departamento", widget=forms.TextInput(
        attrs=tags_input_general), required=False)
    pais = forms.ModelChoiceField(label="País", required=True,
                                  queryset=Pais.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    region = forms.ModelChoiceField(label="Región", required=True,
                                    queryset=Region.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    comuna = forms.ModelChoiceField(label="Comuna", required=True,
                                    queryset=Comuna.objects.all(), widget=forms.Select(attrs=tags_input_select2 ))
    emp_cospostal = forms.CharField(label="Código Postal", widget=forms.TextInput(
        attrs=tags_input_general), required=False)
    emp_fonouno = forms.CharField(label="Teléfono Principal", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_mailuno = forms.CharField(label="Correo Principal", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_fonodos = forms.CharField(label="Teléfono Secundario", widget=forms.TextInput(
        attrs=tags_input_general), required=False)
    emp_maildos = forms.CharField(label="Correo Secundario", widget=forms.TextInput(
        attrs=tags_input_general), required=False)
    emp_fechaingreso = forms.DateField(input_formats=["%d-%m-%Y"], label="Fecha de ingreso",
                                    widget=forms.DateInput(format="%d-%m-%Y",
                                                           attrs=tags_input_date), required=True)
    emp_isholding = forms.ChoiceField(initial='N', label="Es Holding?", choices=Empresa.OPCIONES,
                                      widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    emp_activa = forms.ChoiceField(initial='S', label='Empresa Activa?', choices=Empresa.OPCIONES,
                                      widget=forms.Select(attrs=tags_input_general), required=False)
    emp_rutcontador = forms.CharField(label="Rut del Contador", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_nombrecontador = forms.CharField(label="Nombre del Contador", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    emp_imagenempresa  = forms.ImageField(label="Logo Empresa", widget=forms.FileInput(
        attrs=tags_input_file), required=False)


    def clean_emp_rutrepresentante(self):
        data = self.cleaned_data["emp_rutrepresentante"]

        if not validarRut(data):
            self.add_error('emp_rutrepresentante', "El rut no es valido")
        return data

    def clean_emp_rutcontador(self):
        data = self.cleaned_data["emp_rutcontador"]

        if not validarRut(data):
            self.add_error('emp_rutcontador', "El rut no es valido")
        return data

    class Meta:
        model = Empresa
        fields = (
            "emp_rut"
            , "emp_nombrerepresentante"
            , "emp_rutrepresentante"
            , "emp_isestatal"
            , "emp_razonsocial"
            , "emp_giro"
            , "emp_direccion"
            , "emp_numero"
            , "emp_piso"
            , "emp_dptooficina"
            , "pais"
            , "region"
            , "comuna"
            , "emp_cospostal"
            , "emp_fonouno"
            , "emp_mailuno"
            , "emp_fonodos"
            , "emp_maildos"
            , "emp_fechaingreso"
            , "emp_isholding"
            , "emp_activa"
            , "emp_rutcontador"
            , "emp_nombrecontador"
            , "emp_imagenempresa"
        )

class AssociatedEntitiesForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
    }

    mutualSecurity = forms.ModelChoiceField(label="Mutual", required=True,
                                  queryset=MutualSecurity.objects.filter(ms_active="S"), widget=forms.Select(attrs=tags_input_general))
    cajasCompensacion = forms.ModelChoiceField(label="Caja Compensación", required=True,
                                    queryset=CajasCompensacion.objects.filter(cc_activo="S"), widget=forms.Select(attrs=tags_input_general))

    class Meta:
        model = Empresa
        fields = (
            "mutualSecurity"
            , "cajasCompensacion"
        )