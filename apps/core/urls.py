from django.urls import path

from .views import home, suporte


urlpatterns = [
    path("", home, name="home"),
    path("suporte/", suporte, name="suporte"),
]
