
import unittest

from pipeline import (
    extrair_dados,
    transformar_dados
)


class TestePipeline(unittest.TestCase):

    def test_quantidade_clientes(self):

        df = extrair_dados()

        self.assertEqual(len(df), 47)

    def test_normalizacao_preserva_clientes(self):

        df = extrair_dados()
        df_tratado = transformar_dados(df)

        self.assertEqual(
            len(df_tratado),
            len(df)
        )

    def test_colunas_normalizadas(self):

        df = extrair_dados()
        df_tratado = transformar_dados(df)

        colunas_esperadas = [
            "cnpj_normalizado",
            "telefone_normalizado",
            "data_cadastro_normalizado",
            "bairro_normalizado",
            "cep_normalizado"
        ]

        for coluna in colunas_esperadas:
            self.assertIn(
                coluna,
                df_tratado.columns
            )


if __name__ == "__main__":
    unittest.main()
