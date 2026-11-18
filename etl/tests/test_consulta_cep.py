
import unittest
import requests

from unittest.mock import patch
from etl.consulta_cep import consultar_cep


class TesteConsultaCEP(unittest.TestCase):

    @patch("etl.consulta_cep.requests.get")
    def test_cep_encontrado(self, mock_get):

        mock_get.return_value.json.return_value = {
            "cep": "71926-750",
            "bairro": "Águas Claras",
            "localidade": "Brasília",
            "uf": "DF"
        }

        resultado = consultar_cep("71926750")

        self.assertEqual(
            resultado["status"],
            "encontrado"
        )

        self.assertEqual(
            resultado["dados"]["uf"],
            "DF"
        )

    @patch("etl.consulta_cep.requests.get")
    def test_cep_nao_encontrado(self, mock_get):

        mock_get.return_value.json.return_value = {
            "erro": True
        }

        resultado = consultar_cep("12345678")

        self.assertEqual(
            resultado["status"],
            "nao_encontrado"
        )

    @patch("etl.consulta_cep.requests.get")
    def test_timeout(self, mock_get):

        mock_get.side_effect = requests.Timeout(
            "Tempo de espera excedido"
        )

        resultado = consultar_cep("71926750")

        self.assertEqual(
            resultado["status"],
            "erro_consulta"
        )

    @patch("etl.consulta_cep.requests.get")
    def test_erro_http(self, mock_get):

        mock_get.return_value.raise_for_status.side_effect = (
            requests.HTTPError("Erro HTTP 500")
        )

        resultado = consultar_cep("71926750")

        self.assertEqual(
            resultado["status"],
            "erro_consulta"
        )

    @patch("etl.consulta_cep.requests.get")
    def test_json_invalido(self, mock_get):

        mock_get.return_value.json.side_effect = (
            ValueError("JSON inválido")
        )

        resultado = consultar_cep("71926750")

        self.assertEqual(
            resultado["status"],
            "erro_consulta"
        )


if __name__ == "__main__":
    unittest.main()
