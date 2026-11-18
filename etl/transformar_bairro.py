
from pathlib import Path
import pandas as pd

from normalizacao import normalizar_bairro

# Localiza a pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivo tratado na Aula 5
CAMINHO_CSV = (
    BASE_DIR
    / "dados"
    / "tratados"
    / "clientes_cnpj_telefone_data_tratados.csv"
)

# Lê o CSV
df = pd.read_csv(
    CAMINHO_CSV,
    sep=";",
    encoding="utf-8-sig",
    dtype=str,
    keep_default_na=False
)

# Aplica a normalização
df["bairro_normalizado"] = (
    df["bairro_informado"].apply(normalizar_bairro)
)

# Exibe os resultados
print("\n=== BAIRROS NORMALIZADOS ===")

print(
    df[
        [
            "id_cliente",
            "bairro_informado",
            "bairro_normalizado"
        ]
    ].to_string(index=False)
)

# Identifica os registros sem bairro normalizado
bairros_pendentes = df[
    df["bairro_normalizado"].isna()
]

print("\n=== RESUMO ===")
print(f"Total de clientes: {len(df)}")
print(
    f"Bairros normalizados: "
    f"{df['bairro_normalizado'].notna().sum()}"
)
print(f"Bairros para revisão: {len(bairros_pendentes)}")

print("\n=== AGRUPAMENTO POR BAIRRO ===")
print(df["bairro_normalizado"].value_counts(dropna=False))


# Lista de auditoria
auditoria = []

for indice, cliente in df.iterrows():

    original = cliente["bairro_informado"]
    tratado = cliente["bairro_normalizado"]

    if pd.isna(tratado):
        criterio = "Bairro ausente ou desconhecido - revisão necessária"

    elif original != tratado:
        criterio = "Normalização por dicionário de equivalências"

    else:
        continue

    auditoria.append({
        "id_cliente": cliente["id_cliente"],
        "campo": "bairro_informado",
        "valor_original": original,
        "valor_tratado": (
            "" if pd.isna(tratado) else tratado
        ),
        "criterio": criterio
    })

# Cria o DataFrame de auditoria
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

print("\n=== AUDITORIA DOS BAIRROS ===")
print(df_auditoria)

print(
    f"\nTotal de registros de auditoria: "
    f"{len(df_auditoria)}"
)


# Pastas de saída
PASTA_TRATADOS = BASE_DIR / "dados" / "tratados"
PASTA_RELATORIOS = BASE_DIR / "relatorios"

PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)
PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)

# Salva os clientes tratados
df.to_csv(
    PASTA_TRATADOS / "clientes_bairros_tratados.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# Salva a auditoria
df_auditoria.to_csv(
    PASTA_RELATORIOS / "auditoria_bairros.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivos salvos com sucesso!")
