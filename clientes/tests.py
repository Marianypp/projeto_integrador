
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

