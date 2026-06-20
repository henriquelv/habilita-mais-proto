from django.contrib.auth.models import User
from django.db import models


class Pagamento(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        PAGO = "pago", "Pago"
        VENCIDO = "vencido", "Vencido"

    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pagamentos")
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )
    comprovante = models.FileField(upload_to="comprovantes/", blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["vencimento"]
        verbose_name = "pagamento"
        verbose_name_plural = "pagamentos"

    def __str__(self):
        return f"{self.descricao} - {self.aluno.username} ({self.status})"
