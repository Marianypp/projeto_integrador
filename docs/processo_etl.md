# Documentação do Processo ETL

## 1. Objetivo

O processo ETL tem como objetivo transformar os dados cadastrais da Distribuidora Vetor em informações estruturadas, padronizadas e adequadas para armazenamento em um banco de dados relacional.

## 2. Extração

A etapa de extração realiza a leitura do arquivo CSV original, preservando os dados de origem para permitir comparações posteriores.

## 3. Transformação

Durante a transformação, são aplicadas regras de normalização aos campos cadastrais, incluindo CNPJ, telefone, CEP, bairro, UF e datas.

As inconsistências identificadas são tratadas conforme os critérios definidos no processo de normalização.

## 4. Enriquecimento

O serviço ViaCEP é utilizado como fonte externa de referência para informações de localização.

Os dados retornados pela consulta são armazenados separadamente, permitindo identificar divergências sem substituir automaticamente as informações cadastrais.

O mecanismo de cache contribui para reduzir consultas repetidas ao serviço externo.

## 5. Auditoria

As transformações realizadas são registradas para permitir a identificação do campo tratado, do valor original, do valor resultante, do critério aplicado e da fonte de referência.

## 6. Carga

Os dados tratados são carregados no PostgreSQL, respeitando os relacionamentos entre clientes, vendedores e registros de auditoria.

## 7. Validação

A qualidade dos dados é avaliada por meio de testes automatizados, comparação dos arquivos original e tratado e consultas de consistência ao banco de dados.


## 8. Resultados

Os indicadores de qualidade e os resultados obtidos devem ser consultados nos relatórios de validação armazenados na pasta `relatorios/`.

## 9. Limitações

A qualidade dos resultados depende dos dados de origem e das regras de tratamento implementadas.

Consultas externas também estão sujeitas à disponibilidade do serviço utilizado. As divergências que não podem ser resolvidas automaticamente devem permanecer documentadas para análise posterior.



## Relembrando as etapas do ETL

### Extract — Extração
Leitura do CSV original, identificação das colunas e análise inicial da qualidade dos dados.

### Transform — Transformação
Normalização dos campos, tratamento de inconsistências, enriquecimento e geração de auditorias.

### Load — Carga
Armazenamento dos clientes, vendedores e registros de auditoria no PostgreSQL.



## Documentando as regras de normalização
|Campo            |Tratamento                                                     |Exemplo Dado Original |Exemplo Dado Tratado |
|-----------------|---------------------------------------------------------------|----------------------|---------------------|
|CNPJ             |Remoção de caracteres de formatação e padronização dos dígitos |11.222.333/0001-81    |11222333000181       |
|Telefone         |Padronização dos dígitos                                       |(61) 99999-9999       |61999999999          |
|CEP              |Padronização e consulta de referência                          |71926-750             |71926750             |
|Bairro           |Normalização das variações de escrita                          |aguas claras          |Águas Claras         |
|UF               |Padronização das siglas                                        |df                    |DF                   |
|Data             |Conversão para formato consistente                             |15/01/2024            |2024-01-15           |
|Vendedor         |Padronização e identificação do responsável                    |
|Valores ausentes |	Tratamento conforme as regras de cada campo                   |



## Documentando o enriquecimento com ViaCEP
O ViaCEP foi utilizado como fonte externa de referência para os dados de localização.
A decisão de manter os campos de referência separados dos dados normalizados permite preservar a rastreabilidade das informações.
A informação retornada pelo ViaCEP não deve ser considerada automaticamente superior ao dado cadastral em todas as situações.
Essa decisão evita alterações indevidas e facilita a análise posterior das divergências.




