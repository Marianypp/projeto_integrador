import sqlite3
import pandas as pd

df = pd.read_csv(
    "clientes_tratados.csv",
    sep=";",
    dtype=str
)

colunas_banco = [
    "id_cliente",
    "razao_social",
    "cnpj_normalizado",
    "telefone_normalizado",
    "bairro_normalizado",
    "email",
    "cep_normalizado",
    "cidade",
    "uf",
    "data_cadastro_normalizada",
    "vendedor_responsavel"
]

registros = df[colunas_banco].values.tolist()

print("\nQuantidade de registros preparados:", len(registros))
print("Primeiro registro:", registros[0])

print("\n===== DADOS PARA INSERÇÃO =====")
print(df[colunas_banco].head())

print("Dimensões do arquivo:", df.shape)
print("Colunas disponíveis:", df.columns.tolist())

conexao = sqlite3.connect("clientes.db")

conexao.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente TEXT PRIMARY KEY,
        razao_social TEXT,
        cnpj TEXT,
        telefone TEXT,
        bairro_normalizado TEXT,
        email TEXT,
        cep_normalizado TEXT,
        cidade TEXT,
        uf TEXT,
        data_cadastro_normalizada TEXT,
        vendedor_responsavel TEXT
    )
""")

conexao.commit()


colunas_existentes = {
    coluna[1]
    for coluna in conexao.execute("PRAGMA table_info(clientes)")
}

novas_colunas = {
    "email": "TEXT",
    "cep_normalizado": "TEXT",
    "cidade": "TEXT",
    "uf": "TEXT",
    "data_cadastro_normalizada": "TEXT",
    "vendedor_responsavel": "TEXT",
    "bairro_normalizado": "TEXT"
}

for nome, tipo in novas_colunas.items():
    if nome not in colunas_existentes:
        conexao.execute(
            f"ALTER TABLE clientes ADD COLUMN {nome} {tipo}"
        )

conexao.commit()

print("Conexão com o banco de dados realizada!")

conexao.executemany("""
    INSERT OR REPLACE INTO clientes (
        id_cliente,
        razao_social,
        cnpj,
        telefone,
        bairro_normalizado,
        email,
        cep_normalizado,
        cidade,
        uf,
        data_cadastro_normalizada,
        vendedor_responsavel
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", registros)

conexao.commit()

print("Clientes inseridos com sucesso!")

cursor = conexao.execute("""
    SELECT COUNT(*) FROM clientes
""")

total = cursor.fetchone()[0]

print("\nTotal de clientes no banco:", total)

cursor = conexao.execute("""
    SELECT id_cliente, razao_social, bairro_normalizado, cep_normalizado
    FROM clientes
    LIMIT 5
""")

for cliente in cursor:
    print(cliente)

cursor = conexao.execute("""
    SELECT COUNT(*)
    FROM clientes
    WHERE bairro_normalizado IS NULL
       OR TRIM(bairro_normalizado) = ''
       OR cep_normalizado IS NULL
       OR TRIM(cep_normalizado) = ''
""")
sem_localizacao = cursor.fetchone()[0]

print("\nClientes sem bairro ou CEP:", sem_localizacao)


cursor = conexao.execute("PRAGMA table_info(clientes)")

for coluna in cursor:
    print(coluna)

cursor = conexao.execute("""
    SELECT id_cliente, razao_social, bairro_normalizado, cep_normalizado
    FROM clientes
    WHERE bairro_normalizado IS NULL
       OR TRIM(bairro_normalizado) = ''
       OR cep_normalizado IS NULL
       OR TRIM(cep_normalizado) = ''
""")

print("\n===== CLIENTES COM LOCALIZAÇÃO PENDENTE =====")

for cliente in cursor:
    print(cliente)

conexao.close()