from django.contrib import admin

from .models import Certificado, ProgressoAluno


@admin.register(ProgressoAluno)
class ProgressoAlunoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "aulas_teoricas_concluidas", "aulas_praticas_concluidas", "exame_status", "ativo")
    list_filter = ("ativo", "exame_status")
    search_fields = ("aluno__username",)


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ("nome", "aluno", "ativo", "emitido_em")
    list_filter = ("ativo", "emitido_em")
    search_fields = ("nome", "aluno__username")
