from django import forms
from django.contrib.auth.models import User

from .models import PerfilAluno


class LoginForm(forms.Form):
    username = forms.CharField(
        label="E-mail ou usuário",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "seu@email.com"}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite sua senha"}),
    )


class CadastroForm(forms.Form):
    nome = forms.CharField(
        label="Nome completo",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Seu nome"}),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "seu@email.com"}),
    )
    password = forms.CharField(
        label="Senha",
        min_length=8,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite sua senha"}),
    )
    cpf = forms.CharField(
        label="CPF",
        max_length=14,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "123.456.789-00"}),
    )
    telefone = forms.CharField(
        label="Telefone",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "(11) 99999-9999"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        if PerfilAluno.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Já existe uma conta com este CPF.")
        return cpf


class PerfilAlunoForm(forms.ModelForm):
    first_name = forms.CharField(label="Nome", max_length=150, required=False)
    last_name = forms.CharField(label="Sobrenome", max_length=150, required=False)
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = PerfilAluno
        fields = [
            "first_name",
            "last_name",
            "email",
            "cpf",
            "telefone",
            "data_nascimento",
            "cep",
            "endereco",
            "categoria_cnh",
        ]
        widgets = {
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "cep": forms.TextInput(attrs={"class": "form-control"}),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "categoria_cnh": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name
        self.fields["email"].initial = user.email
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def save(self, commit=True):
        perfil = super().save(commit=False)
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save()
            perfil.save()
        return perfil
