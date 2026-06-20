from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..forms import PerfilAlunoForm
from ..models import PerfilAluno


@login_required(login_url="/login/")
def perfil_view(request):
    # busca ou cria o perfil do usuário se ainda não existir
    perfil, _ = PerfilAluno.objects.get_or_create(
        usuario=request.user,
        defaults={"cpf": "", "telefone": ""},
    )
    # retorna o formulário com os dados atuais
    form = PerfilAlunoForm(request.POST or None, instance=perfil, user=request.user)

    if request.method == "POST" and form.is_valid():
        # salva as alterações do formulário de perfil
        form.save()
        messages.success(request, "Perfil atualizado com sucesso!")

    return render(request, "accounts/perfil.html", {"form": form, "perfil": perfil})
