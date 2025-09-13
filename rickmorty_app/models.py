from django.db import models

class Episodio(models.Model):
    api_id = models.IntegerField(unique=True)
    nome = models.CharField(max_length=200, blank=True, null=True)
    data_exibicao = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    personagens = models.ManyToManyField('Personagem', related_name='episodios')

    def __str__(self):
        return f"{self.codigo} - {self.nome}" if self.codigo and self.nome else f"Episódio ID: {self.api_id}"

class Personagem(models.Model):
    api_id = models.IntegerField(unique=True)
    nome = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    especie = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    imagem = models.URLField()

    def __str__(self):
        return self.nome