
from normalizacao import normalizar_cep

ceps = [
    "71926-750",
    "72140-010",
    "72006400",
    "00000-000",
    "",
    "123",
    "71900-100"
]

for cep in ceps:
    resultado = normalizar_cep(cep)

    print(f"Original: {cep}")
    print(f"Normalizado: {resultado}")
    print("-" * 30)
