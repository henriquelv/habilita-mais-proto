from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.accounts.decorators import aluno_required
from apps.agendamentos.models import Agendamento
from apps.avaliacoes.models import ResultadoAvaliacao

from .dashboard_views import ensure_initial_student_data


@login_required(login_url="/login/")
@aluno_required
def historico_view(request):
    ensure_initial_student_data(request.user)
    aulas_concluidas = Agendamento.objects.filter(
        aluno=request.user,
        ativo=True,
        tipo=Agendamento.TipoAula.PRATICA,
        status=Agendamento.Status.CONCLUIDO,
    ).order_by("-data")
    aulas_canceladas = Agendamento.objects.filter(
        aluno=request.user,
        tipo=Agendamento.TipoAula.PRATICA,
        status=Agendamento.Status.CANCELADO,
    ).order_by("-data")
    total = aulas_concluidas.count() + aulas_canceladas.count()
    taxa_conclusao = round((aulas_concluidas.count() / total) * 100) if total else 0

    resultados_por_instrutor = {
        resultado.avaliacao.instrutor: resultado
        for resultado in ResultadoAvaliacao.objects.filter(aluno=request.user, ativo=True).select_related("avaliacao")
    }

    return render(
        request,
        "progresso/historico.html",
        {
            "aulas_concluidas": aulas_concluidas,
            "aulas_canceladas": aulas_canceladas,
            "taxa_conclusao": taxa_conclusao,
            "resultados_por_instrutor": resultados_por_instrutor,
        },
    )
