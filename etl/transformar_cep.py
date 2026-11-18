from normalizacao import comparar_bairros
from pathlib import Path
import pandas as pd

from normalizacao import normalizar_cep
from cache_cep import carregar_cache, consultar_com_cache


BASE_DIR = Path(__file__).resolve().parent.parent

CAMINHO_CSV = (
    BASE_DIR
    / "dados"
    / "tratados"
    / "clientes_bairros_tratados.csv"
)

# Lê o CSV
df = pd.read_csv(
    CAMINHO_CSV,
    sep=";",
    encoding="utf-8-sig",
    dtype=str,
    keep_default_na=False
)

# Normaliza os CEPs
df["cep_normalizado"] = (
    df["cep"].apply(normalizar_cep)
)

# Carrega o cache
cache = carregar_cache()

# Lista de resultados
resultados = []

for indice, cliente in df.iterrows():

    cep = cliente["cep_normalizado"]

    if pd.isna(cep):
        resultado = {
            "status": "cep_invalido_ou_ausente",
            "dados": None
        }
    else:
        resultado = consultar_com_cache(cep, cache)

    dados = resultado["dados"] or {}

    resultados.append({
        "status_consulta_cep": resultado["status"],
        "bairro_viacep": dados.get("bairro", ""),
        "cidade_viacep": dados.get("localidade", ""),
        "uf_viacep": dados.get("uf", "")
    })

# Acrescenta as informações ao DataFrame
df_resultados = pd.DataFrame(resultados)

df = pd.concat(
    [df, df_resultados],
    axis=1
)

print("\n=== RESULTADO DOS CEPS ===")

print(
    df[
        [
            "id_cliente",
            "cep_normalizado",
            "status_consulta_cep",
            "bairro_viacep"
        ]
    ].to_string(index=False)
)

print("\n=== RESUMO ===")
print(df["status_consulta_cep"].value_counts())


# Compara o bairro normalizado com a ViaCEP
df["comparacao_bairro_cep"] = df.apply(
    lambda cliente: (
        comparar_bairros(
            cliente["bairro_normalizado"],
            cliente["bairro_viacep"]
        )
        if cliente["status_consulta_cep"] == "encontrado"
        else "sem_comparacao"
    ),
    axis=1
)

print("\n=== COMPARAÇÃO BAIRRO X CEP ===")

print(
    df[
        [
            "id_cliente",
            "bairro_normalizado",
            "bairro_viacep",
            "comparacao_bairro_cep"
        ]
    ].to_string(index=False)
)

print("\n=== RESUMO DAS COMPARAÇÕES ===")
print(df["comparacao_bairro_cep"].value_counts())


auditoria = []

for indice, cliente in df.iterrows():

    original = cliente["cep"]
    tratado = cliente["cep_normalizado"]
    status = cliente["status_consulta_cep"]
    comparacao = cliente["comparacao_bairro_cep"]

    # Auditoria da normalização do CEP
    if pd.isna(tratado):
        criterio = "CEP ausente ou formato inválido"

    elif original != tratado:
        criterio = "Remoção de máscara do CEP"

    else:
        criterio = None

    if criterio:
        auditoria.append({
            "id_cliente": cliente["id_cliente"],
            "campo": "cep",
            "valor_original": original,
            "valor_tratado": (
                "" if pd.isna(tratado) else tratado
            ),
            "criterio": criterio
        })

    # Auditoria das consultas e divergências
    if status == "erro_consulta":
        criterio_geo = "Falha técnica na consulta ViaCEP"

    elif status == "nao_encontrado":
        criterio_geo = "CEP não encontrado na ViaCEP"

    elif comparacao in (
        "divergente",
        "revisao_manual",
        "revisao_subdivisao",
        "bairro_informado_ausente",
        "bairro_api_ausente"
    ):
        criterio_geo = (
            f"Revisão geográfica necessária: {comparacao}"
        )

    else:
        criterio_geo = None

    if criterio_geo:
        auditoria.append({
            "id_cliente": cliente["id_cliente"],
            "campo": "bairro_normalizado",
            "valor_original": cliente["bairro_normalizado"] or "",
            "valor_tratado": cliente["bairro_viacep"],
            "criterio": criterio_geo
        })

df_auditoria = pd.DataFrame(
    auditoria,
    columns=[
        "id_cliente",
        "campo",
        "valor_original",
        "valor_tratado",
        "criterio"
    ]
)

print("\n=== AUDITORIA DOS CEPS ===")
print(df_auditoria)


PASTA_TRATADOS = BASE_DIR / "dados" / "tratados"
PASTA_RELATORIOS = BASE_DIR / "relatorios"

PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)
PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)

# Salva a base enriquecida
df.to_csv(
    PASTA_TRATADOS / "clientes_ceps_tratados.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# Salva a auditoria
df_auditoria.to_csv(
    PASTA_RELATORIOS / "auditoria_ceps.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# Salva os casos para revisão
pendentes = df[
    (df["status_consulta_cep"] != "encontrado")
    |
    (df["comparacao_bairro_cep"] != "compativel")
]

pendentes.to_csv(
    PASTA_RELATORIOS / "revisao_geografica.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivos gerados com sucesso!")

