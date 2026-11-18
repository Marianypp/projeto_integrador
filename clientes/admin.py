
from django.contrib import admin

from .models import (
    Cliente,
    Vendedor,
    Auditoria
)


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):

    list_display = ("id", "nome")

    search_fields = ("nome",)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        "id_cliente",
        "razao_social",
        "bairro",
        "vendedor",
        "status_consulta_cep"
    )

    search_fields = (
        "razao_social",
        "cnpj",
        "id_cliente"
    )

    list_filter = (
        "bairro",
        "vendedor",
        "status_consulta_cep"
    )


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):

    list_display = (
        "cliente",
        "campo",
        "status",
        "fonte_referencia",
        "data_registro"
    )

    list_filter = (
        "campo",
        "status",
        "fonte_referencia"
    )

    search_fields = (
        "cliente__id_cliente",
        "valor_original",
        "valor_tratado",
        "criterio"
    )

    readonly_fields = (
        "cliente",
        "campo",
        "valor_original",
        "valor_tratado",
        "valor_referencia",
        "criterio",
        "fonte_referencia",
        "status",
        "data_registro"
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

