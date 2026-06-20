from django.urls import path

from .views import avaliacoes_view


urlpatterns = [
    path("avaliacoes/", avaliacoes_view, name="avaliacoes"),
]
