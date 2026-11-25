
import argparse
import pandas as pd

from pathlib import Path


def carregar_csv(caminho):

    return pd.read_csv(
        caminho,
        sep=None,
        engine="python",
        dtype=str,
        encoding="utf-8-sig"
    )


def obter_identificadores(df):

    return set(
        df["id_cliente"]
        .dropna()
        .str.strip()
        .str.upper()
    )


def validar_arquivos(original, tratado):

    df_original = carregar_csv(original)

    df_tratado = carregar_csv(tratado)

    print("\n=== VALIDACAO DOS ARQUIVOS ===")

    print(
        "Registros originais:",
        len(df_original)
    )

    print(
        "Registros tratados:",
        len(df_tratado)
    )

    print(
        "Linhas duplicadas no original:",
        df_original.duplicated().sum()
    )

    print(
        "Linhas duplicadas no tratado:",
        df_tratado.duplicated().sum()
    )

    if (
        "id_cliente" not in df_original.columns
        or "id_cliente" not in df_tratado.columns
    ):

        print(
            "\nA coluna id_cliente nao foi "
            "encontrada nos dois arquivos."
        )

        print(
            "Colunas originais:",
            df_original.columns.tolist()
        )

        print(
            "Colunas tratadas:",
            df_tratado.columns.tolist()
        )

        return

    ids_originais = obter_identificadores(
        df_original
    )

    ids_tratados = obter_identificadores(
        df_tratado
    )

    print(
        "\nIdentificadores ausentes no tratado:",
        sorted(ids_originais - ids_tratados)
    )

    print(
        "Identificadores adicionais no tratado:",
        sorted(ids_tratados - ids_originais)
    )

    ids_normalizados = (
        df_tratado["id_cliente"]
        .str.strip()
        .str.upper()
    )

    print(
        "Identificadores duplicados:",
        ids_normalizados.duplicated().sum()
    )

    print(
        "Identificadores ausentes:",
        (
            ids_normalizados.isna()
            | ids_normalizados.eq("")
        ).sum()
    )

    print("\n=== VALORES AUSENTES ===")

    print(df_tratado.isna().sum())

    if "bairro" in df_tratado.columns:

        print("\n=== CLIENTES POR BAIRRO ===")

        print(
            df_tratado["bairro"]
            .value_counts(dropna=False)
        )

    if "uf" in df_tratado.columns:

        print("\n=== CLIENTES POR UF ===")

        print(
            df_tratado["uf"]
            .value_counts(dropna=False)
        )

    print("\nValidacao concluida.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Compara os arquivos original "
            "e tratado do ETL."
        )
    )

    parser.add_argument(
        "original",
        type=Path
    )

    parser.add_argument(
        "tratado",
        type=Path
    )

    argumentos = parser.parse_args()

    validar_arquivos(
        argumentos.original,
        argumentos.tratado
    )
