import requests
from django.shortcuts import render, redirect
from .models import Personagem

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