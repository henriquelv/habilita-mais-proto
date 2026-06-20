from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.accounts.decorators import aluno_required
from apps.progresso.models import Certificado, ProgressoAluno

from .dashboard_views import ensure_initial_student_data


@login_required(login_url="/login/")
@aluno_required
def certificados_view(request):
    progresso = ensure_initial_student_data(request.user)
    certificados = Certificado.objects.filter(aluno=request.user, ativo=True)
    pendentes = [
        {
            "nome": "Certificado de Aulas Práticas",
            "previsao": "Após concluir 20 aulas",
            "progresso": progresso.aulas_praticas_concluidas,
            "total": progresso.aulas_praticas_total,
            "percentual": progresso.percentual_praticas,
        },
        {
            "nome": "CNH Definitiva",
            "previsao": "Após aprovação no exame prático",
            "progresso": None,
            "total": None,
            "percentual": 0,
        },
    ]
    return render(
        request,
        "progresso/certificados.html",
        {"certificados": certificados, "pendentes": pendentes, "progresso": progresso},
    )
