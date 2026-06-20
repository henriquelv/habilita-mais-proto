from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


@login_required(login_url="/login/")
def suporte(request):
    if request.method == "POST":
        messages.success(request, "Mensagem enviada! Retornaremos em breve.")
    return render(request, "core/suporte.html")
