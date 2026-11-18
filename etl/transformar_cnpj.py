
from pathlib import Path
import pandas as pd

from normalizacao import normalizar_cnpj

# Localiza a pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho do CSV original
CAMINHO_CSV = (
    BASE_DIR
    / "dados"
    / "originais"
    / "clientes_distribuidora_vetor.csv"
)

# Lê os dados
df = pd.read_csv(
    CAMINHO_CSV,
    sep=";",
    encoding="utf-8-sig",
    dtype=str,
    keep_default_na=False
)

# Cria uma nova coluna com os CNPJs normalizados
df["cnpj_normalizado"] = df["cnpj"].apply(normalizar_cnpj)

# Mostra os resultados
print(df[["id_cliente", "cnpj", "cnpj_normalizado"]])


# Identifica os CNPJs que não passaram
# na verificação de 14 dígitos
cnpjs_invalidos = df[df["cnpj_normalizado"].isna()]

print("\n=== RESULTADO DA NORMALIZAÇÃO ===")

print(f"Total de clientes: {len(df)}")

print(
    f"CNPJs com 14 dígitos: "
    f"{df['cnpj_normalizado'].notna().sum()}"
)

print(
    f"CNPJs que precisam de revisão: "
    f"{len(cnpjs_invalidos)}"
)

if not cnpjs_invalidos.empty:
    print("\nRegistros que precisam de revisão:")
    print(cnpjs_invalidos[["id_cliente", "cnpj"]])


# Lista que armazenará os registros de auditoria
auditoria = []

# Percorre cada cliente
for indice, cliente in df.iterrows():

    cnpj_original = cliente["cnpj"]
    cnpj_tratado = cliente["cnpj_normalizado"]

    # Caso não seja possível normalizar
    if pd.isna(cnpj_tratado):
        criterio = "CNPJ sem 14 dígitos - revisão necessária"

    # Caso o CNPJ tenha sido modificado
    elif cnpj_original != cnpj_tratado:
        criterio = "Remoção de máscara e caracteres não numéricos"

    # Caso já estivesse normalizado
    else:
        continue

    # Registra a alteração ou problema
    auditoria.append({
        "id_cliente": cliente["id_cliente"],
        "campo": "cnpj",
        "valor_original": cnpj_original,
        "valor_tratado": (
            "" if pd.isna(cnpj_tratado)
            else cnpj_tratado
        ),
        "criterio": criterio
    })

# Transforma a lista em DataFrame
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

print("\n=== AUDITORIA ===")
print(df_auditoria)

print(f"\nTotal de registros de auditoria: {len(df_auditoria)}")


# Criar pastas de saída
PASTA_TRATADOS = BASE_DIR / "dados" / "tratados"
PASTA_RELATORIOS = BASE_DIR / "relatorios"

PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)
PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)

# Salvar dados tratados
df.to_csv(
    PASTA_TRATADOS / "clientes_cnpj_tratado.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

# Salvar auditoria
df_auditoria.to_csv(
    PASTA_RELATORIOS / "auditoria_cnpj.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivos gerados com sucesso!")

