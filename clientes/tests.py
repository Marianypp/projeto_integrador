from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from .models import Cliente, Vendedor, Auditoria, AuditoriaAPI
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from unittest.mock import patch


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

        print("\nERRO NO CADASTRO:")
        print(resposta.status_code)
        print(resposta.data)

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

        print("\nERRO NA ATUALIZAÇÃO:")
        print(resposta.status_code)
        print(resposta.data)

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


class TesteConsultasAgrupadas(APITestCase):

    def setUp(self):

        self.vendedor1 = Vendedor.objects.create(
            nome="Ana"
        )

        self.vendedor2 = Vendedor.objects.create(
            nome="Carlos"
        )

        self.vendedor3 = Vendedor.objects.create(
            nome="Marcos"
        )

        self.criar_cliente(
            "TEST001",
            "Empresa A",
            "Águas Claras",
            self.vendedor1
        )

        self.criar_cliente(
            "TEST002",
            "Empresa B",
            "Águas Claras",
            self.vendedor1
        )

        self.criar_cliente(
            "TEST003",
            "Empresa C",
            "Taguatinga",
            self.vendedor2
        )

        self.criar_cliente(
            "TEST004",
            "Empresa D",
            "Taguatinga",
            self.vendedor2,
            ativo=False
        )

        self.url_bairro = reverse(
            "clientes-por-bairro"
        )

        self.url_vendedor = reverse(
            "clientes-por-vendedor"
        )

    def criar_cliente(
        self,
        identificador,
        nome,
        bairro,
        vendedor,
        ativo=True
    ):

        return Cliente.objects.create(
            id_cliente=identificador,
            razao_social=nome,
            bairro=bairro,
            cidade="Brasília",
            uf="DF",
            vendedor=vendedor,
            ativo=ativo
        )

    def test_agrupamento_por_bairro(self):

        resposta = self.client.get(
            self.url_bairro
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["total_bairros"],
            2
        )

        self.assertEqual(
            resposta.data["total_clientes"],
            3
        )

        resultados = {
            item["bairro"]: item["total_clientes"]
            for item in resposta.data["resultados"]
        }

        self.assertEqual(
            resultados["Águas Claras"],
            2
        )

        self.assertEqual(
            resultados["Taguatinga"],
            1
        )

    def test_filtro_por_bairro(self):

        resposta = self.client.get(
            self.url_bairro,
            {"bairro": "Águas Claras"}
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["total_bairros"],
            1
        )

        self.assertEqual(
            resposta.data["total_clientes"],
            2
        )

    def test_agrupamento_por_vendedor(self):

        resposta = self.client.get(
            self.url_vendedor
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["total_vendedores"],
            3
        )

        self.assertEqual(
            resposta.data["total_clientes"],
            3
        )

        resultados = {
            item["nome"]: item["total_clientes"]
            for item in resposta.data["resultados"]
        }

        self.assertEqual(
            resultados["Ana"],
            2
        )

        self.assertEqual(
            resultados["Carlos"],
            1
        )

        self.assertEqual(
            resultados["Marcos"],
            0
        )

    def test_filtro_por_vendedor(self):

        resposta = self.client.get(
            self.url_vendedor,
            {"vendedor_id": self.vendedor1.pk}
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta.data["total_vendedores"],
            1
        )

        self.assertEqual(
            resposta.data["total_clientes"],
            2
        )

    def test_vendedor_id_invalido(self):

        resposta = self.client.get(
            self.url_vendedor,
            {"vendedor_id": "abc"}
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_consultas_sao_publicas(self):

        resposta_bairro = self.client.get(
            self.url_bairro
        )

        resposta_vendedor = self.client.get(
            self.url_vendedor
        )

        self.assertEqual(
            resposta_bairro.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resposta_vendedor.status_code,
            status.HTTP_200_OK
        )


class TesteAutenticacaoAPI(APITestCase):

    def setUp(self):

        self.usuario = User.objects.create_user(
            username="usuario_teste",
            password="SenhaTeste123!"
        )

        self.token = Token.objects.create(
            user=self.usuario
        )

        self.url_vendedores = reverse(
            "vendedor-list"
        )

        self.url_bairros = reverse(
            "clientes-por-bairro"
        )

    def test_consulta_publica_sem_token(self):

        resposta = self.client.get(
            self.url_vendedores
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

    def test_cadastro_sem_token(self):

        resposta = self.client.post(
            self.url_vendedores,
            {"nome": "Vendedor Sem Token"},
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_401_UNAUTHORIZED,
            resposta.data
        )

    def test_cadastro_com_token_valido(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Token {self.token.key}"
            )
        )

        resposta = self.client.post(
            self.url_vendedores,
            {"nome": "Vendedor Autenticado"},
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
            resposta.data
        )

        self.assertTrue(
            Vendedor.objects.filter(
                nome="Vendedor Autenticado"
            ).exists()
        )

    def test_token_invalido(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                "Token token_invalido"
            )
        )

        resposta = self.client.post(
            self.url_vendedores,
            {"nome": "Vendedor Inválido"},
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_401_UNAUTHORIZED,
            resposta.data
        )

    def test_consulta_agrupada_publica(self):

        resposta = self.client.get(
            self.url_bairros
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

    def test_atualizacao_sem_token(self):

        vendedor = Vendedor.objects.create(
            nome="Vendedor Original"
        )

        url_detalhe = reverse(
            "vendedor-detail",
            args=[vendedor.pk]
        )

        resposta = self.client.patch(
            url_detalhe,
            {"nome": "Nome Alterado"},
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_401_UNAUTHORIZED,
            resposta.data
        )

        vendedor.refresh_from_db()

        self.assertEqual(
            vendedor.nome,
            "Vendedor Original"
        )

    def test_exclusao_sem_token(self):

        vendedor = Vendedor.objects.create(
            nome="Vendedor Protegido"
        )

        url_detalhe = reverse(
            "vendedor-detail",
            args=[vendedor.pk]
        )

        resposta = self.client.delete(
            url_detalhe
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_401_UNAUTHORIZED,
            resposta.data
        )

        self.assertTrue(
            Vendedor.objects.filter(
                pk=vendedor.pk
            ).exists()
        )


class TesteDocumentacaoAPI(APITestCase):

    def test_schema_disponivel(self):

        resposta = self.client.get(
            reverse("schema")
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

    def test_swagger_disponivel(self):

        resposta = self.client.get(
            reverse("swagger-ui")
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

    def test_redoc_disponivel(self):

        resposta = self.client.get(
            reverse("redoc")
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

    def test_endpoints_presentes_no_schema(self):

        resposta = self.client.get(
            reverse("schema"),
            HTTP_ACCEPT="application/json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        esquema = resposta.json()

        rotas = esquema["paths"]

        self.assertIn(
            "/api/clientes/",
            rotas
        )

        self.assertIn(
            "/api/vendedores/",
            rotas
        )

        self.assertIn(
            "/api/consultas/clientes-por-bairro/",
            rotas
        )

        self.assertIn(
            "/api/consultas/clientes-por-vendedor/",
            rotas
        )

    def test_parametro_bairro_documentado(self):

        resposta = self.client.get(
            reverse("schema"),
            HTTP_ACCEPT="application/json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        esquema = resposta.json()

        parametros = esquema["paths"][
            "/api/consultas/clientes-por-bairro/"
        ]["get"]["parameters"]

        nomes = [
            parametro["name"]
            for parametro in parametros
        ]

        self.assertIn("bairro", nomes)

    def test_parametro_vendedor_documentado(self):

        resposta = self.client.get(
            reverse("schema"),
            HTTP_ACCEPT="application/json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        esquema = resposta.json()

        parametros = esquema["paths"][
            "/api/consultas/clientes-por-vendedor/"
        ]["get"]["parameters"]

        nomes = [
            parametro["name"]
            for parametro in parametros
        ]

        self.assertIn("vendedor_id", nomes)

    def test_autenticacao_documentada(self):

        resposta = self.client.get(
            reverse("schema"),
            HTTP_ACCEPT="application/json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

        esquema = resposta.json()

        mecanismos = esquema["components"][
            "securitySchemes"
        ]

        self.assertIn(
            "tokenAuth",
            mecanismos
        )


class TesteAuditoriaAPI(APITestCase):

    def setUp(self):

        self.usuario = User.objects.create_user(
            username="usuario_auditoria",
            password="SenhaTeste123!"
        )

        self.admin = User.objects.create_user(
            username="admin_auditoria",
            password="SenhaTeste123!",
            is_staff=True
        )

        self.vendedor = Vendedor.objects.create(
            nome="Vendedor Original"
        )

        self.cliente = Cliente.objects.create(
            id_cliente="AUD001",
            razao_social="Empresa Auditoria",
            telefone="61988887777",
            bairro="Águas Claras",
            cidade="Brasília",
            uf="DF",
            vendedor=self.vendedor,
            ativo=True
        )

        self.url_clientes = reverse(
            "cliente-list"
        )

        self.url_cliente = reverse(
            "cliente-detail",
            args=[self.cliente.pk]
        )

        self.url_vendedores = reverse(
            "vendedor-list"
        )

        self.url_auditorias = reverse(
            "auditoria-list"
        )

    def test_auditoria_criacao_cliente(self):

        self.client.force_authenticate(
            user=self.usuario
        )

        resposta = self.client.post(
            self.url_clientes,
            {
                "id_cliente": "AUD002",
                "razao_social": "Empresa Nova",
                "telefone": "61977776666",
                "bairro": "Águas Claras",
                "cidade": "Brasília",
                "uf": "DF",
                "vendedor": self.vendedor.pk
            },
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
            resposta.data
        )

        auditoria = AuditoriaAPI.objects.get(
            entidade="Cliente",
            identificador_registro="AUD002"
        )

        self.assertEqual(
            auditoria.operacao,
            "CRIACAO"
        )

        self.assertEqual(
            auditoria.dados_anteriores,
            {}
        )

        self.assertEqual(
            auditoria.dados_posteriores[
                "id_cliente"
            ],
            "AUD002"
        )

        self.assertEqual(
            auditoria.usuario,
            self.usuario
        )

    def test_auditoria_atualizacao_cliente(self):

        self.client.force_authenticate(
            user=self.usuario
        )

        resposta = self.client.patch(
            self.url_cliente,
            {
                "telefone": "(61) 97777-6666"
            },
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
            resposta.data
        )

        auditoria = AuditoriaAPI.objects.get(
            entidade="Cliente",
            identificador_registro="AUD001"
        )

        self.assertEqual(
            auditoria.operacao,
            "ATUALIZACAO"
        )

        self.assertEqual(
            auditoria.dados_anteriores["telefone"],
            "61988887777"
        )

        self.assertEqual(
            auditoria.dados_posteriores["telefone"],
            "61977776666"
        )

        self.assertEqual(
            auditoria.campos_alterados,
            ["telefone"]
        )

        self.assertEqual(
            auditoria.usuario,
            self.usuario
        )

    def test_auditoria_inativacao_cliente(self):

        self.client.force_authenticate(
            user=self.usuario
        )

        resposta = self.client.delete(
            self.url_cliente
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT
        )

        auditoria = AuditoriaAPI.objects.get(
            entidade="Cliente",
            identificador_registro="AUD001"
        )

        self.assertEqual(
            auditoria.operacao,
            "INATIVACAO"
        )

        self.assertTrue(
            auditoria.dados_anteriores["ativo"]
        )

        self.assertFalse(
            auditoria.dados_posteriores["ativo"]
        )

        self.cliente.refresh_from_db()

        self.assertFalse(
            self.cliente.ativo
        )

    def test_auditoria_criacao_vendedor(self):

        self.client.force_authenticate(
            user=self.usuario
        )

        resposta = self.client.post(
            self.url_vendedores,
            {
                "nome": "Vendedor Novo"
            },
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
            resposta.data
        )

        auditoria = AuditoriaAPI.objects.get(
            entidade="Vendedor",
            operacao="CRIACAO"
        )

        self.assertEqual(
            auditoria.dados_posteriores["nome"],
            "Vendedor Novo"
        )

        self.assertEqual(
            auditoria.metodo_http,
            "POST"
        )

    def test_auditoria_atualizacao_vendedor(self):

        self.client.force_authenticate(
            user=self.usuario
        )

        url = reverse(
            "vendedor-detail",
            args=[self.vendedor.pk]
        )

        resposta = self.client.patch(
            url,
            {"nome": "Vendedor Alterado"},
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
            resposta.data
        )

        auditoria = AuditoriaAPI.objects.get(
            entidade="Vendedor",
            operacao="ATUALIZACAO"
        )

        self.assertEqual(
            auditoria.dados_anteriores["nome"],
            "Vendedor Original"
        )

        self.assertEqual(
            auditoria.dados_posteriores["nome"],
            "Vendedor Alterado"
        )

        self.assertEqual(
            auditoria.campos_alterados,
            ["nome"]
        )

    def test_auditoria_exclusao_vendedor(self):

        self.client.force_authenticate(
            user=self.usuario
        )

        vendedor = Vendedor.objects.create(
            nome="Vendedor Sem Clientes"
        )

        identificador = vendedor.pk

        url = reverse(
            "vendedor-detail",
            args=[identificador]
        )

        resposta = self.client.delete(url)

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT
        )

        auditoria = AuditoriaAPI.objects.get(
            entidade="Vendedor",
            operacao="EXCLUSAO"
        )

        self.assertEqual(
            auditoria.identificador_registro,
            str(identificador)
        )

        self.assertEqual(
            auditoria.dados_anteriores["nome"],
            "Vendedor Sem Clientes"
        )

        self.assertEqual(
            auditoria.dados_posteriores,
            {}
        )

        self.assertFalse(
            Vendedor.objects.filter(
                pk=identificador
            ).exists()
        )

    def test_exclusao_bloqueada_sem_auditoria(self):

        self.client.force_authenticate(
            user=self.usuario
        )

        url = reverse(
            "vendedor-detail",
            args=[self.vendedor.pk]
        )

        resposta = self.client.delete(url)

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            AuditoriaAPI.objects.count(),
            0
        )

    def test_atualizacao_sem_mudanca(self):

        self.client.force_authenticate(
            user=self.usuario
        )

        resposta = self.client.patch(
            self.url_cliente,
            {
                "telefone": "61988887777"
            },
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
            resposta.data
        )

        self.assertEqual(
            AuditoriaAPI.objects.count(),
            0
        )

    def test_auditoria_sem_autenticacao(self):

        resposta = self.client.get(
            self.url_auditorias
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_auditoria_usuario_comum(self):

        self.client.force_authenticate(
            user=self.usuario
        )

        resposta = self.client.get(
            self.url_auditorias
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_auditoria_administrador(self):

        self.client.force_authenticate(
            user=self.admin
        )

        resposta = self.client.get(
            self.url_auditorias
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK
        )

    def test_auditoria_nao_permite_cadastro(self):

        self.client.force_authenticate(
            user=self.admin
        )

        resposta = self.client.post(
            self.url_auditorias,
            {},
            format="json"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_falha_auditoria_desfaz_atualizacao(self):

        self.client.force_authenticate(
            user=self.usuario
        )

        with patch(
            "clientes.views.registrar_auditoria",
            side_effect=RuntimeError(
                "Falha simulada na auditoria"
            )
        ):

            with self.assertRaises(RuntimeError):

                self.client.patch(
                    self.url_cliente,
                    {
                        "telefone": "61977776666"
                    },
                    format="json"
                )

        self.cliente.refresh_from_db()

        self.assertEqual(
            self.cliente.telefone,
            "61988887777"
        )

        self.assertEqual(
            AuditoriaAPI.objects.count(),
            0
        )
