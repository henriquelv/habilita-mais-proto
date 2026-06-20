from django.contrib.auth.models import User
from django.db import models


class Agendamento(models.Model):
    class TipoAula(models.TextChoices):
        TEORICA = "teorica", "Teórica"
        PRATICA = "pratica", "Prática"
        EXAME = "exame", "Exame"

    class Status(models.TextChoices):
        AGENDADO = "agendado", "Agendado"
        CONCLUIDO = "concluido", "Concluído"
        CANCELADO = "cancelado", "Cancelado"

    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agendamentos")
    tipo = models.CharField(max_length=20, choices=TipoAula.choices)
    data = models.DateField()
    horario = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AGENDADO,
    )
    observacao = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, default="B")
    instrutor = models.CharField(max_length=120, blank=True)
    local = models.CharField(max_length=160, blank=True)
    avaliado = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["data", "horario"]
        verbose_name = "agendamento"
        verbose_name_plural = "agendamentos"

    def __str__(self):
        return f"{self.aluno.username} - {self.tipo} em {self.data}"
