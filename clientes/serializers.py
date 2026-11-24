

from rest_framework import serializers

from .models import Cliente, Vendedor

from etl.normalizacao import (
    normalizar_cnpj,
    normalizar_telefone,
    normalizar_cep,
    normalizar_bairro
)


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
            "comparacao_bairro_cep",
            "ativo"
        ]

        read_only_fields = fields


class ClienteEscritaSerializer(serializers.ModelSerializer):

    telefone = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    cep = serializers.CharField(
        max_length=12,
        required=False,
        allow_null=True,
        allow_blank=True
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
            "vendedor"
        ]

    
    def validate_id_cliente(self, valor):

        valor = valor.strip().upper()

        if not valor:
            raise serializers.ValidationError(
                "O identificador é obrigatório."
            )

        if self.instance is None:

            if Cliente.objects.filter(
                id_cliente=valor
            ).exists():

                raise serializers.ValidationError(
                    "Já existe um cliente com esse identificador."
                )

        return valor


    def validate_cnpj(self, valor):

        tratado = normalizar_cnpj(valor)

        if tratado is None:
            raise serializers.ValidationError(
                "O CNPJ deve conter 14 dígitos."
            )

        return tratado

    def validate_telefone(self, valor):

        tratado = normalizar_telefone(valor)

        if tratado is None:
            raise serializers.ValidationError(
                "Informe um telefone com DDD válido "
                "quanto ao formato."
            )

        return tratado

    def validate_cep(self, valor):

        if valor in (None, ""):
            return None

        tratado = normalizar_cep(valor)

        if tratado is None:
            raise serializers.ValidationError(
                "Informe um CEP com oito dígitos."
            )

        return tratado

    def validate_bairro(self, valor):

        if valor in (None, ""):
            return None

        tratado = normalizar_bairro(valor)

        if tratado is None:
            raise serializers.ValidationError(
                "Bairro não reconhecido. "
                "Solicite revisão do cadastro."
            )

        return tratado

    def validate_uf(self, valor):

        valor = valor.strip().upper()

        if len(valor) != 2 or not valor.isalpha():
            raise serializers.ValidationError(
                "A UF deve conter duas letras."
            )

        return valor

    def validate_vendedor(self, vendedor):

        if vendedor is None:
            raise serializers.ValidationError(
                "Selecione um vendedor."
            )

        return vendedor

    def validate(self, atributos):

        # O identificador é imutável depois da criação.
        if self.instance is not None:
            novo_id = atributos.get("id_cliente")

            if (
                novo_id is not None
                and novo_id != self.instance.id_cliente
            ):
                raise serializers.ValidationError({
                    "id_cliente":
                    "O identificador não pode ser alterado."
                })

        return atributos


class VendedorSerializer(serializers.ModelSerializer):

    quantidade_clientes = serializers.SerializerMethodField()

    class Meta:
        model = Vendedor

        fields = [
            "id",
            "nome",
            "quantidade_clientes"
        ]

        read_only_fields = [
            "id",
            "quantidade_clientes"
        ]

    
    def get_quantidade_clientes(self, obj):

        if hasattr(obj, "total_clientes_ativos"):
            return obj.total_clientes_ativos

        return obj.clientes.filter(
            ativo=True
        ).count()


    def validate_nome(self, valor):

        valor = " ".join(valor.split())

        if len(valor) < 3:
            raise serializers.ValidationError(
                "O nome deve conter pelo menos "
                "três caracteres."
            )

        return valor


class StatusAPISerializer(serializers.Serializer):

    mensagem = serializers.CharField()
    status = serializers.CharField()
    versao = serializers.CharField()


class BairroAgrupadoSerializer(serializers.Serializer):

    bairro = serializers.CharField()
    total_clientes = serializers.IntegerField()


class ConsultaBairroSerializer(serializers.Serializer):

    total_bairros = serializers.IntegerField()

    total_clientes = serializers.IntegerField()

    resultados = BairroAgrupadoSerializer(
        many=True
    )


class VendedorAgrupadoSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    nome = serializers.CharField()
    total_clientes = serializers.IntegerField()


class ConsultaVendedorSerializer(serializers.Serializer):

    total_vendedores = serializers.IntegerField()

    total_clientes = serializers.IntegerField()

    resultados = VendedorAgrupadoSerializer(
        many=True
    )


class ErroConsultaSerializer(serializers.Serializer):

    erro = serializers.CharField()
