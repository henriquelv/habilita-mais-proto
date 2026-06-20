from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from apps.progresso.views.dashboard_views import ensure_initial_student_data

from ..models import Pagamento


@login_required(login_url="/login/")
def pagamentos_view(request):
    ensure_initial_student_data(request.user)
    if request.method == "POST":
        pagamento = get_object_or_404(Pagamento, pk=request.POST.get("pagamento_id"), aluno=request.user, ativo=True)
        pagamento.status = Pagamento.Status.PAGO
        pagamento.save(update_fields=["status"])
        messages.success(request, f"Pagamento de {pagamento.descricao} confirmado!")
        return redirect("pagamentos")

    pagamentos = Pagamento.objects.filter(aluno=request.user, ativo=True)
    pendentes = pagamentos.filter(status=Pagamento.Status.PENDENTE)
    pagos = pagamentos.filter(status=Pagamento.Status.PAGO)
    context = {
        "pendentes": pendentes,
        "pagos": pagos,
        "total_pago": pagos.aggregate(total=Sum("valor"))["total"] or 0,
        "total_pendente": pendentes.aggregate(total=Sum("valor"))["total"] or 0,
    }
    context["total"] = context["total_pago"] + context["total_pendente"]
    return render(request, "pagamentos/pagamentos.html", context)
