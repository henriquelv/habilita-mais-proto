from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from apps.progresso.models import ProgressoAluno

from ..forms import CadastroForm, LoginForm
from ..models import PerfilAluno


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)

        if user is None:
            found_user = User.objects.filter(email__iexact=username).first()
            if found_user:
                user = authenticate(request, username=found_user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect("dashboard")
        messages.error(request, "Usuario ou senha invalidos.")

    return render(request, "accounts/login.html", {"form": form})


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = CadastroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        nome = form.cleaned_data["nome"].strip()
        partes_nome = nome.split(" ", 1)
        user = User.objects.create_user(
            username=form.cleaned_data["email"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            first_name=partes_nome[0],
            last_name=partes_nome[1] if len(partes_nome) > 1 else "",
        )
        PerfilAluno.objects.create(
            usuario=user,
            cpf=form.cleaned_data["cpf"],
            telefone=form.cleaned_data["telefone"],
        )
        ProgressoAluno.objects.get_or_create(aluno=user)
        login(request, user)
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect("dashboard")

    return render(request, "accounts/cadastro.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect("home")
