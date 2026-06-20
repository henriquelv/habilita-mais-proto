from django.contrib.auth.models import User
from django.db import models


class ProgressoAluno(models.Model):
    aluno = models.OneToOneField(User, on_delete=models.CASCADE, related_name="progresso")
    aulas_teoricas_total = models.IntegerField(default=45)
    aulas_teoricas_concluidas = models.IntegerField(default=0)
    aulas_praticas_total = models.IntegerField(default=20)
    aulas_praticas_concluidas = models.IntegerField(default=0)
    exame_status = models.CharField(max_length=30, default="aguardando")
    ativo = models.BooleanField(default=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "progresso de aluno"
        verbose_name_plural = "progressos de alunos"

    @property
    def percentual_teoricas(self):
        if self.aulas_teoricas_total == 0:
            return 0
        return int((self.aulas_teoricas_concluidas / self.aulas_teoricas_total) * 100)

    @property
    def percentual_praticas(self):
        if self.aulas_praticas_total == 0:
            return 0
        return int((self.aulas_praticas_concluidas / self.aulas_praticas_total) * 100)

    @property
    def percentual_total(self):
        total = self.aulas_teoricas_total + self.aulas_praticas_total
        concluidas = self.aulas_teoricas_concluidas + self.aulas_praticas_concluidas
        return int((concluidas / total) * 100) if total else 0

    def __str__(self):
        return f"Progresso de {self.aluno}"


class Certificado(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificados")
    nome = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to="certificados/", blank=True, null=True)
    emitido_em = models.DateTimeField(auto_now_add=True)
    previsao = models.CharField(max_length=120, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["-emitido_em"]
        verbose_name = "certificado"
        verbose_name_plural = "certificados"

    def __str__(self):
        return f"{self.nome} - {self.aluno.username}"
