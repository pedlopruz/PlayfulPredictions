from django import forms
from .models import PartidosPredichos

LIGA_CHOICES = (
    ('LaLiga EA Sports', 'LaLiga EA Sports'),
    ('LaLiga Hypermotion', 'LaLiga Hypermotion'),
)
WINNER_CHOICES = (
    ('', 'None'),
    ('X', 'X'),
    ('2', '2'),
    ('1', '1'),
)
WINNER_PORRA_CHOICES = (
    ('X', 'X'),
    ('2', '2'),
    ('1', '1'),
)
class formulario_prediccion(forms.Form):
    liga = forms.ChoiceField(choices=LIGA_CHOICES,required=False)
    jornada = forms.IntegerField(required=False, min_value=6)
    local = forms.ChoiceField(label="Seleccione un equipo local", choices=[], required=False)
    visitante = forms.ChoiceField(label="Seleccione un equipo visitante", choices=[], required=False)
    winner = forms.ChoiceField(choices=WINNER_CHOICES,required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        equipos_locales = PartidosPredichos.objects.values_list('equipo_local', flat=True).distinct()

        # Agregar la opción "None" al principio de la lista de opciones
        choices = [("", "Sin Elegir")]
        choices += [(equipo_local, equipo_local) for equipo_local in equipos_locales]

        self.fields['local'].choices = choices
        self.fields['visitante'].choices = choices

class formulario_equipos(forms.Form):
    local = forms.ChoiceField(label="Seleccione un equipo local", choices=[])
    visitante = forms.ChoiceField(label="Seleccione un equipo visitante", choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        equipos_locales = PartidosPredichos.objects.values_list('equipo_local', flat=True).distinct()
        self.fields['local'].choices = [(equipo_local, equipo_local) for equipo_local in equipos_locales]
        self.fields['visitante'].choices = [(equipo_local, equipo_local) for equipo_local in equipos_locales]

class formulario_quiniela(forms.Form):
    partido1 = forms.ModelChoiceField(label="Seleccione el primer partido de la LaLiga EA Sport:", queryset=PartidosPredichos.objects.filter(liga = "LaLiga EA Sports"))
    partido2 = forms.ModelChoiceField(label="Seleccione el segundo partido LaLiga EA Sport:", queryset=PartidosPredichos.objects.filter(liga = "LaLiga EA Sports"))
    partido3 = forms.ModelChoiceField(label="Seleccione el tercer partido LaLiga EA Sport:", queryset=PartidosPredichos.objects.filter(liga = "LaLiga EA Sports"))
    partido4 = forms.ModelChoiceField(label="Seleccione el cuarto partido LaLiga EA Sport:", queryset=PartidosPredichos.objects.filter(liga = "LaLiga EA Sports"))
    partido5 = forms.ModelChoiceField(label="Seleccione el quinto partido LaLiga EA Sport:", queryset=PartidosPredichos.objects.filter(liga = "LaLiga EA Sports"))
    partido6 = forms.ModelChoiceField(label="Seleccione el primer partido LaLiga Hypermotion:", queryset=PartidosPredichos.objects.filter(liga = "LaLiga Hypermotion"))
    partido7 = forms.ModelChoiceField(label="Seleccione el segundo partido LaLiga Hypermotion:", queryset=PartidosPredichos.objects.filter(liga = "LaLiga Hypermotion"))
    partido8 = forms.ModelChoiceField(label="Seleccione el tercer partido LaLiga Hypermotion:", queryset=PartidosPredichos.objects.filter(liga = "LaLiga Hypermotion"))
    partido9 = forms.ModelChoiceField(label="Seleccione el cuarto partido LaLiga Hypermotion:", queryset=PartidosPredichos.objects.filter(liga = "LaLiga Hypermotion"))
    partido10 = forms.ModelChoiceField(label="Seleccione el quinto partido LaLiga Hypermotion:", queryset=PartidosPredichos.objects.filter(liga = "LaLiga Hypermotion"))

class formulario_porra(forms.Form):
    partido1 = forms.ChoiceField(choices=WINNER_PORRA_CHOICES,required=True)
    partido2 = forms.ChoiceField(choices=WINNER_PORRA_CHOICES,required=True)
    partido3 = forms.ChoiceField(choices=WINNER_PORRA_CHOICES,required=True)
    partido4 = forms.ChoiceField(choices=WINNER_PORRA_CHOICES,required=True)
    partido5 = forms.ChoiceField(choices=WINNER_PORRA_CHOICES,required=True)
    partido6 = forms.ChoiceField(choices=WINNER_PORRA_CHOICES,required=True)
    partido7 = forms.ChoiceField(choices=WINNER_PORRA_CHOICES,required=True)
    partido8 = forms.ChoiceField(choices=WINNER_PORRA_CHOICES,required=True)
    partido9 = forms.ChoiceField(choices=WINNER_PORRA_CHOICES,required=True)
    partido10 = forms.ChoiceField(choices=WINNER_PORRA_CHOICES,required=True)

