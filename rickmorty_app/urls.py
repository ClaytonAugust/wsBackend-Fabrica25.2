from django.urls import path
from . import views

urlpatterns = [
    path('personagens/', views.listar_personagens, name='listar_personagens'),
    path('episodios/', views.listar_episodios, name='listar_episodios'),
    path('importar/personagens/otimizado/', views.importar_personagens_otimizado,
         name='importar_personagens_otimizado'),
    
    path('personagens/novo/', views.criar_personagem, name='criar_personagem'),
    path('personagens/editar/<int:api_id>/', views.editar_personagem, name='editar_personagem'),
    path('personagens/deletar/<int:api_id>/', views.deletar_personagem, name='deletar_personagem'),
]