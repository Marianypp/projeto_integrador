
import unittest

from unittest.mock import patch
from etl.cache_cep import consultar_com_cache


class TesteCache(unittest.TestCase):

    @patch("etl.cache_cep.consultar_cep")
    def test_utilizar_cache(self, mock_consulta):

        cache = {
            "71926750": {
                "status": "encontrado",
                "dados": {
                    "bairro": "Águas Claras"
                }
            }
        }

        resultado = consultar_com_cache(
            "71926750",
            cache
        )

        self.assertEqual(
            resultado["status"],
            "encontrado"
        )

        mock_consulta.assert_not_called()

    @patch("etl.cache_cep.salvar_cache")
    @patch("etl.cache_cep.consultar_cep")
    def test_salvar_nova_consulta(
        self,
        mock_consulta,
        mock_salvar
    ):

        cache = {}

        mock_consulta.return_value = {
            "status": "encontrado",
            "dados": {
                "bairro": "Águas Claras"
            }
        }

        consultar_com_cache(
            "71926750",
            cache
        )

        self.assertIn("71926750", cache)

        mock_consulta.assert_called_once_with(
            "71926750"
        )

        mock_salvar.assert_called_once()

    @patch("etl.cache_cep.salvar_cache")
    @patch("etl.cache_cep.consultar_cep")
    def test_nao_salvar_erro(
        self,
        mock_consulta,
        mock_salvar
    ):

        cache = {}

        mock_consulta.return_value = {
            "status": "erro_consulta",
            "dados": None
        }

        consultar_com_cache(
            "71926750",
            cache
        )

        self.assertNotIn("71926750", cache)

        mock_salvar.assert_not_called()


if __name__ == "__main__":
    unittest.main()
