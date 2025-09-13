from django import forms
from .models import Personagem, Episodio

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


class EpisodioForm(forms.ModelForm):
    class Meta:
        model = Episodio
        fields = ['titulo', 'data_exibicao', 'personagens']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'data_exibicao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'personagens': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }