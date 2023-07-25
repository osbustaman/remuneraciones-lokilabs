from django import forms

from applications.base.models import Comuna, Pais, Region
from applications.base.utils import validarRut
from applications.empresa.models import Afp, Apv, Banco, CajasCompensacion, MutualSecurity, Salud
from applications.remuneracion.models import Concept


class BanksForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
    }

    ban_nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    ban_codigo = forms.CharField(label="Código", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    ban_activo = forms.ChoiceField(initial='S', label='Banco Activo?', choices=Banco.OPCIONES,
                                   widget=forms.Select(attrs=tags_input_general), required=False)

    class Meta:
        model = Banco
        fields = (
            "ban_nombre", "ban_codigo", "ban_activo"
        )


class CountryForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
    }

    tags_input_readonly = {
        'class': 'form-control',
        'readonly': 'readonly'
    }

    pa_nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_readonly), required=True)
    pa_codigo = forms.IntegerField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_readonly), required=True)

    class Meta:
        model = Pais
        fields = (
            "pa_nombre", "pa_codigo"
        )


class RegionForm(forms.ModelForm):

    tags_input_readonly = {
        'class': 'form-control',
        'readonly': 'readonly'
    }

    tags_input_select2_readonly = {
        'class': 'form-control select2-show-search',
        'readonly': 'readonly'
    }

    re_nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_readonly), required=True)
    pais = forms.ModelChoiceField(label="País", required=True,
                                  queryset=Pais.objects.all(), widget=forms.Select(attrs=tags_input_select2_readonly))
    re_numeroregion = forms.CharField(label="Sigla", widget=forms.TextInput(
        attrs=tags_input_readonly), required=False)
    re_numero = forms.IntegerField(label="N° región", widget=forms.TextInput(
        attrs=tags_input_readonly), required=True)

    class Meta:
        model = Region
        fields = (
            "re_nombre", "pais", "re_numeroregion", "re_numero"
        )


class CommuneForm(forms.ModelForm):

    tags_input_readonly = {
        'class': 'form-control',
        'readonly': 'readonly'
    }

    tags_input_select2_readonly = {
        'class': 'form-control select2-show-search',
        'readonly': 'readonly'
    }

    com_nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_readonly), required=True)
    com_numero = forms.IntegerField(label="N° comuna", widget=forms.TextInput(
        attrs=tags_input_readonly), required=True)
    region = forms.ModelChoiceField(label="Región", required=True,
                                    queryset=Region.objects.all(), widget=forms.Select(attrs=tags_input_select2_readonly))

    class Meta:
        model = Comuna
        fields = (
            "com_nombre", "com_numero", "region"
        )


class AfpForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
    }

    afp_codigoprevired = forms.CharField(label="Código Previred", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    afp_nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    afp_tasatrabajadordependiente = forms.FloatField(label="Tasa trabajador Dependiente", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    afp_sis = forms.FloatField(label="Seguro de Invalidez y Sobrevivencia (SIS)", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    afp_tasatrabajadorindependiente = forms.FloatField(label="Tasa trabajador independiente", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    afp_activo = forms.ChoiceField(initial='S', label='Afp Activa?', choices=Afp.OPCIONES,
                                   widget=forms.Select(attrs=tags_input_general), required=False)

    class Meta:
        model = Afp
        fields = (
            "afp_codigoprevired", "afp_nombre", "afp_tasatrabajadordependiente", "afp_sis", "afp_tasatrabajadorindependiente", "afp_activo"
        )


class ApvForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
    }

    apv_codigoprevired = forms.CharField(label="Código Previred", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    apv_nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    apv_nombrerazonsocial = forms.CharField(label="Razón Social", widget=forms.TextInput(
        attrs=tags_input_general), required=True)

    class Meta:
        model = Apv
        fields = (
            "apv_codigoprevired", "apv_nombre", "apv_nombrerazonsocial"
        )


class SaludForm(forms.ModelForm):

    tags_input_readonly = {
        'class': 'form-control',
        'readonly': 'readonly'
    }

    tags_input_general = {
        'class': 'form-control',
    }

    sa_nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    sa_codigo = forms.CharField(label="Código", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    sa_tipo = forms.ChoiceField(initial='F', label="Tipo Entidad?", choices=Salud.TIPO,
                                widget=forms.Select(attrs=tags_input_general), required=True)
    sa_activo = forms.ChoiceField(initial='S', label='Entidad de Salud Activa?', choices=Salud.OPCIONES,
                                  widget=forms.Select(attrs=tags_input_general), required=False)

    class Meta:
        model = Salud
        fields = (
            "sa_nombre", "sa_codigo", "sa_tipo", "sa_activo"
        )


class CajasCompensacionForm(forms.ModelForm):

    tags_input_readonly = {
        'class': 'form-control',
        'readonly': 'readonly'
    }

    tags_input_general = {
        'class': 'form-control',
    }

    cc_nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    cc_codigo = forms.CharField(label="Código", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    cc_rut = forms.CharField(label="Rut", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    cc_activo = forms.ChoiceField(initial='S', label='Caja de Compensacion Activa?', choices=CajasCompensacion.OPCIONES,
                                  widget=forms.Select(attrs=tags_input_general), required=False)

    def clean_cc_rut(self):
        data = self.cleaned_data["cc_rut"]

        if not validarRut(data):
            self.add_error('cc_rut', "El rut no es valido")
        return data

    class Meta:
        model = CajasCompensacion
        fields = (
            "cc_nombre", "cc_codigo", "cc_rut", "cc_activo"
        )


class MutualSecurityForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
    }
    
    ms_name = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    ms_rut = forms.CharField(label="Rut", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    ms_codeprevired = forms.CharField(label="Código", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    ms_active = forms.ChoiceField(initial='S', label='Activa?', choices=MutualSecurity.OPTIONS,
                                  widget=forms.Select(attrs=tags_input_general), required=False)
    
    def clean_ms_rut(self):
        data = self.cleaned_data["ms_rut"]

        if not validarRut(data):
            self.add_error('ms_rut', "El rut no es valido")
        return data

    class Meta:
        model = MutualSecurity
        fields = (
            "ms_name", "ms_rut", "ms_codeprevired", "ms_active"
        )


class ConceptsForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
    }

    conc_name = forms.CharField(label="Nombre Concepto", widget=forms.TextInput(
        attrs=tags_input_general), required=True)
    conc_typeconcept = forms.ChoiceField(label='Tipo Concepto', choices=Concept.TYPE,
                                  widget=forms.Select(attrs=tags_input_general), required=True)
    conc_description = forms.CharField(label="Descripción", help_text="150 caracteres máximos", widget=forms.TextInput(
        attrs=tags_input_general), required=False)
    
    def clean_conc_description(self):
        data = self.cleaned_data["conc_description"]

        if len(data) > 150:
            self.add_error('conc_description', "No puede ecribir mas de 150 caracteres")
        return data

    class Meta:
        model = Concept
        fields = (
            "conc_name", "conc_typeconcept", "conc_description"
        )