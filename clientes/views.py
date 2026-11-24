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
    VendedorSerializer,
    StatusAPISerializer,
    ConsultaBairroSerializer,
    ConsultaVendedorSerializer,
    ErroConsultaSerializer,
)

from drf_spectacular.types import OpenApiTypes

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)


@extend_schema(
    tags=["Status"],

    summary="Verificar status da API",

    description=(
        "Retorna informações sobre o funcionamento "
        "e a versão da API Distribuidora Vetor."
    ),

    responses={
        200: StatusAPISerializer
    }
)
@api_view(["GET"])
@permission_classes([AllowAny])
def status_api(request):

    return Response({
        "mensagem": "API Distribuidora Vetor",
        "status": "online",
        "versao": "1.0"
    })



@extend_schema_view(

    list=extend_schema(
        tags=["Clientes"],
        summary="Listar clientes ativos",
        description=(
            "Retorna os clientes ativos cadastrados "
            "na Distribuidora Vetor."
        ),
        responses={
            200: ClienteSerializer(many=True)
        }
    ),

    retrieve=extend_schema(
        tags=["Clientes"],
        summary="Consultar cliente",
        description=(
            "Consulta um cliente ativo pelo "
            "identificador."
        ),
        responses={
            200: ClienteSerializer
        }
    ),

    create=extend_schema(
        tags=["Clientes"],
        summary="Cadastrar cliente",
        description=(
            "Cadastra um novo cliente. "
            "Exige autenticação."
        ),
        request=ClienteEscritaSerializer,
        responses={
            201: ClienteSerializer
        }
    ),

    update=extend_schema(
        tags=["Clientes"],
        summary="Atualizar cliente",
        description=(
            "Atualiza os dados de um cliente. "
            "Exige autenticação."
        ),
        request=ClienteEscritaSerializer,
        responses={
            200: ClienteSerializer
        }
    ),

    partial_update=extend_schema(
        tags=["Clientes"],
        summary="Atualizar cliente parcialmente",
        description=(
            "Atualiza somente os campos informados. "
            "Exige autenticação."
        ),
        request=ClienteEscritaSerializer,
        responses={
            200: ClienteSerializer
        }
    ),

    destroy=extend_schema(
        tags=["Clientes"],
        summary="Inativar cliente",
        description=(
            "Realiza a exclusão lógica do cliente, "
            "alterando o campo ativo para False. "
            "Exige autenticação."
        ),
        responses={
            204: None
        }
    ),
)
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


@extend_schema_view(

    list=extend_schema(
        tags=["Vendedores"],
        summary="Listar vendedores",
        description=(
            "Retorna os vendedores cadastrados e "
            "a quantidade de clientes ativos."
        )
    ),

    retrieve=extend_schema(
        tags=["Vendedores"],
        summary="Consultar vendedor"
    ),

    create=extend_schema(
        tags=["Vendedores"],
        summary="Cadastrar vendedor",
        description="Exige autenticação."
    ),

    update=extend_schema(
        tags=["Vendedores"],
        summary="Atualizar vendedor",
        description="Exige autenticação."
    ),

    partial_update=extend_schema(
        tags=["Vendedores"],
        summary="Atualizar vendedor parcialmente",
        description="Exige autenticação."
    ),

    destroy=extend_schema(
        tags=["Vendedores"],
        summary="Excluir vendedor",
        description=(
            "Exclui um vendedor sem clientes vinculados. "
            "Exige autenticação."
        ),
        responses={
            204: None,
            400: OpenApiResponse(
                description=(
                    "O vendedor possui clientes vinculados."
                )
            )
        }
    ),
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


    
    @extend_schema(
        tags=["Vendedores"],

        summary="Listar clientes de um vendedor",

        description=(
            "Retorna os clientes ativos vinculados "
            "ao vendedor informado."
        ),

        responses={
            200: ClienteSerializer(many=True)
        }
    )
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




@extend_schema(
    tags=["Consultas"],

    summary="Consultar clientes por bairro",

    description=(
        "Retorna a quantidade de clientes ativos "
        "agrupados pelo bairro normalizado. "
        "Clientes sem bairro informado não são "
        "incluídos na contagem."
    ),

    parameters=[
        OpenApiParameter(
            name="bairro",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Nome do bairro utilizado como filtro."
            ),
            examples=[
                OpenApiExample(
                    "Águas Claras",
                    value="Águas Claras"
                )
            ]
        )
    ],

    responses={
        200: ConsultaBairroSerializer
    },

    examples=[
        OpenApiExample(
            "Exemplo de agrupamento por bairro",

            value={
                "total_bairros": 2,
                "total_clientes": 15,
                "resultados": [
                    {
                        "bairro": "Águas Claras",
                        "total_clientes": 10
                    },
                    {
                        "bairro": "Taguatinga",
                        "total_clientes": 5
                    }
                ]
            },

            response_only=True,
            status_codes=["200"]
        )
    ]
)
@api_view(["GET"])
@permission_classes([AllowAny])
def clientes_por_bairro(request):

    bairro_filtro = request.query_params.get(
        "bairro"
    )

    clientes = (
        Cliente.objects
        .filter(ativo=True)
        .exclude(bairro__isnull=True)
        .exclude(bairro="")
    )

    if bairro_filtro:
        clientes = clientes.filter(
            bairro__iexact=bairro_filtro.strip()
        )

    agrupamento = (
        clientes
        .values("bairro")
        .annotate(
            total_clientes=Count("id_cliente")
        )
        .order_by("bairro")
    )

    resultado = list(agrupamento)

    return Response({
        "total_bairros": len(resultado),

        "total_clientes": sum(
            item["total_clientes"]
            for item in resultado
        ),

        "resultados": resultado
    })




@extend_schema(
    tags=["Consultas"],

    summary="Consultar clientes por vendedor",

    description=(
        "Retorna a quantidade de clientes ativos "
        "associados a cada vendedor. "
        "Vendedores sem clientes ativos também "
        "são apresentados."
    ),

    parameters=[
        OpenApiParameter(
            name="vendedor_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Identificador positivo do vendedor."
            ),
            examples=[
                OpenApiExample(
                    "Vendedor 1",
                    value=1
                )
            ]
        )
    ],

    responses={
        200: ConsultaVendedorSerializer,
        400: ErroConsultaSerializer
    },

    examples=[
        OpenApiExample(
            "Exemplo de agrupamento por vendedor",

            value={
                "total_vendedores": 2,
                "total_clientes": 10,
                "resultados": [
                    {
                        "id": 1,
                        "nome": "Ana",
                        "total_clientes": 6
                    },
                    {
                        "id": 2,
                        "nome": "Carlos",
                        "total_clientes": 4
                    }
                ]
            },

            response_only=True,
            status_codes=["200"]
        )
    ]
)
@api_view(["GET"])
@permission_classes([AllowAny])
def clientes_por_vendedor(request):

    vendedor_id = request.query_params.get(
        "vendedor_id"
    )

    vendedores = Vendedor.objects.all()

    if vendedor_id is not None:

        try:
            identificador = int(vendedor_id)

            if identificador < 1:
                raise ValueError

        except ValueError:
            return Response(
                {
                    "erro": (
                        "vendedor_id deve ser "
                        "um número inteiro positivo."
                    )
                },
                status=400
            )

        vendedores = vendedores.filter(
            pk=identificador
        )

    agrupamento = (
        vendedores
        .annotate(
            total_clientes=Count(
                "clientes",
                filter=Q(clientes__ativo=True)
            )
        )
        .values(
            "id",
            "nome",
            "total_clientes"
        )
        .order_by("nome")
    )

    resultado = list(agrupamento)

    return Response({
        "total_vendedores": len(resultado),

        "total_clientes": sum(
            item["total_clientes"]
            for item in resultado
        ),

        "resultados": resultado
    })


