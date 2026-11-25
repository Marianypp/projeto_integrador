
from django.core.management.base import (
    BaseCommand,
    CommandError
)

from django.db.models import Count, Q

from clientes.models import (
    Cliente,
    Vendedor,
    Auditoria,
    AuditoriaAPI
)


class Command(BaseCommand):

    help = (
        "Verifica a integridade dos dados "
        "do Projeto Primora."
    )

    def handle(self, *args, **options):

        self.stdout.write(
            "\n=== VALIDACAO DO PROJETO PRIMORA ==="
        )

        total = Cliente.objects.count()

        ativos = Cliente.objects.filter(
            ativo=True
        ).count()

        inativos = Cliente.objects.filter(
            ativo=False
        ).count()

        sem_vendedor = Cliente.objects.filter(
            vendedor__isnull=True
        ).count()

        sem_bairro = (
            Cliente.objects
            .filter(ativo=True)
            .filter(
                Q(bairro__isnull=True)
                | Q(bairro="")
            )
            .count()
        )

        total_vendedores = (
            Vendedor.objects.count()
        )

        agrupamento_vendedores = (
            Vendedor.objects
            .annotate(
                total_clientes=Count(
                    "clientes",
                    filter=Q(
                        clientes__ativo=True
                    )
                )
            )
            .values(
                "id",
                "nome",
                "total_clientes"
            )
        )

        soma_vendedores = sum(
            item["total_clientes"]
            for item in agrupamento_vendedores
        )

        agrupamento_bairros = (
            Cliente.objects
            .filter(ativo=True)
            .exclude(bairro__isnull=True)
            .exclude(bairro="")
            .values("bairro")
            .annotate(
                total_clientes=Count(
                    "id_cliente"
                )
            )
        )

        soma_bairros = sum(
            item["total_clientes"]
            for item in agrupamento_bairros
        )

        self.stdout.write(
            f"Total de clientes: {total}"
        )

        self.stdout.write(
            f"Clientes ativos: {ativos}"
        )

        self.stdout.write(
            f"Clientes inativos: {inativos}"
        )

        self.stdout.write(
            f"Total de vendedores: {total_vendedores}"
        )

        self.stdout.write(
            f"Clientes sem vendedor: {sem_vendedor}"
        )

        self.stdout.write(
            f"Ativos sem bairro: {sem_bairro}"
        )

        self.stdout.write(
            f"Total por vendedor: {soma_vendedores}"
        )

        self.stdout.write(
            f"Total por bairro: {soma_bairros}"
        )

        self.stdout.write(
            f"Auditorias ETL: "
            f"{Auditoria.objects.count()}"
        )

        self.stdout.write(
            f"Auditorias API: "
            f"{AuditoriaAPI.objects.count()}"
        )

        verificacoes = [

            (
                "Existencia de clientes",
                total > 0
            ),

            (
                "Existencia de vendedores",
                total_vendedores > 0
            ),

            (
                "Total de ativos e inativos",
                total == ativos + inativos
            ),

            (
                "Relacionamento com vendedores",
                sem_vendedor == 0
            ),

            (
                "Consistencia por vendedor",
                soma_vendedores == ativos
            ),

            (
                "Consistencia por bairro",
                soma_bairros == ativos - sem_bairro
            ),

        ]

        falhas = 0

        self.stdout.write(
            "\n=== RESULTADOS ==="
        )

        for descricao, resultado in verificacoes:

            if resultado:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"[OK] {descricao}"
                    )
                )

            else:

                falhas += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"[FALHA] {descricao}"
                    )
                )

        if sem_bairro > 0:

            self.stdout.write(
                self.style.WARNING(
                    "Existem clientes ativos "
                    "sem bairro informado."
                )
            )

        if falhas:

            raise CommandError(
                f"Validacao encontrou "
                f"{falhas} falha(s)."
            )

        self.stdout.write(
            self.style.SUCCESS(
                "\nValidacoes do banco concluidas "
                "sem falhas."
            )
        )

