from normalizacao import normalizar_cnpj

cnpj1 = "82.278.248/9638-34"
cnpj2 = "82278248963834"
cnpj3 = "123"
cnpj4 = ""

print("Teste 1:", normalizar_cnpj(cnpj1))
print("Teste 2:", normalizar_cnpj(cnpj2))
print("Teste 3:", normalizar_cnpj(cnpj3))
print("Teste 4:", normalizar_cnpj(cnpj4))