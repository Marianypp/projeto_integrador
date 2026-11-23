
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    status_api,
    ClienteViewSet,
    VendedorViewSet
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
        "",
        include(router.urls)
    ),
]
