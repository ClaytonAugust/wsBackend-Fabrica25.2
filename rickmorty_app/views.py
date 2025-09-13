import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Personagem
from .forms import PersonagemForm
from django.db import models

# func para importar personagens da API
def importar_personagens(request):
    url = "https://rickandmortyapi.com/api/character"
    response = requests.get(url)

    if response.status_code == 200:
        personagens_dados = response.json()
        for item in personagens_dados['results']:
            # cria ou atualiza o personagem no banco de dados
            Personagem.objects.update_or_create(
                api_id=item['id'],
                defaults={
                    'nome': item['name'],
                    'status': item['status'],
                    'especie': item['species'],
                    'genero': item['gender'],
                    'imagem': item['image']
                }
            )

    return redirect('listar_personagens')

# listagem de personagens
def listar_personagens(request):
    personagens = Personagem.objects.all()
    return render(request, 'listar_personagens.html', {'personagens': personagens})

# criar novo personagem manualmente
def criar_personagem(request):
    if request.method == "POST":
        form = PersonagemForm(request.POST)
        if form.is_valid():
            personagem = form.save(commit=False)
            # caso não tenha api_id, atribui um novo id único
            if not personagem.api_id:
                ultimo = Personagem.objects.aggregate(models.Max("api_id"))["api_id__max"] or 0
                personagem.api_id = ultimo + 1
            personagem.save()
            return redirect('listar_personagens')
    else:
        form = PersonagemForm()
    return render(request, 'criar_personagem.html', {'form': form})

# editar personagem
def editar_personagem(request, api_id):
    personagem = get_object_or_404(Personagem, api_id=api_id)
    if request.method == "POST":
        form = PersonagemForm(request.POST, instance=personagem)
        if form.is_valid():
            form.save()
            return redirect('listar_personagens')
    else:
        form = PersonagemForm(instance=personagem)
    return render(request, 'editar_personagem.html', {'form': form, 'personagem': personagem})

# deletar personagem
def deletar_personagem(request, api_id):
    personagem = get_object_or_404(Personagem, api_id=api_id)
    if request.method == "POST":
        personagem.delete()
        return redirect('listar_personagens')
    return render(request, 'deletar_personagem.html', {'personagem': personagem})