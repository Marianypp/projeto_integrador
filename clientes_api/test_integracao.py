"""Testes simples das URLs, documentação e permissões."""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class IntegracaoAPITests(APITestCase):
    def test_listagem_publica(self):
        self.assertEqual(self.client.get('/api/projetos/').status_code, 200)
        self.assertEqual(self.client.get('/api/equipes/').status_code, 200)

    def test_documentacao_abre(self):
        self.assertEqual(self.client.get('/api/schema/').status_code, 200)
        self.assertEqual(self.client.get('/api/docs/').status_code, 200)
        self.assertEqual(self.client.get('/api/docs/redoc/').status_code, 200)

    def test_escrita_exige_autenticacao(self):
        dados = {
            'titulo': 'Exemplo', 'descricao': 'Teste de integração',
            'cliente': 'Cliente de exemplo', 'status': 'planejado',
            'data_inicio': '2026-11-01', 'data_fim_prevista': '2026-12-01',
        }
        resposta = self.client.post('/api/projetos/', dados, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

        usuario = get_user_model().objects.create_user(
            username='integracao_teste', password='senha-temporaria-de-teste'
        )
        token = Token.objects.create(user=usuario)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        resposta = self.client.post('/api/projetos/', dados, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
