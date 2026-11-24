import json

from django.core.serializers.json import (
    DjangoJSONEncoder
)

from .models import (
    Cliente,
    Vendedor,
    AuditoriaAPI
)


def capturar_dados(instancia):

    if isinstance(instancia, Cliente):

        dados = {
            "id_cliente": instancia.id_cliente,
            "razao_social": instancia.razao_social,
            "cnpj": instancia.cnpj,
            "telefone": instancia.telefone,
            "email": instancia.email,
            "bairro": instancia.bairro,
            "cep": instancia.cep,
            "cidade": instancia.cidade,
            "uf": instancia.uf,
            "data_cadastro": instancia.data_cadastro,
            "vendedor_id": instancia.vendedor_id,
            "ativo": instancia.ativo,
        }

    elif isinstance(instancia, Vendedor):

        dados = {
            "id": instancia.pk,
            "nome": instancia.nome,
        }

    else:

        raise ValueError(
            "Entidade não suportada pela auditoria."
        )

    return json.loads(
        json.dumps(
            dados,
            cls=DjangoJSONEncoder
        )
    )


def identificar_campos_alterados(
    dados_anteriores,
    dados_posteriores
):

    campos = (
        set(dados_anteriores.keys())
        | set(dados_posteriores.keys())
    )

    alterados = []

    for campo in campos:

        if (
            campo not in dados_anteriores
            or campo not in dados_posteriores
            or dados_anteriores[campo]
            != dados_posteriores[campo]
        ):

            alterados.append(campo)

    return sorted(alterados)


def registrar_auditoria(
    request,
    entidade,
    identificador,
    operacao,
    dados_anteriores=None,
    dados_posteriores=None
):

    anteriores = (
        dados_anteriores
        if dados_anteriores is not None
        else {}
    )

    posteriores = (
        dados_posteriores
        if dados_posteriores is not None
        else {}
    )

    campos_alterados = (
        identificar_campos_alterados(
            anteriores,
            posteriores
        )
    )

    if (
        operacao == AuditoriaAPI.Operacao.ATUALIZACAO
        and not campos_alterados
    ):

        return None

    usuario = request.user

    return AuditoriaAPI.objects.create(
        entidade=entidade,
        identificador_registro=str(identificador),
        operacao=operacao,
        usuario=usuario,
        usuario_nome=usuario.get_username(),
        dados_anteriores=anteriores,
        dados_posteriores=posteriores,
        campos_alterados=campos_alterados,
        metodo_http=request.method
    )
