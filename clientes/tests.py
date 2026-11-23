from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from django.test import TestCase
from django.db.models.deletion import ProtectedError

from .models import Cliente, Vendedor, Auditoria

from django.contrib.auth import get_user_model


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

        url = reverse("cliente-list")

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
            "cliente-detail",
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
            "cliente-detail",
            kwargs={"id_cliente": "INEXISTENTE"}
        )

        resposta = self.client.get(url)

        self.assertEqual(
            resposta.status_code,
            status.HTTP_404_NOT_FOUND
        )

    
    def test_post_sem_autenticacao(self):

        url = reverse("cliente-list")

        resposta = self.client.post(
            url,
            {},
            format="json"
        )

        self.assertIn(
            resposta.status_code,
            [401, 403]
        )


    def test_nome_vendedor(self):

        url = reverse(
            "cliente-detail",
            kwargs={"id_cliente": "TEST001"}
        )

        resposta = self.client.get(url)

        self.assertEqual(
            resposta.data["vendedor_nome"],
            "Vendedor de Teste"
        )


class TesteCRUDClientes(APITestCase):

    def setUp(self):

        self.usuario = (
            get_user_model().objects.create_user(
                username="teste_crud",
                password="senha_de_teste"
            )
        )

        self.vendedor = Vendedor.objects.create(
            nome="Vendedor Teste"
        )

        self.cliente = Cliente.objects.create(
            id_cliente="TEST001",
            razao_social="Empresa Teste",
            cnpj="12345678000199",
            telefone="61999999999",
            email="teste@example.com",
            bairro="Águas Claras",
            cep="71926750",
            cidade="Brasília",
            uf="DF",
            vendedor=self.vendedor
        )

        self.url_lista = reverse(
            "cliente-list"
        )

        self.url_detalhe = reverse(
            "cliente-detail",
            kwargs={
                "id_cliente": "TEST001"
            }
        )

    def autenticar(self):

        self.client.force_authenticate(
            user=self.usuario
        )

    def test_listagem_publica(self):

        resposta = self.client.get(
            self.url_lista
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(resposta.data),
            1
        )

    def test_cadastro_sem_autenticacao(self):

        resposta = self.client.post(
            self.url_lista,
            {},
            format="json"
        )

        self.assertIn(
            resposta.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN
            ]
        )

    def test_cadastro_autenticado(self):

        self.autenticar()

        dados = {
            "id_cliente": "TEST002",
            "razao_social": "Nova Empresa",
            "cnpj": "98765432000199",
            "telefone": "(61) 98888-7777",
            "email": "nova@example.com",
            "bairro": "aguas claras",
            "cep": "71926-750",
            "cidade": "Brasília",
            "uf": "DF",
            "vendedor": self.vendedor.pk
        }

        resposta = self.client.post(
            self.url_lista,
            dados,
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Cliente.objects.filter(
                id_cliente="TEST002"
            ).exists()
        )

    def test_cnpj_invalido(self):

        self.autenticar()

        dados = {
            "id_cliente": "TEST003",
            "razao_social": "Empresa Inválida",
            "cnpj": "12345",
            "telefone": "61999999999",
            "email": "invalida@example.com",
            "bairro": "Águas Claras",
            "cep": "71926750",
            "cidade": "Brasília",
            "uf": "DF",
            "vendedor": self.vendedor.pk
        }

        resposta = self.client.post(
            self.url_lista,
            dados,
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "cnpj",
            resposta.data
        )

    def test_atualizacao_parcial(self):

        self.autenticar()

        resposta = self.client.patch(
            self.url_detalhe,
            {
                "telefone": "(61) 97777-6666"
            },
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.cliente.refresh_from_db()

        self.assertEqual(
            self.cliente.telefone,
            "61977776666"
        )

    def test_exclusao_logica(self):

        self.autenticar()

        resposta = self.client.delete(
            self.url_detalhe
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.cliente.refresh_from_db()

        self.assertFalse(
            self.cliente.ativo
        )

        self.assertTrue(
            Cliente.objects.filter(
                id_cliente="TEST001"
            ).exists()
        )

    def test_cliente_inativo_nao_aparece(self):

        self.cliente.ativo = False
        self.cliente.save()

        resposta = self.client.get(
            self.url_detalhe
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_404_NOT_FOUND
        )


class TesteCRUDVendedores(APITestCase):

    def setUp(self):

        self.usuario = (
            get_user_model().objects.create_user(
                username="teste_vendedor",
                password="senha_de_teste"
            )
        )

        self.vendedor = Vendedor.objects.create(
            nome="Vendedor Teste"
        )

        self.url_lista = reverse(
            "vendedor-list"
        )

        self.url_detalhe = reverse(
            "vendedor-detail",
            kwargs={"pk": self.vendedor.pk}
        )

    def autenticar(self):

        self.client.force_authenticate(
            user=self.usuario
        )

    def test_listar_vendedores(self):

        resposta = self.client.get(
            self.url_lista
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(resposta.data),
            1
        )

    def test_consultar_vendedor(self):

        resposta = self.client.get(
            self.url_detalhe
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["nome"],
            "Vendedor Teste"
        )

    def test_cadastro_autenticado(self):

        self.autenticar()

        resposta = self.client.post(
            self.url_lista,
            {"nome": "Novo Vendedor"},
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Vendedor.objects.filter(
                nome="Novo Vendedor"
            ).exists()
        )

    def test_cadastro_sem_autenticacao(self):

        resposta = self.client.post(
            self.url_lista,
            {"nome": "Novo Vendedor"},
            format="json"
        )

        self.assertIn(
            resposta.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN
            ]
        )

    def test_nome_invalido(self):

        self.autenticar()

        resposta = self.client.post(
            self.url_lista,
            {"nome": "Jo"},
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_atualizar_vendedor(self):

        self.autenticar()

        resposta = self.client.patch(
            self.url_detalhe,
            {"nome": "Vendedor Atualizado"},
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.vendedor.refresh_from_db()

        self.assertEqual(
            self.vendedor.nome,
            "Vendedor Atualizado"
        )

    def test_excluir_sem_clientes(self):

        self.autenticar()

        resposta = self.client.delete(
            self.url_detalhe
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Vendedor.objects.filter(
                pk=self.vendedor.pk
            ).exists()
        )

    def test_impedir_exclusao_com_clientes(self):

        Cliente.objects.create(
            id_cliente="TEST001",
            razao_social="Empresa Teste",
            cnpj="12345678000199",
            telefone="61999999999",
            email="teste@example.com",
            bairro="Águas Claras",
            cep="71926750",
            cidade="Brasília",
            uf="DF",
            vendedor=self.vendedor
        )

        self.autenticar()

        resposta = self.client.delete(
            self.url_detalhe
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertTrue(
            Vendedor.objects.filter(
                pk=self.vendedor.pk
            ).exists()
        )

    def test_listar_clientes_do_vendedor(self):

        Cliente.objects.create(
            id_cliente="TEST002",
            razao_social="Empresa Exemplo",
            cnpj="98765432000199",
            telefone="61988887777",
            email="exemplo@example.com",
            bairro="Taguatinga",
            cep="72140010",
            cidade="Brasília",
            uf="DF",
            vendedor=self.vendedor
        )

        url = reverse(
            "vendedor-clientes",
            kwargs={"pk": self.vendedor.pk}
        )

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
            "TEST002"
        )
