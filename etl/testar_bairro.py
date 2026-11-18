
from normalizacao import normalizar_bairro

bairros = [
    "AGUAS CLARAS",
    "Aguas claras",
    "Águas Claras/DF",
    "Norte (Aguas Claras)",
    "Sul (Águas Claras)",
    "Vte Pires",
    "V. Pires",
    "taguatinga sul",
    "Guará I",
    "Guará II",
    "Bairro Desconhecido",
    ""
]

for bairro in bairros:
    resultado = normalizar_bairro(bairro)

    print(f"Original: {bairro}")
    print(f"Normalizado: {resultado}")
    print("-" * 35)
