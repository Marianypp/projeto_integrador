from .models import Cliente, Vendedor
from rest_framework import serializers

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id_cliente',
            'razao_social',
            'cnpj_normalizado',
            'telefone_normalizado',
            'email',
            'bairro_normalizado',
            'cep_normalizado',
            'data_cadastro_normalizado',
            'vendedor',
        ]

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ['id_vendedor', 'nome_vendedor']
