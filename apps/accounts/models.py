from django.contrib.auth.models import User
from django.db import models


class PerfilAluno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    cpf = models.CharField(max_length=14, unique=True, blank=True, default="")
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    categoria_cnh = models.CharField(max_length=5, default="B")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "perfil de aluno"
        verbose_name_plural = "perfis de alunos"

    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"
