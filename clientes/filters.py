import django_filters

from .models import Cliente, Vendedor


class ClienteFilter(django_filters.FilterSet):

    bairro = django_filters.CharFilter(
        field_name="bairro",
        lookup_expr="iexact"
    )

    cidade = django_filters.CharFilter(
        field_name="cidade",
        lookup_expr="iexact"
    )

    uf = django_filters.CharFilter(
        field_name="uf",
        lookup_expr="iexact"
    )

    vendedor_id = django_filters.NumberFilter(
        field_name="vendedor_id"
    )

    vendedor_nome = django_filters.CharFilter(
        field_name="vendedor__nome",
        lookup_expr="icontains"
    )

    cnpj = django_filters.CharFilter(
        field_name="cnpj",
        lookup_expr="exact"
    )

    data_inicio = django_filters.DateFilter(
        field_name="data_cadastro",
        lookup_expr="gte"
    )

    data_fim = django_filters.DateFilter(
        field_name="data_cadastro",
        lookup_expr="lte"
    )

    class Meta:

        model = Cliente

        fields = [
            "bairro",
            "cidade",
            "uf",
            "vendedor_id",
            "vendedor_nome",
            "cnpj",
            "data_inicio",
            "data_fim",
        ]


class VendedorFilter(django_filters.FilterSet):

    nome = django_filters.CharFilter(
        field_name="nome",
        lookup_expr="icontains"
    )

    class Meta:

        model = Vendedor

        fields = [
            "nome"
        ]
