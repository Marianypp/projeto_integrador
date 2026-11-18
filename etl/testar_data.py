
from normalizacao import normalizar_data

datas = [
    "2022-06-21",
    "28/02/2022",
    "Dec 24, 2023",
    "08-01-2022",
    "Aug 18, 2022",
    "jul 21, 2022",
    "nov 19, 2021",
    "31/02/2022",
    ""
]

for data in datas:
    resultado = normalizar_data(data)

    print(f"Original: {data}")
    print(f"Normalizada: {resultado}")
    print("-" * 30)
