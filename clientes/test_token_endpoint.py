from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Vendedor


class TesteEmissaoToken(APITestCase):
    def setUp(self):
        usuario_model = get_user_model()
        self.usuario = usuario_model.objects.create_user(
            username="usuario_token_teste",
            password="SenhaToken123!",
        )
        self.url_token = reverse("api-token")

    def test_emite_token_com_credenciais_validas(self):
        resposta = self.client.post(
            self.url_token,
            {
                "username": "usuario_token_teste",
                "password": "SenhaToken123!",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
            resposta.data,
        )
        self.assertIn("token", resposta.data)
        self.assertTrue(
            Token.objects.filter(
                user=self.usuario,
                key=resposta.data["token"],
            ).exists()
        )

    def test_rejeita_credenciais_invalidas(self):
        resposta = self.client.post(
            self.url_token,
            {
                "username": "usuario_token_teste",
                "password": "senha_incorreta",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertNotIn("token", resposta.data)

    def test_token_emitido_permite_cadastrar_vendedor(self):
        resposta_token = self.client.post(
            self.url_token,
            {
                "username": "usuario_token_teste",
                "password": "SenhaToken123!",
            },
            format="json",
        )

        self.assertEqual(
            resposta_token.status_code,
            status.HTTP_200_OK,
            resposta_token.data,
        )

        token = resposta_token.data["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

        resposta_cadastro = self.client.post(
            reverse("vendedor-list"),
            {"nome": "Vendedor Criado com Token"},
            format="json",
        )

        self.assertEqual(
            resposta_cadastro.status_code,
            status.HTTP_201_CREATED,
            resposta_cadastro.data,
        )
        self.assertTrue(
            Vendedor.objects.filter(
                nome="Vendedor Criado com Token"
            ).exists()
        )

    def test_rota_de_token_aparece_no_openapi(self):
        resposta = self.client.get(
            reverse("schema"),
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn(
            "/api/auth/token/",
            resposta.json()["paths"],
        )
