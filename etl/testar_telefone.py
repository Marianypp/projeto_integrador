
from normalizacao import normalizar_telefone

telefones = [
    "+55 61 95386-2084",
    "(61) 98433-1053",
    "(61) 3491-1634",
    "61 3970-2193",
    "61970855700",
    "12345",
    ""
]

for telefone in telefones:
    resultado = normalizar_telefone(telefone)

    print(f"Original: {telefone}")
    print(f"Normalizado: {resultado}")
    print("-" * 30)
