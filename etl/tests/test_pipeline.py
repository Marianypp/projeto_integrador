
import unittest

from unittest.mock import patch

from etl.pipeline import (
    extrair_dados,
    transformar_dados,
    enriquecer_dados,
    gerar_auditoria
)


class TestePipeline(unittest.TestCase):

    def setUp(self):

        self.df_original = extrair_dados()

        self.df_tratado = transformar_dados(
            self.df_original
        )

    def test_quantidade_clientes(self):

        self.assertEqual(
            len(self.df_original),
            47
        )

    def test_preservar_clientes(self):

        self.assertEqual(
            len(self.df_original),
            len(self.df_tratado)
        )

        self.assertEqual(
            self.df_original["id_cliente"].tolist(),
            self.df_tratado["id_cliente"].tolist()
        )

    def test_ids_unicos(self):

        self.assertFalse(
            self.df_tratado["id_cliente"]
            .duplicated()
            .any()
        )

    def test_preservar_dados_originais(self):

        for coluna in self.df_original.columns:

            self.assertEqual(
                self.df_original[coluna].tolist(),
                self.df_tratado[coluna].tolist()
            )

    @patch(
        "etl.pipeline.carregar_cache",
        return_value={}
    )
    @patch("etl.pipeline.consultar_com_cache")
    def test_pipeline_sem_internet(
        self,
        mock_consulta,
        mock_cache
    ):

        df = enriquecer_dados(
            self.df_tratado,
            consultar_ceps=False
        )

        self.assertEqual(len(df), 47)

        mock_consulta.assert_not_called()

    @patch(
        "etl.pipeline.carregar_cache",
        return_value={}
    )
    def test_geracao_auditoria(self, mock_cache):

        df = enriquecer_dados(
            self.df_tratado,
            consultar_ceps=False
        )

        auditoria = gerar_auditoria(df)

        self.assertFalse(auditoria.empty)

        self.assertIn(
            "valor_original",
            auditoria.columns
        )

        self.assertIn(
            "valor_tratado",
            auditoria.columns
        )

        self.assertIn(
            "criterio",
            auditoria.columns
        )

        self.assertTrue(
            auditoria["criterio"]
            .str.strip()
            .ne("")
            .all()
        )


if __name__ == "__main__":
    unittest.main()
