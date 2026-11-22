
from django.urls import path

from .views import (
    status_api,
    listar_clientes,
    consultar_cliente
)


urlpatterns = [
    path(
        "status/",
        status_api,
        name="status-api"
    ),

    path(
        "clientes/",
        listar_clientes,
        name="listar-clientes"
    ),

    path(
        "clientes/<str:id_cliente>/",
        consultar_cliente,
        name="consultar-cliente"
    ),
]


