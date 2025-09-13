from django import forms
from .models import Personagem

class PersonagemForm(forms.ModelForm):
    class Meta:
        model = Personagem
        fields = ['nome', 'status', 'especie', 'genero', 'imagem']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.TextInput(attrs={'class': 'form-control'}),
            'imagem': forms.URLInput(attrs={'class': 'form-control'}),
        }