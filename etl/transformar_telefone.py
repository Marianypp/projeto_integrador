
from pathlib import Path
import pandas as pd

from normalizacao import normalizar_telefone

# Localiza a pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivo produzido na Aula 3
CAMINHO_CSV = (
    BASE_DIR
    / "dados"
    / "tratados"
    / "clientes_cnpj_tratado.csv"
)

# Leitura do arquivo
df = pd.read_csv(
    CAMINHO_CSV,
    sep=";",
    encoding="utf-8-sig",
    dtype=str,
    keep_default_na=False
)

# Normaliza os telefones
df["telefone_normalizado"] = (
    df["telefone"].apply(normalizar_telefone)
)

# Exibe os resultados
print("\n=== TELEFONES NORMALIZADOS ===")

print(
    df[
        [
            "id_cliente",
            "telefone",
            "telefone_normalizado"
        ]
    ].to_string(index=False)
)

# Verifica os telefones não normalizados
invalidos = df[df["telefone_normalizado"].isna()]

print("\n=== RESUMO ===")
print(f"Total de clientes: {len(df)}")
print(f"Telefones para revisão: {len(invalidos)}")


# Lista de auditoria
auditoria = []

# Percorre os registros
for indice, cliente in df.iterrows():

    original = cliente["telefone"]
    tratado = cliente["telefone_normalizado"]

    if pd.isna(tratado):
        criterio = "Formato inválido - revisão necessária"

    elif original != tratado:
        criterio = "Remoção de máscara e DDI quando presente"

    else:
        continue

    auditoria.append({
        "id_cliente": cliente["id_cliente"],
        "campo": "telefone",
        "valor_original": original,
        "valor_tratado": (
            "" if pd.isna(tratado) else tratado
        ),
        "criterio": criterio
    })

# Cria a tabela de auditoria
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

print("\n=== AUDITORIA DOS TELEFONES ===")
print(df_auditoria)


# Define as pastas de saída
PASTA_TRATADOS = BASE_DIR / "dados" / "tratados"
PASTA_RELATORIOS = BASE_DIR / "relatorios"

PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)
PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)

# Salva os clientes com CNPJ e telefone normalizados
df.to_csv(
    PASTA_TRATADOS / "clientes_cnpj_telefone_tratados.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# Salva a auditoria dos telefones
df_auditoria.to_csv(
    PASTA_RELATORIOS / "auditoria_telefone.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivos salvos com sucesso!")
