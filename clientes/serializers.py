
from rest_framework import serializers

from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):

    vendedor_nome = serializers.CharField(
        source="vendedor.nome",
        read_only=True
    )

    class Meta:

        model = Cliente

        fields = [
            "id_cliente",
            "razao_social",
            "cnpj",
            "telefone",
            "email",
            "bairro",
            "cep",
            "cidade",
            "uf",
            "data_cadastro",
            "vendedor",
            "vendedor_nome",
            "status_consulta_cep",
            "comparacao_bairro_cep"
        ]
