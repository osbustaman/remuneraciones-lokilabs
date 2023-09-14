from django import forms

from applications.empresa.models import Afp, Salud


class SalaryCalculatorForm(forms.Form):

    tags_input_general = {
        'class': 'form-control',
    }

    TYPE_GRATIFICATION = (
        (1, 'MENSUAL'),
        (2, 'ANUAL'),
    )

    TYPE_WORKER = (
        (1, 'DEPENDIENTE'),
        (2, 'INDEPENDIENTE'),
    )


    desired_salary= forms.CharField(label="Sueldo líquido deseado", widget=forms.NumberInput(
        attrs=tags_input_general), required=True)
    
    type_of_gratification = forms.ChoiceField(initial=1, label='Tipo de gratificación', choices=TYPE_GRATIFICATION,
                                    widget=forms.Select(attrs=tags_input_general), required=False)
    
    type_of_work = forms.ChoiceField(initial=1, label='Tipo de trabajador', choices=TYPE_WORKER,
                                    widget=forms.Select(attrs=tags_input_general), required=False)
    
    afp = forms.ModelChoiceField(label="AFPs", required=True,
                                queryset=Afp.objects.filter(afp_activo="S"), widget=forms.Select(attrs=tags_input_general))
    
    salud = forms.ModelChoiceField(label="Salud", required=True,
                                queryset=Salud.objects.filter(sa_activo="S"), widget=forms.Select(attrs=tags_input_general))
    
    uf = forms.CharField(label="UF", widget=forms.TextInput(
        attrs=tags_input_general), required=False)

