from django.contrib import admin

from .models import PerfilAluno


@admin.register(PerfilAluno)
class PerfilAlunoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo_usuario", "cpf", "telefone", "categoria_cnh", "ativo", "criado_em")
    list_filter = ("ativo", "tipo_usuario", "categoria_cnh")
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name", "cpf")
