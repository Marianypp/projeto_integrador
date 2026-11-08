def formatar_celular(telefone):
    if not telefone.isdigit():
        raise ValueError("Celular inválido: deve conter apenas dígitos")

    if len(telefone) != 11:
        raise ValueError("Celular inválido: deve conter 11 dígitos")

    ddd = telefone[:2]
    numero = telefone[2:7]
    final = telefone[7:]

    return f"({ddd}) {numero}-{final}"


def formatar_fixo(telefone):
    if not telefone.isdigit():
        raise ValueError("Telefone fixo inválido: deve conter apenas dígitos")

    if len(telefone) != 10:
        raise ValueError("Telefone fixo inválido: deve conter 10 dígitos")

    ddd = telefone[:2]
    numero = telefone[2:6]
    final = telefone[6:]

    return f"({ddd}) {numero}-{final}"



    