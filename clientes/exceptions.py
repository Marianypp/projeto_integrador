
from rest_framework.views import exception_handler


def tratamento_excecoes(exc, context):

    resposta = exception_handler(
        exc,
        context
    )

    if resposta is None:
        return None

    mensagens = {
        400: "Dados inválidos ou operação não permitida.",
        401: "Autenticação necessária.",
        403: "Acesso não autorizado.",
        404: "Recurso não encontrado.",
        405: "Método HTTP não permitido.",
        429: "Limite de requisições excedido."
    }

    dados_originais = resposta.data

    if isinstance(dados_originais, dict):

        dados = dict(dados_originais)

    else:

        dados = {
            "detalhes": dados_originais
        }

    dados["status_code"] = resposta.status_code

    dados["mensagem"] = mensagens.get(
        resposta.status_code,
        "Não foi possível concluir a operação."
    )

    resposta.data = dados

    return resposta
