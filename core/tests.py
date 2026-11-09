from django.test import TestCase
from .normalizacao import formatar_celular, formatar_fixo

class TesteFormatacaoTelefone(TestCase):
    def test_formatar_celular(self):
        telefone = "61987654321"
        resultado = formatar_celular(telefone)
        self.assertEqual(resultado, "(61) 98765-4321")

    def test_celular_invalido(self):
        telefone = "12345678"

        with self.assertRaises(ValueError):
            formatar_celular(telefone)

class TesteFormatacaoFixo(TestCase):
    def test_formatar_fixo(self):
        telefone = "6132345678"
        resultado = formatar_fixo(telefone)
        self.assertEqual(resultado, "(61) 3234-5678")

    def test_fixo_invalido(self):
        telefone = "1234567"

        with self.assertRaises(ValueError):
            formatar_fixo(telefone)

    def test_celular_com_letras(self):
        telefone = "61A987654321"

        with self.assertRaises(ValueError):
            formatar_celular(telefone)

    def test_fixo_com_letras(self):
        telefone = "61B32345678"

        with self.assertRaises(ValueError):
            formatar_fixo(telefone)

  