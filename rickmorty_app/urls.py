from django.urls import path
from . import views

urlpatterns = [
    path('personagens/', views.listar_personagens, name='listar_personagens'),
    path('importar/', views.importar_personagens, name='importar_personagens'),
]
