from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.agendamentos.models import Agendamento
from apps.avaliacoes.models import Avaliacao, ResultadoAvaliacao
from apps.pagamentos.models import Pagamento
from apps.progresso.models import Certificado, ProgressoAluno


def ensure_initial_student_data(user):
    progresso, _ = ProgressoAluno.objects.get_or_create(
        aluno=user,
        defaults={
            "aulas_teoricas_concluidas": 45,
            "aulas_praticas_concluidas": 15,
            "exame_status": "aguardando",
        },
    )

    if not Agendamento.objects.filter(aluno=user).exists():
        Agendamento.objects.bulk_create(
            [
                Agendamento(
                    aluno=user,
                    tipo=Agendamento.TipoAula.PRATICA,
                    categoria="B",
                    data=date(2025, 11, 20),
                    horario="14:00",
                    instrutor="Carlos Silva",
                    status=Agendamento.Status.CONCLUIDO,
                    avaliado=False,
                ),
                Agendamento(
                    aluno=user,
                    tipo=Agendamento.TipoAula.PRATICA,
                    categoria="B",
                    data=date(2025, 11, 28),
                    horario="10:00",
                    instrutor="Maria Santos",
                    status=Agendamento.Status.AGENDADO,
                ),
                Agendamento(
                    aluno=user,
                    tipo=Agendamento.TipoAula.PRATICA,
                    categoria="B",
                    data=date(2025, 11, 30),
                    horario="15:00",
                    instrutor="João Pedro",
                    status=Agendamento.Status.AGENDADO,
                ),
            ]
        )

    if not Pagamento.objects.filter(aluno=user).exists():
        Pagamento.objects.bulk_create(
            [
                Pagamento(aluno=user, descricao="Matrícula", valor=Decimal("800.00"), vencimento=date(2024, 12, 10), status=Pagamento.Status.PAGO),
                Pagamento(aluno=user, descricao="Mensalidade Dezembro", valor=Decimal("450.00"), vencimento=date(2024, 12, 20), status=Pagamento.Status.PAGO),
                Pagamento(aluno=user, descricao="Taxa Exame Médico", valor=Decimal("200.00"), vencimento=date(2025, 1, 5), status=Pagamento.Status.PAGO),
                Pagamento(aluno=user, descricao="Mensalidade Janeiro", valor=Decimal("450.00"), vencimento=date(2025, 1, 20), status=Pagamento.Status.PENDENTE),
                Pagamento(aluno=user, descricao="Taxa de Exame Pratico", valor=Decimal("280.00"), vencimento=date(2025, 1, 25), status=Pagamento.Status.PENDENTE),
            ]
        )

    if not Certificado.objects.filter(aluno=user).exists():
        Certificado.objects.bulk_create(
            [
                Certificado(aluno=user, nome="Conclusão Aulas Teóricas"),
                Certificado(aluno=user, nome="Exame Médico"),
                Certificado(aluno=user, nome="Exame Psicotécnico"),
            ]
        )

    for instrutor in ["Carlos Silva", "Maria Santos", "João Pedro", "Ana Costa"]:
        Avaliacao.objects.get_or_create(
            titulo=f"Avaliação do instrutor {instrutor}",
            defaults={"descricao": "Feedback das aulas práticas", "instrutor": instrutor},
        )

    return progresso


@login_required(login_url="/login/")
def dashboard_view(request):
    progresso = ensure_initial_student_data(request.user)
    proximas_aulas = Agendamento.objects.filter(
        aluno=request.user,
        ativo=True,
        status=Agendamento.Status.AGENDADO,
    ).order_by("data", "horario")[:2]
    pagamentos_pendentes = Pagamento.objects.filter(
        aluno=request.user,
        ativo=True,
        status=Pagamento.Status.PENDENTE,
    ).order_by("vencimento")[:2]
    aulas_para_avaliar = Agendamento.objects.filter(
        aluno=request.user,
        ativo=True,
        status=Agendamento.Status.CONCLUIDO,
        avaliado=False,
    ).exclude(instrutor="")[:2]

    context = {
        "progresso": progresso,
        "proximas_aulas": proximas_aulas,
        "pagamentos_pendentes": pagamentos_pendentes,
        "aulas_para_avaliar": aulas_para_avaliar,
        "avaliacoes_count": ResultadoAvaliacao.objects.filter(aluno=request.user, ativo=True).count(),
    }
    return render(request, "progresso/dashboard.html", context)
