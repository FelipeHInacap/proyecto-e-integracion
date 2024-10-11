from django import forms
from .models import Usuario

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']  # Ajusta los campos según tu modelo
