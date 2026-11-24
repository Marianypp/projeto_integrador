from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from drf_spectacular.utils import extend_schema, OpenApiResponse


class TokenResponseSerializer(serializers.Serializer):
    """Formato da resposta retornada quando o login é válido."""

    token = serializers.CharField()


class TokenObtainView(ObtainAuthToken):
    """Autentica um usuário e retorna seu token de acesso."""

    serializer_class = AuthTokenSerializer

    @extend_schema(
        tags=["Autenticação"],
        summary="Obter token de acesso",
        description=(
            "Recebe usuário e senha de uma conta cadastrada no Django. "
            "Com credenciais válidas, retorna um token que deve ser "
            "enviado nas operações protegidas pelo cabeçalho "
            "Authorization: Token <token>."
        ),
        request=AuthTokenSerializer,
        responses={
            200: TokenResponseSerializer,
            400: OpenApiResponse(
                description="Usuário ou senha inválidos."
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
