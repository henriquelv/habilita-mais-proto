from django.contrib import admin

from .models import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ("descricao", "aluno", "valor", "vencimento", "status", "ativo")
    list_filter = ("status", "ativo", "vencimento")
    search_fields = ("descricao", "aluno__username")
