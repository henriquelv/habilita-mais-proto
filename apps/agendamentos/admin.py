from django.contrib import admin

from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "tipo", "categoria", "data", "horario", "status", "ativo")
    list_filter = ("tipo", "status", "ativo", "data")
    search_fields = ("aluno__username", "instrutor", "local")
