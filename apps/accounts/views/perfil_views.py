from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..forms import PerfilAlunoForm
from ..models import PerfilAluno


@login_required(login_url="/login/")
def perfil_view(request):
    perfil, _ = PerfilAluno.objects.get_or_create(
        usuario=request.user,
        defaults={"cpf": "", "telefone": ""},
    )
    form = PerfilAlunoForm(request.POST or None, instance=perfil, user=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Perfil atualizado com sucesso!")

    return render(request, "accounts/perfil.html", {"form": form, "perfil": perfil})
