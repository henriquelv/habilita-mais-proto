from django.urls import path

from .views import certificados_view, dashboard_view, historico_view


urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("historico/", historico_view, name="historico"),
    path("certificados/", certificados_view, name="certificados"),
]
