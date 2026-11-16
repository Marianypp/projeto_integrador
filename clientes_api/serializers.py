"""Serialização dos modelos efetivamente existentes neste branch."""
from rest_framework import serializers
from .models import Equipe, Projeto


class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = [
            'id', 'titulo', 'descricao', 'cliente', 'status',
            'data_inicio', 'data_fim_prevista',
        ]


class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ['id', 'nome', 'descricao', 'projeto', 'lider', 'membros']
