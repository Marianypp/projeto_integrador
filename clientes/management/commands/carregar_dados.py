
from pathlib import Path
from datetime import date

import pandas as pd

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from clientes.models import (
    Cliente,
    Vendedor,
    Auditoria
)


class Command(BaseCommand):

    help = "Carrega os dados tratados da Distribuidora Vetor"

    @transaction.atomic
    def handle(self, *args, **options):

        base_dir = Path(settings.BASE_DIR)

        caminho_clientes = (
            base_dir
            / "dados"
            / "tratados"
            / "clientes_final.csv"
        )

        caminho_auditoria = (
            base_dir
            / "relatorios"
            / "auditoria_final.csv"
        )

        df_clientes = pd.read_csv(
            caminho_clientes,
            sep=";",
            encoding="utf-8-sig",
            dtype=str,
            keep_default_na=False
        )

        df_auditoria = pd.read_csv(
            caminho_auditoria,
            sep=";",
            encoding="utf-8-sig",
            dtype=str,
            keep_default_na=False
        )

        if len(df_clientes) != 47:
            raise ValueError(
                "A base deve conter 47 clientes."
            )

        if df_clientes["id_cliente"].duplicated().any():
            raise ValueError(
                "Existem IDs duplicados no CSV."
            )

        self.stdout.write("Iniciando a carga...")


        for _, linha in df_clientes.iterrows():

            # Obtém ou cria o vendedor
            vendedor, criado = Vendedor.objects.get_or_create(
                nome=linha["vendedor_responsavel"].strip()
            )

            # Converte a data tratada
            data_texto = linha["data_cadastro_normalizado"]

            data_cadastro = (
                date.fromisoformat(data_texto)
                if data_texto
                else None
            )

            # Cria ou atualiza o cliente
            cliente, criado = Cliente.objects.update_or_create(

                id_cliente=linha["id_cliente"],

                defaults={
                    "razao_social": linha["razao_social"],

                    "cnpj": (
                        linha["cnpj_normalizado"] or None
                    ),

                    "telefone": (
                        linha["telefone_normalizado"] or None
                    ),

                    "email": linha["email"],

                    "bairro": (
                        linha["bairro_normalizado"] or None
                    ),

                    "cep": (
                        linha["cep_normalizado"] or None
                    ),

                    "cidade": linha["cidade"],
                    "uf": linha["uf"],

                    "data_cadastro": data_cadastro,

                    "vendedor": vendedor,

                    "bairro_viacep": linha["bairro_viacep"],

                    "cidade_viacep": linha["cidade_viacep"],

                    "uf_viacep": linha["uf_viacep"],

                    "status_consulta_cep": (
                        linha["status_consulta_cep"]
                    ),

                    "comparacao_bairro_cep": (
                        linha["comparacao_bairro_cep"]
                    )
                }
            )

            if criado:
                mensagem = "Cliente criado"
            else:
                mensagem = "Cliente atualizado"

            self.stdout.write(
                f"{mensagem}: {cliente.id_cliente}"
            )


        novos_registros = 0

        for _, linha in df_auditoria.iterrows():

            cliente = Cliente.objects.get(
                id_cliente=linha["id_cliente"]
            )

            original = linha["valor_original"]
            tratado = linha["valor_tratado"]
            referencia = ""

            # Separa referência externa de alteração efetiva
            if linha["status"] == "revisao_geografica":

                referencia = tratado
                tratado = original

            auditoria, criada = Auditoria.objects.get_or_create(

                cliente=cliente,
                campo=linha["campo"],

                valor_original=original,
                valor_tratado=tratado,
                valor_referencia=referencia,

                criterio=linha["criterio"],

                fonte_referencia=linha["fonte_referencia"],

                status=linha["status"]
            )

            if criada:
                novos_registros += 1

        self.stdout.write(
            self.style.SUCCESS(
                "\nCarga concluída com sucesso!"
            )
        )

        self.stdout.write(
            f"Clientes no banco: {Cliente.objects.count()}"
        )

        self.stdout.write(
            f"Vendedores no banco: {Vendedor.objects.count()}"
        )

        self.stdout.write(
            f"Novos registros de auditoria: {novos_registros}"
        )

        self.stdout.write(
            f"Auditorias no banco: {Auditoria.objects.count()}"
        )
