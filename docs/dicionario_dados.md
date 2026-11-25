# Dicionário de Dados

Projeto Primora — Distribuidora Vetor


## Dicionário da tabela Vendedor
Tabela: clientes_vendedor
Finalidade: armazenar os vendedores responsáveis pelo atendimento dos clientes.

|Campo |Tipo lógico  |Restrição |Descrição                 |
|------|-------------|----------|--------------------------|
| id   |Inteiro      |   PK	    |Identificador do vendedor |
|nome  |VARCHAR(150) |  Único   |Nome do vendedor          |   



## Dicionário da tabela Cliente
Tabela: clientes_cliente
Finalidade: armazenar os dados cadastrais, de localização e relacionamento dos clientes.

|Campo                |Tipo lógico  |Descrição                     |
|---------------------|-------------|------------------------------|
|id_cliente	          |VARCHAR(20)	|Identificador único — PK      |
|razao_social	      |VARCHAR(255)	|Razão social do cliente       |
|cnpj	              |VARCHAR(14)  |CNPJ normalizado              |
|telefone             |VARCHAR(11)  |Telefone normalizado          |
|email	              |VARCHAR(254) |Endereço eletrônico           |
|bairro               |VARCHAR(150) |Bairro normalizado            |
|cep	              |VARCHAR(8)	|Código postal normalizado     | 
|cidade	              |VARCHAR(100) |Município                     |
|uf	                  |VARCHAR(2)	|Unidade federativa            |
|data_cadastro        |DATE         |Data de cadastro              |
|vendedor_id	      |Inteiro	    |Vendedor responsável — FK     |
|bairro_viacep	      |VARCHAR(150) |Bairro retornado pelo ViaCEP  |
|cidade_viacep	      |VARCHAR(100)	|Cidade retornada pelo ViaCEP  |
|uf_viacep	          |VARCHAR(2)   |UF retornada pelo ViaCEP      |
|status_consulta_cep  |VARCHAR(50)	|Situação da consulta externa  |
|comparacao_bairro_cep|VARCHAR(50)  |Resultado da comparação       |
|ativo	              |BOOLEAN      |Situação cadastral do cliente |



## Dicionário da tabela Auditoria
Tabela: clientes_auditoria
Finalidade: registrar as transformações realizadas pelo processo ETL.

|Campo             |Tipo lógico	|Descrição                            |
|------------------|------------|-------------------------------------|
|id	               |Inteiro     |Identificador da auditoria — PK      |
|cliente_id        |Texto       |Cliente relacionado — FK             |
|campo             |Texto       |Campo submetido ao tratamento        |
|valor_original    |Texto	    |Valor antes da transformação         |
|valor_tratado     |Texto	    |Valor após a transformação           |
|valor_referencia  |Texto       |Informação utilizada como referência |
|criterio          |Texto       |Regra aplicada no tratamento         |
|fonte_referencia  |Texto       |Origem da informação de referência   |
|status	           |Texto       |Situação do tratamento               |
|data_registro     |DATETIME    |Data e hora da auditoria             |



## Dicionário da tabela AuditoriaAPI
Tabela: clientes_auditoriaapi
Finalidade: registrar as operações realizadas pela API REST.

|Campo                  |Tipo lógico |Descrição                    |
|-----------------------|------------|-----------------------------|
|id                     |Inteiro     |Identificador — PK           |
|entidade               |VARCHAR(50) |Entidade modificada          |
|identificador_registro |VARCHAR(100)|Identificador do registro    |
|operacao               |VARCHAR(20) |Tipo de operação             |
|usuario_id             |Inteiro     |Usuário responsável — FK     |
|usuario_nome           |VARCHAR(150)|Nome do usuário responsável  |
|dados_anteriores       |JSON        |Dados anteriores à operação  |
|dados_posteriores      |JSON        |Dados posteriores à operação |
|campos_alterados       |JSON        |Campos modificados           |
|metodo_http            |VARCHAR(10) |Método HTTP utilizado        |
|data_registro          |DATETIME    |Data e hora da operação      |



## Restrições de integridade

O banco de dados utiliza mecanismos de integridade referencial e validação para garantir a consistência das informações.

- O identificador do cliente é único e obrigatório.
- O nome do vendedor possui restrição de unicidade.
- Cada cliente deve possuir um vendedor responsável.
- A exclusão de vendedores com clientes vinculados é protegida pelo relacionamento `PROTECT`.
- A exclusão de clientes pela API ocorre de maneira lógica, utilizando o campo `ativo`.
- Os registros de auditoria do ETL permanecem associados aos respectivos clientes.
- Os registros de auditoria da API preservam informações sobre as operações realizadas.
- A exclusão de um usuário pode preservar seus registros de auditoria por meio do relacionamento `SET_NULL`.

As validações implementadas nos serializers complementam as restrições existentes no banco de dados.

