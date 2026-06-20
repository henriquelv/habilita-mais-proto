from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class PerfilAluno(models.Model):
    class TipoUsuario(models.TextChoices):
        ALUNO = "aluno", "Aluno"
        INSTRUTOR = "instrutor", "Instrutor"
        ADMIN = "admin", "Admin"

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    cpf = models.CharField(max_length=14, blank=True, default="")
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    categoria_cnh = models.CharField(max_length=5, default="B")
    tipo_usuario = models.CharField(max_length=20, choices=TipoUsuario.choices, default=TipoUsuario.ALUNO)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "perfil de aluno"
        verbose_name_plural = "perfis de alunos"
        constraints = [
            models.UniqueConstraint(
                fields=["cpf"],
                condition=~Q(cpf=""),
                name="unique_non_empty_cpf",
            )
        ]

    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"
