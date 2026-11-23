from django.db.models import Count, Q

from django.db.models.deletion import ProtectedError

from rest_framework.exceptions import ValidationError

from django.db import transaction

from rest_framework import (
    viewsets,
    status
)

from rest_framework.decorators import (
    action,
    api_view,
    permission_classes
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly
)

from rest_framework.response import Response

from .models import Cliente, Vendedor

from .serializers import (
    ClienteSerializer,
    ClienteEscritaSerializer,
    VendedorSerializer
)


@api_view(["GET"])
@permission_classes([AllowAny])
def status_api(request):

    return Response({
        "mensagem": "API Distribuidora Vetor",
        "status": "online",
        "versao": "1.0"
    })


class ClienteViewSet(viewsets.ModelViewSet):

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    lookup_field = "id_cliente"

    def get_queryset(self):

        return (
            Cliente.objects
            .filter(ativo=True)
            .select_related("vendedor")
            .order_by("id_cliente")
        )

    def get_serializer_class(self):

        if self.action in [
            "create",
            "update",
            "partial_update"
        ]:
            return ClienteEscritaSerializer

        return ClienteSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        with transaction.atomic():
            cliente = serializer.save()

        resposta = ClienteSerializer(
            cliente
        )

        return Response(
            resposta.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        parcial = kwargs.pop("partial", False)

        cliente = self.get_object()

        serializer = ClienteEscritaSerializer(
            cliente,
            data=request.data,
            partial=parcial
        )

        serializer.is_valid(
            raise_exception=True
        )

        with transaction.atomic():
            cliente = serializer.save()

        resposta = ClienteSerializer(
            cliente
        )

        return Response(
            resposta.data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):

        cliente = self.get_object()

        with transaction.atomic():

            cliente.ativo = False

            cliente.save(
                update_fields=["ativo"]
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class VendedorViewSet(viewsets.ModelViewSet):

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    serializer_class = VendedorSerializer

    
    def get_queryset(self):

        return (
            Vendedor.objects
            .annotate(
                total_clientes_ativos=Count(
                    "clientes",
                    filter=Q(clientes__ativo=True)
                )
            )
            .order_by("nome")
        )


    def perform_destroy(self, instance):

        try:
            with transaction.atomic():
                instance.delete()

        except ProtectedError:

            raise ValidationError({
                "erro": (
                    "Não é possível excluir este vendedor "
                    "porque existem clientes vinculados."
                )
            })


    @action(
        detail=True,
        methods=["get"],
        url_path="clientes"
    )
    def clientes(self, request, pk=None):

        vendedor = self.get_object()

        clientes = (
            vendedor.clientes
            .filter(ativo=True)
            .select_related("vendedor")
            .order_by("id_cliente")
        )

        serializer = ClienteSerializer(
            clientes,
            many=True
        )

        return Response(serializer.data)
