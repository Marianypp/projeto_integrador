from django.db import transaction
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError

from .filters import (
    ClienteFilter,
    VendedorFilter
)

from django_filters.rest_framework import (
    DjangoFilterBackend
)

from django.shortcuts import get_object_or_404

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from drf_spectacular.types import OpenApiTypes

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)

from .models import Cliente, Vendedor, AuditoriaAPI

from .pagination import (
    PaginacaoPadrao,
    PaginacaoAuditoria
)

from .permissions import PermissaoGerenciamento

from rest_framework import (
    viewsets,
    status
)

from rest_framework.decorators import (
    action,
    api_view,
    permission_classes
)

from rest_framework.exceptions import ValidationError

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser
)

from rest_framework.response import Response

from .serializers import (
    ClienteSerializer,
    ClienteEscritaSerializer,
    VendedorSerializer,
    StatusAPISerializer,
    ConsultaBairroSerializer,
    ConsultaVendedorSerializer,
    ErroConsultaSerializer,
    AuditoriaAPISerializer,
)

from .services import (
    capturar_dados,
    registrar_auditoria
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
            "Retorna uma lista paginada de clientes "
            "ativos. Requer autenticação."
        ),
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
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
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
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
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
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
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
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
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
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
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
        responses={
            204: None
        }
    ),
)
class ClienteViewSet(viewsets.ModelViewSet):

    permission_classes = [
    PermissaoGerenciamento
]

    lookup_field = "id_cliente"

    pagination_class = PaginacaoPadrao


    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = ClienteFilter

    search_fields = [
        "razao_social",
        "cnpj",
        "bairro",
        "vendedor__nome"
    ]

    ordering_fields = [
        "id_cliente",
        "razao_social",
        "bairro",
        "cidade",
        "data_cadastro",
        "vendedor__nome"
    ]

    ordering = [
        "id_cliente"
    ]


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

            registrar_auditoria(
                request=request,
                entidade="Cliente",
                identificador=cliente.pk,
                operacao=AuditoriaAPI.Operacao.CRIACAO,
                dados_anteriores={},
                dados_posteriores=capturar_dados(
                    cliente
                )
            )

        return Response(
            ClienteSerializer(cliente).data,
            status=status.HTTP_201_CREATED
        )


    
    def update(self, request, *args, **kwargs):

        parcial = kwargs.pop(
            "partial",
            False
        )

        with transaction.atomic():

            cliente = get_object_or_404(
                Cliente.objects
                .select_for_update()
                .filter(ativo=True),

                id_cliente=self.kwargs["id_cliente"]
            )

            self.check_object_permissions(
                request,
                cliente
            )

            dados_anteriores = capturar_dados(
                cliente
            )

            serializer = self.get_serializer(
                cliente,
                data=request.data,
                partial=parcial
            )

            serializer.is_valid(
                raise_exception=True
            )

            cliente = serializer.save()

            dados_posteriores = capturar_dados(
                cliente
            )

            registrar_auditoria(
                request=request,
                entidade="Cliente",
                identificador=cliente.pk,
                operacao=(
                    AuditoriaAPI.Operacao.ATUALIZACAO
                ),
                dados_anteriores=dados_anteriores,
                dados_posteriores=dados_posteriores
            )

        return Response(
            ClienteSerializer(cliente).data,
            status=status.HTTP_200_OK
        )


    
    def destroy(self, request, *args, **kwargs):

        with transaction.atomic():

            cliente = get_object_or_404(
                Cliente.objects
                .select_for_update()
                .filter(ativo=True),

                id_cliente=self.kwargs["id_cliente"]
            )

            self.check_object_permissions(
                request,
                cliente
            )

            dados_anteriores = capturar_dados(
                cliente
            )

            cliente.ativo = False

            cliente.save(
                update_fields=["ativo"]
            )

            dados_posteriores = capturar_dados(
                cliente
            )

            registrar_auditoria(
                request=request,
                entidade="Cliente",
                identificador=cliente.pk,
                operacao=(
                    AuditoriaAPI.Operacao.INATIVACAO
                ),
                dados_anteriores=dados_anteriores,
                dados_posteriores=dados_posteriores
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )



@extend_schema_view(

    list=extend_schema(
        tags=["Vendedores"],
        summary="Listar vendedores",
        description=(
            "Retorna uma lista paginada de clientes ativos. Requer autenticação."
        ),
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
    ),

    retrieve=extend_schema(
        tags=["Vendedores"],
        summary="Consultar vendedor",
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
    ),

    create=extend_schema(
        tags=["Vendedores"],
        summary="Cadastrar vendedor",
        description="Exige autenticação.",
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
    ),

    update=extend_schema(
        tags=["Vendedores"],
        summary="Atualizar vendedor",
        description="Exige autenticação.",
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
    ),

    partial_update=extend_schema(
        tags=["Vendedores"],
        summary="Atualizar vendedor parcialmente",
        description="Exige autenticação.",
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
    ),

    destroy=extend_schema(
        tags=["Vendedores"],
        summary="Excluir vendedor",
        description=(
            "Exclui um vendedor sem clientes vinculados. "
            "Exige autenticação."
        ),
        auth=[
            {"tokenAuth": []},
            {"cookieAuth": []}
        ],
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
    PermissaoGerenciamento
]

    serializer_class = VendedorSerializer

    pagination_class = PaginacaoPadrao


    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = VendedorFilter

    search_fields = [
        "nome"
    ]

    ordering_fields = [
        "id",
        "nome",
        "total_clientes_ativos"
    ]

    ordering = [
        "nome",
        "id"
    ]


    
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

                vendedor = get_object_or_404(
                    Vendedor.objects.select_for_update(),

                    pk=instance.pk
                )

                self.check_object_permissions(
                    self.request,
                    vendedor
                )

                identificador = vendedor.pk

                dados_anteriores = capturar_dados(
                    vendedor
                )

                vendedor.delete()

                registrar_auditoria(
                    request=self.request,
                    entidade="Vendedor",
                    identificador=identificador,
                    operacao=(
                        AuditoriaAPI.Operacao.EXCLUSAO
                    ),
                    dados_anteriores=dados_anteriores,
                    dados_posteriores={}
                )

        except ProtectedError:

            raise ValidationError({
                "erro": (
                    "Não é possível excluir este "
                    "vendedor porque existem "
                    "clientes vinculados."
                )
            })



    
    
    @extend_schema(
        tags=["Vendedores"],

        summary="Listar clientes de um vendedor",

        description=(
            "Retorna uma lista paginada dos "
            "clientes ativos vinculados ao vendedor."
        ),

        responses={
            200: ClienteSerializer(many=True)
        }
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="clientes",
        filter_backends=[]
    )
    def clientes(self, request, pk=None):

        vendedor = self.get_object()

        clientes = (
            vendedor.clientes
            .filter(ativo=True)
            .select_related("vendedor")
            .order_by("id_cliente")
        )

        pagina = self.paginate_queryset(
            clientes
        )

        if pagina is not None:

            serializer = ClienteSerializer(
                pagina,
                many=True
            )

            return self.get_paginated_response(
                serializer.data
            )

        serializer = ClienteSerializer(
            clientes,
            many=True
        )

        return Response(
            serializer.data
        )



    def perform_create(self, serializer):

        with transaction.atomic():

            vendedor = serializer.save()

            registrar_auditoria(
                request=self.request,
                entidade="Vendedor",
                identificador=vendedor.pk,
                operacao=AuditoriaAPI.Operacao.CRIACAO,
                dados_anteriores={},
                dados_posteriores=capturar_dados(
                    vendedor
                )
            )


    def update(self, request, *args, **kwargs):

        parcial = kwargs.pop(
            "partial",
            False
        )

        with transaction.atomic():

            vendedor = get_object_or_404(
                Vendedor.objects.select_for_update(),

                pk=self.kwargs["pk"]
            )

            self.check_object_permissions(
                request,
                vendedor
            )

            dados_anteriores = capturar_dados(
                vendedor
            )

            serializer = self.get_serializer(
                vendedor,
                data=request.data,
                partial=parcial
            )

            serializer.is_valid(
                raise_exception=True
            )

            vendedor = serializer.save()

            registrar_auditoria(
                request=request,
                entidade="Vendedor",
                identificador=vendedor.pk,
                operacao=(
                    AuditoriaAPI.Operacao.ATUALIZACAO
                ),
                dados_anteriores=dados_anteriores,
                dados_posteriores=capturar_dados(
                    vendedor
                )
            )

        return Response(
            VendedorSerializer(vendedor).data,
            status=status.HTTP_200_OK
        )



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

            raise ValidationError({
                "erro": (
                    "vendedor_id deve ser um "
                    "número inteiro positivo."
                )
            })

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


@extend_schema_view(

    list=extend_schema(
        tags=["Auditoria"],
        summary="Listar registros de auditoria",
        description=(
            "Retorna o histórico das operações "
            "realizadas pela API. "
            "Acesso restrito a administradores."
        ),

        parameters=[
            OpenApiParameter(
                name="entidade",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Cliente ou Vendedor."
            ),

            OpenApiParameter(
                name="operacao",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                enum=[
                    "CRIACAO",
                    "ATUALIZACAO",
                    "EXCLUSAO",
                    "INATIVACAO"
                ]
            ),

            OpenApiParameter(
                name="identificador",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description=(
                    "Identificador do registro auditado."
                )
            )
        ]
    ),

    retrieve=extend_schema(
        tags=["Auditoria"],
        summary="Consultar registro de auditoria",
        description=(
            "Consulta um registro específico "
            "do histórico de operações."
        )
    )
)
class AuditoriaAPIViewSet(
    viewsets.ReadOnlyModelViewSet
):

    serializer_class = AuditoriaAPISerializer

    permission_classes = [
        IsAdminUser
    ]

    pagination_class = PaginacaoAuditoria


    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [
        "entidade",
        "identificador_registro",
        "usuario_nome",
        "operacao"
    ]

    ordering_fields = [
        "id",
        "data_registro",
        "entidade",
        "operacao",
        "usuario_nome"
    ]

    ordering = [
        "-data_registro",
        "-id"
    ]



    def get_queryset(self):

        auditorias = (
            AuditoriaAPI.objects.all()
        )

        if self.action == "list":

            entidade = (
                self.request.query_params.get(
                    "entidade"
                )
            )

            operacao = (
                self.request.query_params.get(
                    "operacao"
                )
            )

            identificador = (
                self.request.query_params.get(
                    "identificador"
                )
            )

            if entidade:

                auditorias = auditorias.filter(
                    entidade__iexact=entidade.strip()
                )

            if operacao:

                auditorias = auditorias.filter(
                    operacao__iexact=operacao.strip()
                )

            if identificador:

                auditorias = auditorias.filter(
                    identificador_registro=(
                        identificador.strip()
                    )
                )

        return auditorias.order_by(
            "-data_registro",
            "-id"
        )
