
import pandas as pd
from core.normalizacao import formatar_celular, formatar_fixo


# ==========================================
# 1. EXTRAÇÃO DA BASE DE CLIENTES
# ==========================================

df = pd.read_csv(
    "02-clientes_distribuidora_vetor.csv",
    sep=";",
    dtype=str
)

print("===== BASE ORIGINAL =====")
print("Dimensões:", df.shape)


# ==========================================
# 2. NORMALIZAÇÃO DOS BAIRROS
# ==========================================

normalizacao_bairros = {
    "Aguas claras": "Águas Claras",
    "aguas claras": "Águas Claras",
    "AGUAS CLARAS": "Águas Claras",
    "Águas Claras/DF": "Águas Claras",
    "Aguas Claras - DF": "Águas Claras",

    "Taguatinga - DF": "Taguatinga",
    "Taguatinga/DF": "Taguatinga",
    "TAGUATINGA": "Taguatinga",

    "taguatinga sul": "Taguatinga Sul",

    "Vte Pires": "Vicente Pires",
    "V. Pires": "Vicente Pires",
    "Vicente Pires - DF": "Vicente Pires",
    "VICENTE PIRES": "Vicente Pires",

    "guara - df": "Guará",

    "Sul (Aguas Claras)": "Sul (Águas Claras)",
    "Norte (Aguas Claras)": "Norte (Águas Claras)"
}

df["bairro_normalizado"] = (
    df["bairro_informado"].replace(normalizacao_bairros)
)

alteracoes_bairro = df[
    df["bairro_informado"].notna() &
    (df["bairro_informado"] != df["bairro_normalizado"])
]

auditoria_bairro = pd.DataFrame({
    "id_cliente": alteracoes_bairro["id_cliente"],
    "campo": "bairro",
    "valor_original": alteracoes_bairro["bairro_informado"],
    "valor_tratado": alteracoes_bairro["bairro_normalizado"],
    "criterio": "dicionario_de_normalizacao"
})


# ==========================================
# 3. NORMALIZAÇÃO DOS CEPS
# ==========================================

df["cep_normalizado"] = df["cep"]

# CEPs que já vieram preenchidos na base original
ceps_para_consultar = df[
    df["cep"].notna() &
    (df["cep"] != "00000-000")
]["cep"].unique()

print("CEPs para consultar:", len(ceps_para_consultar))
print(ceps_para_consultar)

ceps_referencia = {
    "Águas Claras": "71936-970",
    "Sul (Águas Claras)": "71936-970",
    "Norte (Águas Claras)": "71936-970",
    "Águas Claras Sul": "71936-970",
    "Águas Claras Norte": "71936-970",

    "Taguatinga": "72010-971",
    "Taguatinga Sul": "72010-971",

    "Vicente Pires": "72110-970",

    "Guará": "71010-970",
    "Guará I": "71010-970",
    "Guará II": "71081-400"
}

mascara_cep_invalido = (
    df["cep"].isna() |
    (df["cep"] == "00000-000")
)

cep_referencia = df["bairro_normalizado"].map(ceps_referencia)

df.loc[
    mascara_cep_invalido,
    "cep_normalizado"
] = cep_referencia[mascara_cep_invalido]

df["origem_cep"] = "original"

df.loc[
    mascara_cep_invalido & cep_referencia.notna(),
    "origem_cep"
] = "referencia_regional"

df.loc[
    mascara_cep_invalido & cep_referencia.isna(),
    "origem_cep"
] = "sem_informacao"

alteracoes_cep = df[
    df["origem_cep"] == "referencia_regional"
]

auditoria_cep = pd.DataFrame({
    "id_cliente": alteracoes_cep["id_cliente"],
    "campo": "cep",
    "valor_original": alteracoes_cep["cep"],
    "valor_tratado": alteracoes_cep["cep_normalizado"],
    "criterio": "referencia_regional_por_bairro"
})


# ==========================================
# 4. NORMALIZAÇÃO DOS CNPJS
# ==========================================

df["cnpj_normalizado"] = df["cnpj"]

mascara_cnpj = df["cnpj"].str.fullmatch(
    r"\d{14}",
    na=False
)

df.loc[mascara_cnpj, "cnpj_normalizado"] = (
    df.loc[mascara_cnpj, "cnpj"].apply(
        lambda cnpj: (
            f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/"
            f"{cnpj[8:12]}-{cnpj[12:14]}"
        )
    )
)

alteracoes_cnpj = df[
    df["cnpj"] != df["cnpj_normalizado"]
]

auditoria_cnpj = pd.DataFrame({
    "id_cliente": alteracoes_cnpj["id_cliente"],
    "campo": "cnpj",
    "valor_original": alteracoes_cnpj["cnpj"],
    "valor_tratado": alteracoes_cnpj["cnpj_normalizado"],
    "criterio": "formatacao_cnpj"
})


# ==========================================
# 5. NORMALIZAÇÃO DOS TELEFONES
# ==========================================

df["telefone_digitos"] = df["telefone"].str.replace(
    r"\D",
    "",
    regex=True
)

mascara_codigo_pais = (
    (df["telefone_digitos"].str.len() == 13) &
    (df["telefone_digitos"].str.startswith("55"))
)

df.loc[mascara_codigo_pais, "telefone_digitos"] = (
    df.loc[mascara_codigo_pais, "telefone_digitos"].str[2:]
)

df["telefone_normalizado"] = df["telefone_digitos"]

mascara_celular = df["telefone_digitos"].str.len() == 11
mascara_fixo = df["telefone_digitos"].str.len() == 10

df.loc[mascara_celular, "telefone_normalizado"] = (
    df.loc[mascara_celular, "telefone_digitos"].apply(
        formatar_celular
    )
)

df.loc[mascara_fixo, "telefone_normalizado"] = (
    df.loc[mascara_fixo, "telefone_digitos"].apply(
        formatar_fixo
    )
)

alteracoes_telefone = df[
    df["telefone"] != df["telefone_normalizado"]
]

auditoria_telefone = pd.DataFrame({
    "id_cliente": alteracoes_telefone["id_cliente"],
    "campo": "telefone",
    "valor_original": alteracoes_telefone["telefone"],
    "valor_tratado": alteracoes_telefone["telefone_normalizado"],
    "criterio": "remocao_codigo_pais_e_formatacao_por_quantidade_de_digitos"
})

# A coluna auxiliar não precisa permanecer na base final.
df = df.drop(columns=["telefone_digitos"])


# ==========================================
# 6. NORMALIZAÇÃO DAS DATAS
# ==========================================

datas = df["data_cadastro"].str.strip()

mascara_iso = datas.str.fullmatch(
    r"\d{4}-\d{2}-\d{2}",
    na=False
)

datas_convertidas = pd.Series(
    pd.NaT,
    index=df.index,
    dtype="datetime64[ns]"
)

# Datas que já estão no padrão ISO.
datas_convertidas.loc[mascara_iso] = pd.to_datetime(
    datas.loc[mascara_iso],
    format="%Y-%m-%d",
    errors="coerce"
)

# Demais formatos, considerando dia primeiro.
datas_convertidas.loc[~mascara_iso] = pd.to_datetime(
    datas.loc[~mascara_iso],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

df["data_cadastro_normalizada"] = (
    datas_convertidas.dt.strftime("%Y-%m-%d")
)

alteracoes_data = df[
    df["data_cadastro"] != df["data_cadastro_normalizada"]
]

auditoria_data = pd.DataFrame({
    "id_cliente": alteracoes_data["id_cliente"],
    "campo": "data_cadastro",
    "valor_original": alteracoes_data["data_cadastro"],
    "valor_tratado": alteracoes_data["data_cadastro_normalizada"],
    "criterio": "conversao_para_iso_yyyy_mm_dd_dia_primeiro"
})


# ==========================================
# 7. CONSOLIDAÇÃO DA AUDITORIA
# ==========================================

df_auditoria = pd.concat(
    [
        auditoria_bairro,
        auditoria_cep,
        auditoria_cnpj,
        auditoria_telefone,
        auditoria_data
    ],
    ignore_index=True
)


# ==========================================
# 8. VERIFICAÇÕES DA BASE TRATADA
# ==========================================

print("\n===== DIMENSÕES DA BASE =====")
print(df.shape)

print("\n===== BAIRROS NORMALIZADOS =====")
print(df["bairro_normalizado"].value_counts(dropna=False))

print("\n===== ORIGEM DOS CEPS =====")
print(df["origem_cep"].value_counts(dropna=False))

print("\n===== TAMANHO DOS CNPJS =====")
print(df["cnpj_normalizado"].str.len().value_counts())

print("\n===== VALIDAÇÃO DOS TELEFONES =====")
print(
    "Celulares:",
    df["telefone_normalizado"].str.match(
        r"^\(61\) 9\d{4}-\d{4}$",
        na=False
    ).sum()
)

print(
    "Fixos:",
    df["telefone_normalizado"].str.match(
        r"^\(61\) \d{4}-\d{4}$",
        na=False
    ).sum()
)

print("\n===== DATAS NÃO CONVERTIDAS =====")
print(df["data_cadastro_normalizada"].isna().sum())


# ==========================================
# 9. RESUMO DA AUDITORIA
# ==========================================

print("\n===== RESUMO DAS ALTERAÇÕES =====")

print("Bairros tratados:", len(auditoria_bairro))
print("CEPs tratados:", len(auditoria_cep))
print("CNPJs tratados:", len(auditoria_cnpj))
print("Telefones tratados:", len(auditoria_telefone))
print("Datas tratadas:", len(auditoria_data))

print("\nTotal de alterações:", len(df_auditoria))


# ==========================================
# 10. EXPORTAÇÃO DOS ARQUIVOS
# ==========================================

df.to_csv(
    "clientes_tratados.csv",
    sep=";",
    index=False
)

df_auditoria.to_csv(
    "auditoria_etl.csv",
    sep=";",
    index=False
)

print("\n===== EXPORTAÇÃO CONCLUÍDA =====")
print("Arquivo clientes_tratados.csv salvo!")
print("Arquivo auditoria_etl.csv salvo!")
print("Total de clientes:", len(df))
