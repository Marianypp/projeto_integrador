
from pathlib import Path
import pandas as pd

# Localiza a pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho do arquivo original
CAMINHO_CSV = (
    BASE_DIR
    / "dados"
    / "originais"
    / "clientes_distribuidora_vetor.csv"
)

# Leitura do CSV
df = pd.read_csv(
    CAMINHO_CSV,
    sep=";",
    encoding="utf-8-sig",
    dtype=str,
    keep_default_na=False
)

print("=== ANÁLISE INICIAL ===")

print(f"Quantidade de clientes: {len(df)}")
print(f"Quantidade de colunas: {len(df.columns)}")

print("\nNomes das colunas:")
print(df.columns.tolist())

print("\nPrimeiros cinco registros:")
print(df.head())

print("\nValores vazios por coluna:")
for coluna in df.columns:
    quantidade = df[coluna].str.strip().eq("").sum()
    print(f"{coluna}: {quantidade}")

print("\nIDs duplicados:")
print(df["id_cliente"].duplicated().sum())

print("\nBairros encontrados:")
print(df["bairro_informado"].value_counts(dropna=False))


# Criar a pasta de relatórios, se não existir
PASTA_RELATORIOS = BASE_DIR / "relatorios"
PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)

# Caminho do relatório
CAMINHO_RELATORIO = (
    PASTA_RELATORIOS / "relatorio_inicial.txt"
)

# Contagem de campos vazios
valores_vazios = {}

for coluna in df.columns:
    valores_vazios[coluna] = int(
        df[coluna].str.strip().eq("").sum()
    )

# Construção do relatório
linhas = [
    "RELATÓRIO INICIAL - DISTRIBUIDORA VETOR",
    "=" * 45,
    f"Total de clientes: {len(df)}",
    f"Total de colunas: {len(df.columns)}",
    "",
    "VALORES VAZIOS:",
]

for coluna, quantidade in valores_vazios.items():
    linhas.append(f"{coluna}: {quantidade}")

linhas.append("")
linhas.append("BAIRROS ENCONTRADOS:")

for bairro, quantidade in df["bairro_informado"].value_counts().items():
    nome = bairro if bairro.strip() else "(vazio)"
    linhas.append(f"{nome}: {quantidade}")

# Salvar relatório
CAMINHO_RELATORIO.write_text(
    "\n".join(linhas),
    encoding="utf-8"
)

print("\nRelatório gerado com sucesso!")
print(CAMINHO_RELATORIO)
