from django.db import models

class Personagem(models.Model):
    api_id = models.IntegerField(unique=True)
    nome = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    especie = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    imagem = models.URLField()

    def __str__(self):
        return self.nome


