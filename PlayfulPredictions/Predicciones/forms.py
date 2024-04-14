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
