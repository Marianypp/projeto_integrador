
import requests


def consultar_cep(cep):
    # Monta a URL da consulta
    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        # Faz a requisição HTTP
        resposta = requests.get(
            url,
            timeout=10
        )

        # Verifica erros HTTP
        resposta.raise_for_status()

        # Converte a resposta JSON em dicionário
        dados = resposta.json()

        # Verifica se o CEP não foi encontrado
        if dados.get("erro"):
            return {
                "status": "nao_encontrado",
                "dados": None
            }

        return {
            "status": "encontrado",
            "dados": {
                "cep": dados.get("cep", ""),
                "bairro": dados.get("bairro", ""),
                "localidade": dados.get("localidade", ""),
                "uf": dados.get("uf", "")
            }
        }

    except (requests.RequestException, ValueError) as erro:
        print(f"Erro ao consultar {cep}: {erro}")

        return {
            "status": "erro_consulta",
            "dados": None
        }
