import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Personagem, Episodio
from .forms import PersonagemForm
from django.db import models, transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages 
def importar_personagens_otimizado(request):
    """
    Importa personagens e seus episódios relacionados de forma otimizada, 
    buscando a próxima página que ainda não foi totalmente importada.
    """
    # Descobre qual a última página importada para continuar de onde parou
    personagens_count = Personagem.objects.count()
    page = (personagens_count // 20) + 1 # 20 é o número de itens por página na API

    url = f"https://rickandmortyapi.com/api/character?page={page}"
    
    try:
        response = requests.get(url, timeout=10) # Timeout para evitar travamentos
        if response.status_code == 404:
            messages.info(request, "Todos os personagens já foram importados da API.")
            return redirect("listar_personagens")
        response.raise_for_status() # Lança um erro para outros status HTTP ruins (500, etc)
        data = response.json()
        personagens_dados = data['results']
    except requests.RequestException as e:
        messages.error(request, f"Erro ao acessar a API: {e}")
        return redirect("listar_personagens")

    # coletar ids de episodios
    todos_ep_ids = set()
    for item in personagens_dados:
        # Extrai o ID de cada URL de episodios
        ep_ids = [int(ep_url.split("/")[-1]) for ep_url in item['episode']]
        todos_ep_ids.update(ep_ids)

    # busca de epsodios de uma vez
    if todos_ep_ids:
        ids_string = ",".join(map(str, todos_ep_ids))
        ep_url = f"https://rickandmortyapi.com/api/episode/{ids_string}"
        try:
            ep_response = requests.get(ep_url, timeout=10)
            ep_response.raise_for_status()
            episodios_api_data = ep_response.json()
            # A API retorna um único objeto se for um só ID, e uma lista se forem vários
            if not isinstance(episodios_api_data, list):
                episodios_api_data = [episodios_api_data]
        except requests.RequestException as e:
            messages.error(request, f"Erro ao buscar episódios da API: {e}")
            return redirect("listar_personagens")

        # mapeia episodios por id usando metodo map
        episodios_map = {ep['id']: ep for ep in episodios_api_data}
    else:
        episodios_map = {}

    # salva no banco de dados de forma otimizada
    try:
        with transaction.atomic(): # Garante que tudo seja salvo ou nada seja salvo em caso de erro(meio paia isso)
            # Salva/Atualiza os eps
            episodios_no_db = {}
            for ep_id, ep_data in episodios_map.items():
                episodio_obj, _ = Episodio.objects.update_or_create(
                    api_id=ep_id,
                    defaults={
                        'nome': ep_data['name'],
                        'data_exibicao': ep_data['air_date'],
                        'codigo': ep_data['episode'],
                    }
                )
                episodios_no_db[ep_id] = episodio_obj

            # Salva/Atualiza os personagens e sua relação com os eps
            for item in personagens_dados:
                personagem_obj, _ = Personagem.objects.update_or_create(
                    api_id=item['id'],
                    defaults={
                        'nome': item['name'],
                        'status': item['status'],
                        'especie': item['species'],
                        'genero': item['gender'],
                        'imagem': item['image'],
                    }
                )
                
                # Pega os IDs dos episódios deste personagem
                ep_ids_do_personagem = [int(ep_url.split("/")[-1]) for ep_url in item['episode']]
                # Pega os objetos Episodio correspondentes que já salvamos
                episodios_para_adicionar = [episodios_no_db[ep_id] for ep_id in ep_ids_do_personagem if ep_id in episodios_no_db]
                # Usa .set() para sincronizar as relações de forma eficiente
                personagem_obj.episodios.set(episodios_para_adicionar)

    except Exception as e:
        messages.error(request, f"Erro ao salvar os dados no banco: {e}")
        return redirect("listar_personagens")

    messages.success(request, f"Página {page} de personagens importada com sucesso!")
    return redirect("listar_personagens")

# listar personagens
def listar_personagens(request):
    """
    Lista os personagens salvos no BANCO DE DADOS LOCAL com paginação e busca.
    """
    query = request.GET.get('q')
    personagens_list = Personagem.objects.prefetch_related('episodios').order_by('nome')

    if query:
        personagens_list = personagens_list.filter(nome__icontains=query)

    paginator = Paginator(personagens_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query or ""
    }
    return render(request, "listar_personagens.html", context)

# crud de personagens e episodios
# listar episodios
def listar_episodios(request):
    query = request.GET.get('q')
    episodios_list = Episodio.objects.prefetch_related('personagens').order_by('api_id')
    if query:
        episodios_list = episodios_list.filter(
            models.Q(nome__icontains=query) | models.Q(codigo__icontains=query)
        )
    paginator = Paginator(episodios_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "query": query or ""
    }
    return render(request, "listar_episodios.html", context)

# criar personagem
def criar_personagem(request):
    if request.method == "POST":
        form = PersonagemForm(request.POST)
        if form.is_valid():
            personagem = form.save(commit=False)
            if not personagem.api_id:
                ultimo = Personagem.objects.aggregate(models.Max("api_id"))["api_id__max"] or 0
                personagem.api_id = ultimo + 1
            personagem.save()
            form.save_m2m() 
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