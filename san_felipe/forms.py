# tu_app/forms.py
from django import forms

class SugerenciaForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    sugerencia = forms.CharField(widget=forms.Textarea, required=True)

from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["nombre", "email", "telefono", "fecha", "hora", "mensaje"]