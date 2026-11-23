from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    status_api,
    ClienteViewSet,
    VendedorViewSet,
    clientes_por_bairro,
    clientes_por_vendedor
)


router = DefaultRouter()

router.register(
    r"clientes",
    ClienteViewSet,
    basename="cliente"
)

router.register(
    r"vendedores",
    VendedorViewSet,
    basename="vendedor"
)


urlpatterns = [
    path(
        "status/",
        status_api,
        name="status-api"
    ),

    path(
        "consultas/clientes-por-bairro/",
        clientes_por_bairro,
        name="clientes-por-bairro"
    ),

    path(
        "consultas/clientes-por-vendedor/",
        clientes_por_vendedor,
        name="clientes-por-vendedor"
    ),

    path(
        "",
        include(router.urls)
    ),
]
