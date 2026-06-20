from django.contrib.auth.models import User
from django.db import models


class Avaliacao(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    instrutor = models.CharField(max_length=120, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["titulo"]
        verbose_name = "avaliação"
        verbose_name_plural = "avaliações"

    def __str__(self):
        return self.titulo


class ResultadoAvaliacao(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resultados")
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    comentario = models.TextField(blank=True)
    aprovado = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    data_realizacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_realizacao"]
        verbose_name = "resultado de avaliação"
        verbose_name_plural = "resultados de avaliações"

    def __str__(self):
        return f"{self.aluno} - {self.avaliacao} - {self.nota}"
