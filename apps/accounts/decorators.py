from django.contrib.auth.decorators import user_passes_test


def _tipo_usuario(user):
    if not user.is_authenticated:
        return None
    if user.is_staff or user.is_superuser:
        return "admin"
    perfil = getattr(user, "perfil", None)
    return getattr(perfil, "tipo_usuario", None)


def aluno_required(view_func):
    """Permite acesso apenas a usuários com perfil de aluno."""
    return user_passes_test(
        lambda user: _tipo_usuario(user) == "aluno",
        login_url="/login/",
    )(view_func)


def instrutor_required(view_func):
    """Permite acesso apenas a instrutores."""
    return user_passes_test(
        lambda user: _tipo_usuario(user) == "instrutor",
        login_url="/login/",
    )(view_func)
