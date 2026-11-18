
import json
from pathlib import Path

from etl.consulta_cep import consultar_cep


BASE_DIR = Path(__file__).resolve().parent.parent

CAMINHO_CACHE = (
    BASE_DIR / "dados" / "cache_ceps.json"
)


def carregar_cache():
    if CAMINHO_CACHE.exists():
        with open(CAMINHO_CACHE, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    return {}


def salvar_cache(cache):
    CAMINHO_CACHE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(CAMINHO_CACHE, "w", encoding="utf-8") as arquivo:
        json.dump(
            cache,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def consultar_com_cache(cep, cache):
    # Se já consultamos o CEP, usamos o cache
    if cep in cache:
        return cache[cep]

    # Caso contrário, consultamos a API
    resultado = consultar_cep(cep)

    # Armazena apenas respostas conclusivas
    if resultado["status"] in (
        "encontrado",
        "nao_encontrado"
    ):
        cache[cep] = resultado
        salvar_cache(cache)

    return resultado
