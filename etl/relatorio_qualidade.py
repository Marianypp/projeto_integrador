
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

CAMINHO_CSV = (
    BASE_DIR
    / "dados"
    / "tratados"
    / "clientes_final.csv"
)

df = pd.read_csv(
    CAMINHO_CSV,
    sep=";",
    encoding="utf-8-sig",
    dtype=str,
    keep_default_na=False
)

campos = {
    "CNPJ": "cnpj_normalizado",
    "Telefone": "telefone_normalizado",
    "Data": "data_cadastro_normalizado",
    "Bairro": "bairro_normalizado",
    "CEP": "cep_normalizado"
}

total = len(df)

relatorio = []

for nome, coluna in campos.items():

    preenchidos = df[coluna].str.strip().ne("").sum()

    pendentes = total - preenchidos

    percentual = (
        preenchidos / total * 100
        if total
        else 0
    )

    relatorio.append({
        "campo": nome,
        "total_registros": total,
        "normalizados": preenchidos,
        "pendentes": pendentes,
        "percentual_normalizado": round(percentual, 2)
    })

df_relatorio = pd.DataFrame(relatorio)

print("\n=== RELATÓRIO DE QUALIDADE ===")
print(df_relatorio.to_string(index=False))

print("\n=== CEP: STATUS DAS CONSULTAS ===")
print(df["status_consulta_cep"].value_counts())

print("\n=== COMPARAÇÃO GEOGRÁFICA ===")
print(df["comparacao_bairro_cep"].value_counts())

df_relatorio.to_csv(
    BASE_DIR / "relatorios" / "qualidade_dados.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)
