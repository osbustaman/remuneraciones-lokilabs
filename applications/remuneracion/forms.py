from django import forms

from applications.empresa.models import Afp, Salud


class SalaryCalculatorForm(forms.Form):

    tags_input_general = {
        'class': 'form-control',
    }

    _HAS_LEGAL_GRATIFICATION = (
        (1, 'SI'),
        (2, 'NO'),
    )

    TYPE_GRATIFICATION = (
        (0, ' ---------- '),
        (1, 'MENSUAL'),
        (2, 'ANUAL'),
    )

    TYPE_WORKER = (
        (1, 'DEPENDIENTE'),
        (2, 'INDEPENDIENTE'),
    )


    base_salary= forms.CharField(label="Sueldo base", widget=forms.NumberInput(
        attrs=tags_input_general), required=True)
    
    has_legal_gratification = forms.ChoiceField(initial=1, label='Tiene gratificación legal?', choices=_HAS_LEGAL_GRATIFICATION,
                                    widget=forms.Select(attrs=tags_input_general), required=True)
    
    type_of_gratification = forms.ChoiceField(initial=0, label='Tipo de gratificación', choices=TYPE_GRATIFICATION,
                                    widget=forms.Select(attrs=tags_input_general), required=False)
    
    type_of_work = forms.ChoiceField(initial=1, label='Tipo de trabajador', choices=TYPE_WORKER,
                                    widget=forms.Select(attrs=tags_input_general), required=True)
    
    afp = forms.ModelChoiceField(label="AFPs", required=True,
                                queryset=Afp.objects.filter(afp_activo="S"), widget=forms.Select(attrs=tags_input_general))
    
    salud = forms.ModelChoiceField(label="Salud", required=True,
                                queryset=Salud.objects.filter(sa_activo="S"), widget=forms.Select(attrs=tags_input_general))
    
    quantity_uf_health = forms.CharField(label="UF", widget=forms.TextInput(
        attrs=tags_input_general), required=False)

