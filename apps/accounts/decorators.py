from django.contrib.auth.decorators import user_passes_test


def _tipo_usuario(user):
    if not user.is_authenticated:
        return None
    if user.is_staff or user.is_superuser:
        return "admin"
    perfil = getattr(user, "perfil", None)
    return getattr(perfil, "tipo_usuario", None)


def _is_admin(user):
    return _tipo_usuario(user) == "admin"


def aluno_required(view_func):
    """Permite acesso a alunos e administradores."""
    return user_passes_test(
        lambda user: _tipo_usuario(user) == "aluno" or _is_admin(user),
        login_url="/login/",
    )(view_func)


def instrutor_required(view_func):
    """Permite acesso a instrutores e administradores."""
    return user_passes_test(
        lambda user: _tipo_usuario(user) == "instrutor" or _is_admin(user),
        login_url="/login/",
    )(view_func)
