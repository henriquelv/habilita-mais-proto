from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import aluno_required

from ..forms import AgendamentoForm
from ..models import Agendamento


def _time_to_minutes(value):
    if isinstance(value, str):
        parsed = datetime.strptime(value, "%H:%M").time()
    else:
        parsed = value
    return parsed.hour * 60 + parsed.minute


def _validar_regras_agendamento(request, agendamento):
    qs = Agendamento.objects.filter(aluno=request.user, ativo=True)
    if agendamento.tipo != Agendamento.TipoAula.PRATICA:
        return True

    total_praticas = qs.filter(tipo=Agendamento.TipoAula.PRATICA).exclude(status=Agendamento.Status.CANCELADO).count()
    if total_praticas >= 20:
        messages.error(request, "Limite máximo de 20 agendamentos simultâneos atingido.")
        return False

    aulas_no_dia = qs.filter(
        tipo=Agendamento.TipoAula.PRATICA,
        data=agendamento.data,
    ).exclude(status=Agendamento.Status.CANCELADO)
    if aulas_no_dia.count() >= 2:
        messages.error(request, "Você já atingiu o limite de 2 aulas por dia.")
        return False

    inicio_semana = agendamento.data - timedelta(days=agendamento.data.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    semana_categoria = qs.filter(
        tipo=Agendamento.TipoAula.PRATICA,
        categoria=agendamento.categoria,
        data__range=(inicio_semana, fim_semana),
    ).exclude(status=Agendamento.Status.CANCELADO)
    if semana_categoria.count() >= 3:
        messages.error(request, f"Limite de 3 aulas da categoria {agendamento.categoria} nesta semana atingido.")
        return False

    novo_horario = _time_to_minutes(agendamento.horario)
    for aula in aulas_no_dia:
        diff = abs(novo_horario - _time_to_minutes(aula.horario))
        if aula.categoria == agendamento.categoria and diff < 50:
            messages.error(request, "Esta aula se sobrepõe a uma aula já agendada.")
            return False
        if aula.categoria != agendamento.categoria and diff < 80:
            messages.error(request, "Para categorias diferentes, é necessário 30 minutos de intervalo.")
            return False
    return True


@login_required(login_url="/login/")
@aluno_required
def agendamento_view(request):
    form = AgendamentoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        agendamento = form.save(commit=False)
        agendamento.aluno = request.user
        agendamento.status = Agendamento.Status.AGENDADO
        if _validar_regras_agendamento(request, agendamento):
            agendamento.save()
            messages.success(request, "Agendamento confirmado com sucesso!")
            return redirect("meus_agendamentos")

    materiais = [
        ("Legislação de Trânsito", "Código de Trânsito Brasileiro completo", "2.5 MB"),
        ("Direção Defensiva", "Manual de direção defensiva", "1.8 MB"),
        ("Primeiros Socorros", "Guia de primeiros socorros no trânsito", "1.2 MB"),
        ("Mecânica Básica", "Conhecimentos básicos de mecânica", "3.1 MB"),
        ("Meio Ambiente", "Educação ambiental e trânsito", "900 KB"),
    ]
    return render(request, "agendamentos/agendamento.html", {"form": form, "materiais": materiais})


@login_required(login_url="/login/")
@aluno_required
def meus_agendamentos_view(request):
    agendamentos_base = Agendamento.objects.filter(aluno=request.user)
    status = request.GET.get("status", "").strip()
    tipo = request.GET.get("tipo", "").strip()
    data = request.GET.get("data", "").strip()

    agendamentos_filtrados = agendamentos_base
    if status:
        agendamentos_filtrados = agendamentos_filtrados.filter(status=status)
    else:
        agendamentos_filtrados = agendamentos_filtrados.filter(ativo=True)
    if tipo:
        agendamentos_filtrados = agendamentos_filtrados.filter(tipo=tipo)
    if data:
        agendamentos_filtrados = agendamentos_filtrados.filter(data=data)

    agendamentos_ativos = agendamentos_base.filter(ativo=True)
    context = {
        "agendamentos": agendamentos_filtrados.order_by("data", "horario"),
        "confirmados": agendamentos_ativos.filter(status=Agendamento.Status.AGENDADO),
        "pendentes": agendamentos_ativos.filter(status=Agendamento.Status.AGENDADO),
        "total_praticas": agendamentos_ativos.filter(tipo=Agendamento.TipoAula.PRATICA).count(),
        "status_choices": Agendamento.Status.choices,
        "tipo_choices": Agendamento.TipoAula.choices,
        "filtros": {"status": status, "tipo": tipo, "data": data},
    }
    return render(request, "agendamentos/meus_agendamentos.html", context)


@login_required(login_url="/login/")
@aluno_required
def cancelar_agendamento_view(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk, aluno=request.user, ativo=True)
    if request.method == "POST":
        agendamento.status = Agendamento.Status.CANCELADO
        agendamento.ativo = False
        agendamento.save(update_fields=["status", "ativo"])
        messages.success(request, "Agendamento cancelado com sucesso!")
    return redirect("meus_agendamentos")
