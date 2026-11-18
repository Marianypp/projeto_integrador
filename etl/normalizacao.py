from datetime import datetime
import re
import unicodedata


def normalizar_cnpj(cnpj):
    # Verifica se o valor está vazio
    if cnpj is None or str(cnpj).strip() == "":
        return None

    # Converte o valor para texto
    cnpj = str(cnpj)

    # Remove tudo que não for número
    cnpj_limpo = re.sub(r"\D", "", cnpj)

    # Verifica se tem exatamente 14 dígitos
    if len(cnpj_limpo) != 14:
        return None

    # Retorna o CNPJ normalizado
    return cnpj_limpo


def normalizar_telefone(telefone):
    # Verifica se o telefone está vazio
    if telefone is None or str(telefone).strip() == "":
        return None

    # Transforma o valor em texto
    telefone = str(telefone)

    # Remove espaços, parênteses, traços e outros símbolos
    telefone_limpo = re.sub(r"\D", "", telefone)

    # Remove o DDI 55 quando estiver presente
    if len(telefone_limpo) in (12, 13) and telefone_limpo.startswith("55"):
        telefone_limpo = telefone_limpo[2:]

    # Verifica a quantidade de dígitos
    if len(telefone_limpo) not in (10, 11):
        return None

    return telefone_limpo


def normalizar_data(valor):
    # Verifica se a data está vazia
    if valor is None or str(valor).strip() == "":
        return None

    # Converte o valor para texto
    data_texto = str(valor).strip()

    # Meses abreviados encontrados no CSV
    meses = {
        "jan": "Jan",
        "feb": "Feb",
        "mar": "Mar",
        "apr": "Apr",
        "may": "May",
        "jun": "Jun",
        "jul": "Jul",
        "aug": "Aug",
        "sep": "Sep",
        "oct": "Oct",
        "nov": "Nov",
        "dec": "Dec"
    }

    # Padroniza o nome do mês, quando existir
    partes = data_texto.split(" ", 1)

    if len(partes) == 2:
        mes = partes[0].lower()

        if mes in meses:
            data_texto = meses[mes] + " " + partes[1]

    # Formatos aceitos pelo projeto
    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y"
    ]

    # Tenta converter formatos numéricos
    for formato in formatos:
        try:
            data = datetime.strptime(data_texto, formato)
            return data.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # Trata os meses em inglês sem depender
    # do idioma configurado no computador
    meses_numericos = {
        "Jan": 1, "Feb": 2, "Mar": 3,
        "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9,
        "Oct": 10, "Nov": 11, "Dec": 12
    }

    try:
        mes_texto, restante = data_texto.split(" ", 1)
        dia_texto, ano_texto = restante.split(",", 1)

        mes = meses_numericos[mes_texto]
        dia = int(dia_texto.strip())
        ano = int(ano_texto.strip())

        data = datetime(ano, mes, dia)

        return data.strftime("%Y-%m-%d")

    except (ValueError, KeyError):
        return None


def preparar_texto(texto):
    # Verifica se o valor está vazio
    if texto is None or str(texto).strip() == "":
        return ""

    # Converte para texto e minúsculas
    texto = str(texto).strip().lower()

    # Separa letras e acentos
    texto = unicodedata.normalize("NFD", texto)

    # Remove os sinais de acentuação
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    # Remove espaços duplicados
    texto = " ".join(texto.split())

    return texto


MAPA_BAIRROS = {
    # Águas Claras
    "aguas claras": "Águas Claras",
    "aguas claras/df": "Águas Claras",
    "aguas claras - df": "Águas Claras",

    # Subdivisões de Águas Claras
    "aguas claras norte": "Águas Claras Norte",
    "norte (aguas claras)": "Águas Claras Norte",
    "aguas claras sul": "Águas Claras Sul",
    "sul (aguas claras)": "Águas Claras Sul",

    # Taguatinga
    "taguatinga": "Taguatinga",
    "taguatinga - df": "Taguatinga",
    "taguatinga/df": "Taguatinga",
    "taguatinga sul": "Taguatinga Sul",

    # Vicente Pires
    "vicente pires": "Vicente Pires",
    "vicente pires - df": "Vicente Pires",
    "vte pires": "Vicente Pires",
    "v. pires": "Vicente Pires",

    # Guará
    "guara": "Guará",
    "guara - df": "Guará",
    "guara i": "Guará I",
    "guara ii": "Guará II"
}

def normalizar_bairro(bairro):
    # Verifica se está vazio
    if bairro is None or str(bairro).strip() == "":
        return None

    # Prepara o texto para comparação
    bairro_preparado = preparar_texto(bairro)

    # Procura no dicionário
    bairro_normalizado = MAPA_BAIRROS.get(
        bairro_preparado
    )

    # Se não encontrar correspondência,
    # retorna None para revisão
    return bairro_normalizado



def normalizar_cep(cep):

    if cep is None:
        return None

    cep = str(cep).strip()

    if not cep:
        return None

    # Aceita apenas oito dígitos,
    # com ou sem o hífen da máscara
    if not re.fullmatch(r"[0-9]{5}-?[0-9]{3}", cep):
        return None

    cep_limpo = cep.replace("-", "")

    if cep_limpo == "00000000":
        return None

    return cep_limpo



def comparar_bairros(bairro_informado, bairro_api):

    if not bairro_informado:
        return "bairro_informado_ausente"

    if not bairro_api:
        return "bairro_api_ausente"

    # Normaliza o nome retornado pela API
    bairro_api_normalizado = normalizar_bairro(bairro_api)

    # Se não reconhecermos o bairro da API,
    # não fazemos uma comparação conclusiva
    if bairro_api_normalizado is None:
        return "revisao_manual"

    # Compara os nomes padronizados
    if bairro_informado == bairro_api_normalizado:
        return "compativel"

    # Identifica subdivisões de um mesmo grupo
    grupos = [
        "Águas Claras",
        "Taguatinga",
        "Vicente Pires",
        "Guará"
    ]

    for grupo in grupos:
        if (
            bairro_informado.startswith(grupo)
            and bairro_api_normalizado.startswith(grupo)
        ):
            return "revisao_subdivisao"

    return "divergente"
