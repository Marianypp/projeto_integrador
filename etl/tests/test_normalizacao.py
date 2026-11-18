
import unittest

from etl.normalizacao import (
    normalizar_cnpj,
    normalizar_telefone,
    normalizar_data,
    normalizar_bairro,
    normalizar_cep,
    comparar_bairros
)


class TesteNormalizacao(unittest.TestCase):

    # ==========================
    # TESTES DE CNPJ
    # ==========================

    def test_cnpj_com_mascara(self):
        self.assertEqual(
            normalizar_cnpj("82.278.248/9638-34"),
            "82278248963834"
        )

    def test_cnpj_sem_mascara(self):
        self.assertEqual(
            normalizar_cnpj("82278248963834"),
            "82278248963834"
        )

    def test_cnpj_invalido(self):
        self.assertIsNone(
            normalizar_cnpj("12345")
        )

    def test_cnpj_vazio(self):
        self.assertIsNone(
            normalizar_cnpj("")
        )

    # ==========================
    # TESTES DE TELEFONE
    # ==========================

    def test_telefone_com_ddi(self):
        self.assertEqual(
            normalizar_telefone("+55 61 95386-2084"),
            "61953862084"
        )

    def test_telefone_fixo(self):
        self.assertEqual(
            normalizar_telefone("(61) 3491-1634"),
            "6134911634"
        )

    def test_telefone_invalido(self):
        self.assertIsNone(
            normalizar_telefone("123")
        )

    # ==========================
    # TESTES DE DATA
    # ==========================

    def test_data_brasileira(self):
        self.assertEqual(
            normalizar_data("18/08/2022"),
            "2022-08-18"
        )

    def test_data_iso(self):
        self.assertEqual(
            normalizar_data("2022-08-18"),
            "2022-08-18"
        )

    def test_data_ingles(self):
        self.assertEqual(
            normalizar_data("Aug 18, 2022"),
            "2022-08-18"
        )

    def test_data_invalida(self):
        self.assertIsNone(
            normalizar_data("31/02/2022")
        )

    # ==========================
    # TESTES DE BAIRRO
    # ==========================

    def test_bairro_sem_acento(self):
        self.assertEqual(
            normalizar_bairro("aguas claras"),
            "Águas Claras"
        )

    def test_bairro_abreviado(self):
        self.assertEqual(
            normalizar_bairro("Vte Pires"),
            "Vicente Pires"
        )

    def test_bairro_subdivisao(self):
        self.assertEqual(
            normalizar_bairro("Guará II"),
            "Guará II"
        )

    def test_bairro_desconhecido(self):
        self.assertIsNone(
            normalizar_bairro("Bairro desconhecido")
        )

    # ==========================
    # TESTES DE CEP
    # ==========================

    def test_cep_com_mascara(self):
        self.assertEqual(
            normalizar_cep("71926-750"),
            "71926750"
        )

    def test_cep_zerado(self):
        self.assertIsNone(
            normalizar_cep("00000-000")
        )

    def test_cep_com_letras(self):
        self.assertIsNone(
            normalizar_cep("ABC71926750")
        )

    def test_cep_vazio(self):
        self.assertIsNone(
            normalizar_cep("")
        )

    # ==========================
    # COMPARAÇÃO GEOGRÁFICA
    # ==========================

    def test_bairros_compativeis(self):
        self.assertEqual(
            comparar_bairros(
                "Águas Claras",
                "Aguas claras"
            ),
            "compativel"
        )

    def test_bairros_divergentes(self):
        self.assertEqual(
            comparar_bairros(
                "Águas Claras",
                "Taguatinga"
            ),
            "divergente"
        )

    def test_bairros_subdivisoes(self):
        self.assertEqual(
            comparar_bairros(
                "Guará I",
                "Guará II"
            ),
            "revisao_subdivisao"
        )


if __name__ == "__main__":
    unittest.main()
