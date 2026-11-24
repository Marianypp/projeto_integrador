from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)


class PermissaoGerenciamento(BasePermission):

    message = (
        "Você não possui permissão para "
        "realizar esta operação."
    )

    def has_permission(self, request, view):

        usuario = request.user

        if not usuario or not usuario.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        if usuario.is_staff or usuario.is_superuser:
            return True

        return usuario.groups.filter(
            name="Operadores"
        ).exists()
