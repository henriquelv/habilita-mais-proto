from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from apps.agendamentos.models import Agendamento
from apps.progresso.views.dashboard_views import ensure_initial_student_data

from ..forms import ResultadoAvaliacaoForm
from ..models import Avaliacao, ResultadoAvaliacao


@login_required(login_url="/login/")
def avaliacoes_view(request):
    ensure_initial_student_data(request.user)
    form = ResultadoAvaliacaoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        instrutor = form.cleaned_data["instrutor"]
        avaliacao, _ = Avaliacao.objects.get_or_create(
            titulo=f"Avaliação do instrutor {instrutor}",
            defaults={"descricao": "Feedback das aulas práticas", "instrutor": instrutor},
        )
        ResultadoAvaliacao.objects.create(
            aluno=request.user,
            avaliacao=avaliacao,
            nota=form.cleaned_data["nota"],
            comentario=form.cleaned_data["comentario"],
            aprovado=form.cleaned_data["nota"] >= 3,
        )
        Agendamento.objects.filter(aluno=request.user, instrutor=instrutor, status=Agendamento.Status.CONCLUIDO).update(avaliado=True)
        messages.success(request, "Avaliação enviada com sucesso! Obrigado pelo feedback.")
        return redirect("avaliacoes")

    aulas_pendentes = Agendamento.objects.filter(
        aluno=request.user,
        ativo=True,
        status=Agendamento.Status.CONCLUIDO,
        avaliado=False,
    ).exclude(instrutor="")
    instrutores = Avaliacao.objects.filter(ativo=True).values("instrutor").annotate(
        media=Avg("resultadoavaliacao__nota"),
        total=Count("resultadoavaliacao"),
    )
    resultados = ResultadoAvaliacao.objects.filter(aluno=request.user, ativo=True).select_related("avaliacao")

    return render(
        request,
        "avaliacoes/avaliacoes.html",
        {
            "form": form,
            "aulas_pendentes": aulas_pendentes,
            "instrutores": instrutores,
            "resultados": resultados,
        },
    )
