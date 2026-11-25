
from io import StringIO

from django.contrib.auth.models import User, Group

from django.core.management import call_command

from django.urls import reverse

from rest_framework import status

from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase

from .models import (
    Cliente,
    Vendedor,
    AuditoriaAPI
)


class TesteIntegracaoSistema(APITestCase):

    def setUp(self):

        self.operador = User.objects.create_user(
            username="operador_integracao",
            password="SenhaTeste123!"
        )

        grupo, _ = Group.objects.get_or_create(
            name="Operadores"
        )

        self.operador.groups.add(grupo)

        self.token = Token.objects.create(
            user=self.operador
        )

        self.vendedor_a = Vendedor.objects.create(
            nome="Vendedor Integracao A"
        )

        self.vendedor_b = Vendedor.objects.create(
            nome="Vendedor Integracao B"
        )

        self.cliente_a = Cliente.objects.create(
            id_cliente="INT001",
            razao_social="Empresa Integracao A",
            bairro="Taguatinga",
            cidade="Brasília",
            uf="DF",
            vendedor=self.vendedor_a,
            ativo=True
        )

        self.cliente_b = Cliente.objects.create(
            id_cliente="INT002",
            razao_social="Empresa Integracao B",
            bairro="Águas Claras",
            cidade="Brasília",
            uf="DF",
            vendedor=self.vendedor_b,
            ativo=True
        )

        self.cliente_inativo = Cliente.objects.create(
            id_cliente="INT003",
            razao_social="Empresa Inativa",
            bairro="Taguatinga",
            cidade="Brasília",
            uf="DF",
            vendedor=self.vendedor_a,
            ativo=False
        )

        self.url_clientes = reverse(
            "cliente-list"
        )

        self.url_vendedores = reverse(
            "vendedor-list"
        )

        self.url_bairros = reverse(
            "clientes-por-bairro"
        )

        self.url_agrupamento_vendedores = reverse(
            "clientes-por-vendedor"
        )

        self.url_cliente_a = reverse(
            "cliente-detail",
            args=[self.cliente_a.pk]
        )

    def autenticar(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Token {self.token.key}"
            )
        )


    def test_total_clientes_api_igual_banco(self):

        self.autenticar()

        total_banco = Cliente.objects.filter(
            ativo=True
        ).count()

        resposta = self.client.get(
            self.url_clientes
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["count"],
            total_banco
        )

    def test_total_vendedores_api_igual_banco(self):

        self.autenticar()

        resposta = self.client.get(
            self.url_vendedores
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["count"],
            Vendedor.objects.count()
        )

    def test_dados_cliente_api_iguais_banco(self):

        self.autenticar()

        resposta = self.client.get(
            self.url_cliente_a
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["id_cliente"],
            self.cliente_a.pk
        )

        self.assertEqual(
            resposta.data["razao_social"],
            self.cliente_a.razao_social
        )

        self.assertEqual(
            resposta.data["bairro"],
            self.cliente_a.bairro
        )

        self.assertEqual(
            resposta.data["vendedor_nome"],
            self.vendedor_a.nome
        )

    def test_cliente_inativo_ausente_na_api(self):

        self.autenticar()

        resposta = self.client.get(
            self.url_clientes
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        identificadores = [
            item["id_cliente"]
            for item in resposta.data["results"]
        ]

        self.assertNotIn(
            self.cliente_inativo.pk,
            identificadores
        )


    def test_agrupamento_bairros_consistente(self):

        resposta = self.client.get(
            self.url_bairros
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        esperado = {}

        clientes = (
            Cliente.objects
            .filter(ativo=True)
            .exclude(bairro__isnull=True)
            .exclude(bairro="")
        )

        for cliente in clientes:

            bairro = cliente.bairro

            esperado[bairro] = (
                esperado.get(bairro, 0) + 1
            )

        recebido = {
            item["bairro"]: item["total_clientes"]
            for item in resposta.data["resultados"]
        }

        self.assertEqual(
            recebido,
            esperado
        )

        self.assertEqual(
            resposta.data["total_clientes"],
            sum(esperado.values())
        )

    def test_agrupamento_vendedores_consistente(self):

        resposta = self.client.get(
            self.url_agrupamento_vendedores
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        esperado = {
            vendedor.pk: vendedor.clientes.filter(
                ativo=True
            ).count()
            for vendedor in Vendedor.objects.all()
        }

        recebido = {
            item["id"]: item["total_clientes"]
            for item in resposta.data["resultados"]
        }

        self.assertEqual(
            recebido,
            esperado
        )

        self.assertEqual(
            resposta.data["total_clientes"],
            Cliente.objects.filter(
                ativo=True
            ).count()
        )

    def test_cliente_sem_bairro_nos_agrupamentos(self):

        Cliente.objects.create(
            id_cliente="INT004",
            razao_social="Empresa Sem Bairro",
            bairro=None,
            cidade="Brasília",
            uf="DF",
            vendedor=self.vendedor_a,
            ativo=True
        )

        resposta_bairros = self.client.get(
            self.url_bairros
        )

        resposta_vendedores = self.client.get(
            self.url_agrupamento_vendedores
        )

        self.assertEqual(
            resposta_bairros.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta_vendedores.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta_bairros.data["total_clientes"],
            2
        )

        self.assertEqual(
            resposta_vendedores.data["total_clientes"],
            3
        )


    def test_cadastro_normalizado_no_banco(self):

        self.autenticar()

        dados = {

            "id_cliente": "INT004",

            "razao_social": (
                "Empresa Normalizacao"
            ),

            "cnpj": "11222333000181",

            "telefone": "(61) 99999-9999",

            "email": "integracao@example.com",

            "bairro": "Taguatinga",

            "cep": "71926-750",

            "cidade": "Brasília",

            "uf": "df",

            "data_cadastro": "2024-01-15",

            "vendedor": self.vendedor_a.pk

        }

        resposta = self.client.post(
            self.url_clientes,
            dados,
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
            resposta.data
        )

        cliente = Cliente.objects.get(
            pk="INT004"
        )

        self.assertEqual(
            cliente.telefone,
            "61999999999"
        )

        self.assertEqual(
            cliente.cep,
            "71926750"
        )

        self.assertEqual(
            cliente.uf,
            "DF"
        )

        self.assertEqual(
            cliente.vendedor_id,
            self.vendedor_a.pk
        )


    def test_atualizacao_refletida_na_auditoria(self):

        self.autenticar()

        nome_original = (
            self.cliente_a.razao_social
        )

        novo_nome = "Empresa Atualizada"

        resposta = self.client.patch(
            self.url_cliente_a,
            {
                "razao_social": novo_nome
            },
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
            resposta.data
        )

        self.cliente_a.refresh_from_db()

        self.assertEqual(
            self.cliente_a.razao_social,
            novo_nome
        )

        auditoria = AuditoriaAPI.objects.get(
            entidade="Cliente",
            identificador_registro=(
                self.cliente_a.pk
            ),
            operacao="ATUALIZACAO"
        )

        self.assertEqual(
            auditoria.dados_anteriores[
                "razao_social"
            ],
            nome_original
        )

        self.assertEqual(
            auditoria.dados_posteriores[
                "razao_social"
            ],
            novo_nome
        )

        self.assertIn(
            "razao_social",
            auditoria.campos_alterados
        )

        self.assertEqual(
            auditoria.usuario_id,
            self.operador.pk
        )


    def test_inativacao_atualiza_agrupamentos(self):

        self.autenticar()

        resposta = self.client.delete(
            self.url_cliente_a
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.cliente_a.refresh_from_db()

        self.assertFalse(
            self.cliente_a.ativo
        )

        resposta_bairros = self.client.get(
            self.url_bairros
        )

        resposta_vendedores = self.client.get(
            self.url_agrupamento_vendedores
        )

        self.assertEqual(
            resposta_bairros.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta_vendedores.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta_bairros.data["total_clientes"],
            1
        )

        self.assertEqual(
            resposta_vendedores.data["total_clientes"],
            1
        )

        self.assertTrue(
            AuditoriaAPI.objects.filter(
                entidade="Cliente",
                identificador_registro=(
                    self.cliente_a.pk
                ),
                operacao="INATIVACAO"
            ).exists()
        )


    def test_operacao_negada_nao_altera_banco(self):

        usuario = User.objects.create_user(
            username="consulta_integracao",
            password="SenhaTeste123!"
        )

        token = Token.objects.create(
            user=usuario
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Token {token.key}"
            )
        )

        nome_original = (
            self.cliente_a.razao_social
        )

        resposta = self.client.patch(
            self.url_cliente_a,
            {
                "razao_social": (
                    "Alteracao Indevida"
                )
            },
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.cliente_a.refresh_from_db()

        self.assertEqual(
            self.cliente_a.razao_social,
            nome_original
        )

        self.assertEqual(
            AuditoriaAPI.objects.count(),
            0
        )


    def test_comando_validar_sistema(self):

        saida = StringIO()

        call_command(
            "validar_sistema",
            stdout=saida,
            no_color=True
        )

        resultado = saida.getvalue()

        self.assertIn(
            "Total de clientes: 3",
            resultado
        )

        self.assertIn(
            "Clientes ativos: 2",
            resultado
        )

        self.assertIn(
            "Clientes inativos: 1",
            resultado
        )

        self.assertIn(
            "Validacoes do banco concluidas "
            "sem falhas.",
            resultado
        )
