
from pathlib import Path
import argparse
import pandas as pd

from etl.normalizacao import (
    normalizar_cnpj,
    normalizar_telefone,
    normalizar_data,
    normalizar_bairro,
    normalizar_cep,
    comparar_bairros
)

from etl.cache_cep import (
    carregar_cache,
    consultar_com_cache
)


# Pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivo original
CAMINHO_ORIGINAL = (
    BASE_DIR
    / "dados"
    / "originais"
    / "clientes_distribuidora_vetor.csv"
)

# Pastas de saída
PASTA_TRATADOS = BASE_DIR / "dados" / "tratados"
PASTA_RELATORIOS = BASE_DIR / "relatorios"

# Cria as pastas, caso não existam
PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)
PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)


def extrair_dados():

    print("\n[1/5] Extraindo dados...")

    df = pd.read_csv(
        CAMINHO_ORIGINAL,
        sep=";",
        encoding="utf-8-sig",
        dtype=str,
        keep_default_na=False
    )

    print(f"Clientes encontrados: {len(df)}")

    # Verifica se os IDs estão duplicados
    if df["id_cliente"].duplicated().any():
        raise ValueError(
            "Existem IDs de clientes duplicados!"
        )

    return df


def transformar_dados(df):

    print("\n[2/5] Normalizando os dados...")

    # Trabalha sobre uma cópia
    df = df.copy()

    # CNPJ
    df["cnpj_normalizado"] = (
        df["cnpj"].apply(normalizar_cnpj)
    )

    # Telefone
    df["telefone_normalizado"] = (
        df["telefone"].apply(normalizar_telefone)
    )

    # Data
    df["data_cadastro_normalizado"] = (
        df["data_cadastro"].apply(normalizar_data)
    )

    # Bairro
    df["bairro_normalizado"] = (
        df["bairro_informado"].apply(normalizar_bairro)
    )

    # CEP
    df["cep_normalizado"] = (
        df["cep"].apply(normalizar_cep)
    )

    print("Normalização concluída!")

    return df


def enriquecer_dados(df, consultar_ceps=False):

    print("\n[3/5] Enriquecendo os dados...")

    df = df.copy()

    cache = carregar_cache()
    resultados = []

    for _, cliente in df.iterrows():

        cep = cliente["cep_normalizado"]

        if pd.isna(cep):
            resultado = {
                "status": "cep_invalido_ou_ausente",
                "dados": None
            }

        elif consultar_ceps:
            resultado = consultar_com_cache(cep, cache)

        elif cep in cache:
            resultado = cache[cep]

        else:
            resultado = {
                "status": "nao_consultado",
                "dados": None
            }

        dados = resultado["dados"] or {}

        bairro_api = dados.get("bairro", "")

        if resultado["status"] == "encontrado":
            comparacao = comparar_bairros(
                cliente["bairro_normalizado"],
                bairro_api
            )
        else:
            comparacao = "sem_comparacao"

        resultados.append({
            "status_consulta_cep": resultado["status"],
            "bairro_viacep": bairro_api,
            "cidade_viacep": dados.get("localidade", ""),
            "uf_viacep": dados.get("uf", ""),
            "comparacao_bairro_cep": comparacao
        })

    # Converte os resultados em DataFrame
    df_resultados = pd.DataFrame(
        resultados,
        index=df.index
    )

    # Acrescenta as colunas ao DataFrame original
    df = pd.concat([df, df_resultados], axis=1)

    print("Enriquecimento concluído!")

    return df


def gerar_auditoria(df):

    print("\n[4/5] Gerando auditoria...")

    auditoria = []

    campos = {
        "cnpj": "cnpj_normalizado",
        "telefone": "telefone_normalizado",
        "data_cadastro": "data_cadastro_normalizado",
        "bairro_informado": "bairro_normalizado",
        "cep": "cep_normalizado"
    }

    criterios = {
        "cnpj": "Padronização para 14 dígitos",
        "telefone": "Remoção de máscara e DDI",
        "data_cadastro": "Conversão para ISO 8601",
        "bairro_informado": "Dicionário de equivalências",
        "cep": "Padronização para 8 dígitos"
    }

    for _, cliente in df.iterrows():

        for campo_original, campo_tratado in campos.items():

            original = cliente[campo_original]
            tratado = cliente[campo_tratado]

            if pd.isna(tratado):
                status = "revisao_necessaria"
                criterio = "Valor ausente ou não normalizado"

            elif original != tratado:
                status = "alterado"
                criterio = criterios[campo_original]

            else:
                continue

            auditoria.append({
                "id_cliente": cliente["id_cliente"],
                "campo": campo_original,
                "valor_original": original,
                "valor_tratado": (
                    "" if pd.isna(tratado)
                    else tratado
                ),
                "criterio": criterio,
                "fonte_referencia": "Regra interna do ETL",
                "status": status
            })

        # Registra resultados de consultas e
        # divergências geográficas
        status_cep = cliente["status_consulta_cep"]
        comparacao = cliente["comparacao_bairro_cep"]

        if status_cep in (
            "nao_encontrado",
            "erro_consulta"
        ):
            motivo = f"Consulta CEP: {status_cep}"

        elif comparacao not in (
            "compativel",
            "sem_comparacao"
        ):
            motivo = f"Comparação geográfica: {comparacao}"

        else:
            motivo = None

        if motivo:
            auditoria.append({
                "id_cliente": cliente["id_cliente"],
                "campo": "bairro_normalizado",
                "valor_original": (
                    cliente["bairro_normalizado"] or ""
                ),
                "valor_tratado": (
                    cliente["bairro_viacep"]
                ),
                "criterio": motivo,
                "fonte_referencia": "ViaCEP",
                "status": "revisao_geografica"
            })

    colunas = [
        "id_cliente",
        "campo",
        "valor_original",
        "valor_tratado",
        "criterio",
        "fonte_referencia",
        "status"
    ]

    df_auditoria = pd.DataFrame(
        auditoria,
        columns=colunas
    )

    print(
        f"Registros de auditoria: {len(df_auditoria)}"
    )

    return df_auditoria


def salvar_resultados(df, df_auditoria):

    print("\n[5/5] Salvando os resultados...")

    # Garante que nenhum cliente foi perdido
    if len(df) != 47:
        raise ValueError(
            "A quantidade de clientes está diferente de 47!"
        )

    # Verifica IDs duplicados
    if df["id_cliente"].duplicated().any():
        raise ValueError(
            "Existem IDs duplicados na base final!"
        )

    # Arquivo com os clientes tratados
    caminho_clientes = (
        PASTA_TRATADOS / "clientes_final.csv"
    )

    df.to_csv(
        caminho_clientes,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    # Arquivo de auditoria consolidada
    caminho_auditoria = (
        PASTA_RELATORIOS / "auditoria_final.csv"
    )

    df_auditoria.to_csv(
        caminho_auditoria,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    # Registros que precisam de revisão
    
    pendentes = df[
        df["cnpj_normalizado"].isna()
        |
        df["telefone_normalizado"].isna()
        |
        df["data_cadastro_normalizado"].isna()
        |
        df["bairro_normalizado"].isna()
        |
        df["cep_normalizado"].isna()
        |
        (
            df["status_consulta_cep"]
            != "encontrado"
        )
        |
        (
            df["comparacao_bairro_cep"]
            != "compativel"
        )
    ]


    pendentes.to_csv(
        PASTA_RELATORIOS / "pendencias_finais.csv",
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nArquivos gerados:")
    print(caminho_clientes)
    print(caminho_auditoria)
    print(f"Pendências identificadas: {len(pendentes)}")


def executar_pipeline(consultar_ceps=False):

    print("=" * 50)
    print("ETL - DISTRIBUIDORA VETOR")
    print("=" * 50)

    # Etapa 1 - Extração
    df = extrair_dados()

    # Etapa 2 - Transformação
    df = transformar_dados(df)

    # Etapa 3 - Enriquecimento
    df = enriquecer_dados(
        df,
        consultar_ceps=consultar_ceps
    )

    # Etapa 4 - Auditoria
    df_auditoria = gerar_auditoria(df)

    # Etapa 5 - Saída
    salvar_resultados(df, df_auditoria)

    print("\n" + "=" * 50)
    print("PIPELINE EXECUTADO COM SUCESSO!")
    print("=" * 50)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Pipeline ETL da Distribuidora Vetor"
    )

    parser.add_argument(
        "--consultar-ceps",
        action="store_true",
        help="Consulta a ViaCEP para enriquecer os dados"
    )

    argumentos = parser.parse_args()

    executar_pipeline(
        consultar_ceps=argumentos.consultar_ceps
    )
