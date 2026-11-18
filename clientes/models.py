from django.db import models


class Vendedor(models.Model):

    nome = models.CharField(
        max_length=150,
        unique=True
    )

    def __str__(self):
        return self.nome


class Cliente(models.Model):

    id_cliente = models.CharField(
        max_length=20,
        primary_key=True
    )

    razao_social = models.CharField(
        max_length=255
    )

    cnpj = models.CharField(
        max_length=14,
        null=True,
        blank=True
    )

    telefone = models.CharField(
        max_length=11,
        null=True,
        blank=True
    )

    email = models.EmailField(
        max_length=254,
        blank=True
    )

    bairro = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        db_index=True
    )

    cep = models.CharField(
        max_length=8,
        null=True,
        blank=True
    )

    cidade = models.CharField(
        max_length=100
    )

    uf = models.CharField(
        max_length=2
    )

    data_cadastro = models.DateField(
        null=True,
        blank=True
    )

    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.PROTECT,
        related_name="clientes"
    )

    bairro_viacep = models.CharField(
        max_length=150,
        blank=True
    )

    cidade_viacep = models.CharField(
        max_length=100,
        blank=True
    )

    uf_viacep = models.CharField(
        max_length=2,
        blank=True
    )

    status_consulta_cep = models.CharField(
        max_length=50,
        blank=True
    )

    comparacao_bairro_cep = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return self.razao_social


class Auditoria(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="auditorias"
    )

    campo = models.CharField(
        max_length=100
    )

    valor_original = models.TextField(
        blank=True
    )

    valor_tratado = models.TextField(
        blank=True
    )

    valor_referencia = models.TextField(
        blank=True
    )

    criterio = models.TextField()

    fonte_referencia = models.CharField(
        max_length=150
    )

    status = models.CharField(
        max_length=50
    )

    data_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.cliente_id} - {self.campo}"
        )
