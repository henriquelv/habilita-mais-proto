from django.contrib import admin

from .models import Avaliacao, ResultadoAvaliacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "instrutor", "ativo", "criado_em")
    list_filter = ("ativo", "criado_em")
    search_fields = ("titulo", "instrutor")


@admin.register(ResultadoAvaliacao)
class ResultadoAvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "avaliacao", "nota", "aprovado", "ativo", "data_realizacao")
    list_filter = ("aprovado", "ativo", "data_realizacao")
    search_fields = ("aluno__username", "avaliacao__titulo", "avaliacao__instrutor")
