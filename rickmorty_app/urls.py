from django.urls import path
from . import views

urlpatterns = [
    path('personagens/', views.listar_personagens, name='listar_personagens'),
    path('importar/', views.importar_personagens, name='importar_personagens'),
    path('personagens/novo/', views.criar_personagem, name='criar_personagem'),
    path('personagens/editar/<int:api_id>/', views.editar_personagem, name='editar_personagem'),
    path('personagens/deletar/<int:api_id>/', views.deletar_personagem, name='deletar_personagem'),
]
