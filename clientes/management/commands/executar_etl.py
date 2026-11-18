
from django.core.management.base import BaseCommand
from django.core.management import call_command

from etl.pipeline import executar_pipeline


class Command(BaseCommand):

    help = (
        "Executa o ETL completo "
        "da Distribuidora Vetor"
    )

    def add_arguments(self, parser):

        parser.add_argument(
            "--consultar-ceps",
            action="store_true",
            help="Realiza novas consultas à ViaCEP"
        )

    def handle(self, *args, **options):

        self.stdout.write(
            "Iniciando o processo de ETL..."
        )

        # Extração e transformação
        executar_pipeline(
            consultar_ceps=options["consultar_ceps"]
        )

        # Carga no PostgreSQL
        call_command("carregar_dados")

        self.stdout.write(
            self.style.SUCCESS(
                "\nETL completo finalizado!"
            )
        )
