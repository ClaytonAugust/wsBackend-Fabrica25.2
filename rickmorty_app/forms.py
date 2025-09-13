from django import forms
from .models import Personagem, Episodio

class PersonagemForm(forms.ModelForm):
    # Adicionando o campo de episódios para seleção
    episodios = forms.ModelMultipleChoiceField(
        queryset=Episodio.objects.all().order_by('nome'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Personagem
        fields = ['nome', 'status', 'especie', 'genero', 'imagem', 'episodios']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.TextInput(attrs={'class': 'form-control'}),
            'imagem': forms.URLInput(attrs={'class': 'form-control'}),
        }