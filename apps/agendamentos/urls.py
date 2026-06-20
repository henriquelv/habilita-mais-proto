from django.urls import path

from .views import agendamento_view, cancelar_agendamento_view, meus_agendamentos_view


urlpatterns = [
    path("agendamento/", agendamento_view, name="agendamento"),
    path("meus-agendamentos/", meus_agendamentos_view, name="meus_agendamentos"),
    path("meus-agendamentos/<int:pk>/cancelar/", cancelar_agendamento_view, name="cancelar_agendamento"),
]
