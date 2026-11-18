
import unittest
from unittest.mock import patch

from normalizacao import normalizar_cep
from consulta_cep import consultar_cep


class TesteCEP(unittest.TestCase):

    def test_cep_com_mascara(self):
        self.assertEqual(
            normalizar_cep("71926-750"),
            "71926750"
        )

    def test_cep_zerado(self):
        self.assertIsNone(
            normalizar_cep("00000-000")
        )

    def test_cep_vazio(self):
        self.assertIsNone(
            normalizar_cep("")
        )

    @patch("consulta_cep.requests.get")
    def test_consulta_simulada(self, mock_get):

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
            resultado["dados"]["bairro"],
            "Águas Claras"
        )


if __name__ == "__main__":
    unittest.main()
