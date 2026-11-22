from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from django.test import TestCase
from django.db.models.deletion import ProtectedError

from .models import Cliente, Vendedor, Auditoria


class TesteBancoDados(TestCase):

    def setUp(self):

        self.vendedor = Vendedor.objects.create(
            nome="Vendedor de Teste"
        )

        self.cliente = Cliente.objects.create(
            id_cliente="TEST001",
            razao_social="Empresa de Teste",
            cnpj="12345678000199",
            telefone="61999999999",
            email="teste@example.com",
            bairro="Águas Claras",
            cep="71926750",
            cidade="Brasília",
            uf="DF",
            vendedor=self.vendedor
        )

    def test_criar_cliente(self):

        self.assertEqual(
            Cliente.objects.count(),
            1
        )

    def test_relacionamento_vendedor(self):

        self.assertEqual(
            self.cliente.vendedor,
            self.vendedor
        )

    def test_proteger_vendedor(self):

        with self.assertRaises(ProtectedError):

            self.vendedor.delete()

    def test_atualizar_cliente_sem_duplicar(self):

        Cliente.objects.update_or_create(
            id_cliente="TEST001",
            defaults={
                "razao_social": "Empresa Atualizada"
            }
        )

        self.assertEqual(
            Cliente.objects.count(),
            1
        )

        cliente = Cliente.objects.get(
            id_cliente="TEST001"
        )

        self.assertEqual(
            cliente.razao_social,
            "Empresa Atualizada"
        )

    def test_criar_auditoria(self):

        Auditoria.objects.create(
            cliente=self.cliente,
            campo="bairro",
            valor_original="aguas claras",
            valor_tratado="Águas Claras",
            criterio="Normalização textual",
            fonte_referencia="Regra interna",
            status="alterado"
        )

        self.assertEqual(
            self.cliente.auditorias.count(),
            1
        )

    def test_preservar_cliente_auditado(self):

        Auditoria.objects.create(
            cliente=self.cliente,
            campo="bairro",
            criterio="Normalização",
            fonte_referencia="Regra interna",
            status="alterado"
        )

        with self.assertRaises(ProtectedError):

            self.cliente.delete()


class TesteAPIClientes(APITestCase):

    def setUp(self):

        self.vendedor = Vendedor.objects.create(
            nome="Vendedor de Teste"
        )

        self.cliente = Cliente.objects.create(
            id_cliente="TEST001",
            razao_social="Empresa Teste LTDA",
            cnpj="12345678000199",
            telefone="61999999999",
            email="teste@example.com",
            bairro="Águas Claras",
            cep="71926750",
            cidade="Brasília",
            uf="DF",
            vendedor=self.vendedor
        )

    def test_status_api(self):

        url = reverse("status-api")

        resposta = self.client.get(url)

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["status"],
            "online"
        )

    def test_listar_clientes(self):

        url = reverse("listar-clientes")

        resposta = self.client.get(url)

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(resposta.data),
            1
        )

        self.assertEqual(
            resposta.data[0]["id_cliente"],
            "TEST001"
        )

    def test_consultar_cliente(self):

        url = reverse(
            "consultar-cliente",
            kwargs={"id_cliente": "TEST001"}
        )

        resposta = self.client.get(url)

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["razao_social"],
            "Empresa Teste LTDA"
        )

    def test_cliente_inexistente(self):

        url = reverse(
            "consultar-cliente",
            kwargs={"id_cliente": "INEXISTENTE"}
        )

        resposta = self.client.get(url)

        self.assertEqual(
            resposta.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_post_nao_permitido(self):

        url = reverse("listar-clientes")

        # Autentica para testar especificamente
        # se o método POST está implementado.
        from django.contrib.auth import get_user_model

        usuario = get_user_model().objects.create_user(
            username="usuario_teste",
            password="senha_apenas_para_teste"
        )

        self.client.force_authenticate(
            user=usuario
        )

        resposta = self.client.post(
            url,
            {},
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_nome_vendedor(self):

        url = reverse(
            "consultar-cliente",
            kwargs={"id_cliente": "TEST001"}
        )

        resposta = self.client.get(url)

        self.assertEqual(
            resposta.data["vendedor_nome"],
            "Vendedor de Teste"
        )
