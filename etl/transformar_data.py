
from pathlib import Path
import pandas as pd

from normalizacao import normalizar_data

# Localiza a pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivo gerado na Aula 4
CAMINHO_CSV = (
    BASE_DIR
    / "dados"
    / "tratados"
    / "clientes_cnpj_telefone_tratados.csv"
)

# Lê os dados
df = pd.read_csv(
    CAMINHO_CSV,
    sep=";",
    encoding="utf-8-sig",
    dtype=str,
    keep_default_na=False
)

# Cria a coluna de datas normalizadas
df["data_cadastro_normalizado"] = (
    df["data_cadastro"].apply(normalizar_data)
)

# Exibe os resultados
print("\n=== DATAS NORMALIZADAS ===")

print(
    df[
        [
            "id_cliente",
            "data_cadastro",
            "data_cadastro_normalizado"
        ]
    ].to_string(index=False)
)

# Identifica datas que não puderam ser convertidas
datas_invalidas = df[
    df["data_cadastro_normalizado"].isna()
]

print("\n=== RESUMO ===")
print(f"Total de clientes: {len(df)}")
print(
    f"Datas normalizadas: "
    f"{df['data_cadastro_normalizado'].notna().sum()}"
)
print(f"Datas para revisão: {len(datas_invalidas)}")


# Lista que armazenará a auditoria
auditoria = []

# Percorre os clientes
for indice, cliente in df.iterrows():

    original = cliente["data_cadastro"]
    tratado = cliente["data_cadastro_normalizado"]

    if pd.isna(tratado):
        criterio = "Data inválida - revisão necessária"

    elif original != tratado:
        criterio = "Conversão para o padrão ISO 8601"

    else:
        continue

    # Registra a alteração
    auditoria.append({
        "id_cliente": cliente["id_cliente"],
        "campo": "data_cadastro",
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

print("\n=== AUDITORIA DAS DATAS ===")
print(df_auditoria)

print(
    f"\nRegistros de auditoria: {len(df_auditoria)}"
)


# Pastas de saída
PASTA_TRATADOS = BASE_DIR / "dados" / "tratados"
PASTA_RELATORIOS = BASE_DIR / "relatorios"

PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)
PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)

# Salva os clientes tratados
df.to_csv(
    PASTA_TRATADOS / "clientes_cnpj_telefone_data_tratados.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# Salva a auditoria das datas
df_auditoria.to_csv(
    PASTA_RELATORIOS / "auditoria_data.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivos salvos com sucesso!")
