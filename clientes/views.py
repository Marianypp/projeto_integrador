
from django.shortcuts import get_object_or_404

from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly
)

from rest_framework.response import Response

from .models import Cliente
from .serializers import ClienteSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def status_api(request):

    return Response({
        "mensagem": "API Distribuidora Vetor",
        "status": "online",
        "versao": "1.0"
    })


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def listar_clientes(request):

    clientes = Cliente.objects.select_related(
        "vendedor"
    ).all().order_by("id_cliente")

    serializer = ClienteSerializer(
        clientes,
        many=True
    )

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def consultar_cliente(request, id_cliente):

    cliente = get_object_or_404(
        Cliente.objects.select_related("vendedor"),
        id_cliente=id_cliente
    )

    serializer = ClienteSerializer(cliente)

    return Response(serializer.data)

