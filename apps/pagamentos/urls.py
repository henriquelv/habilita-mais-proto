from django.urls import path

from .views import pagamentos_view


urlpatterns = [
    path("pagamentos/", pagamentos_view, name="pagamentos"),
]
