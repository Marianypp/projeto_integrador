# Regras de Normalização de Bairros — Distribuidora Vetor

## Objetivo

Padronizar os nomes dos bairros informados pelos clientes da Distribuidora Vetor, reduzindo inconsistências de escrita e permitindo consultas agrupadas na futura API REST.

## Estratégia adotada

A equipe optou pela normalização textual determinística combinada com um dicionário de equivalências.

As regras incluem:

1. Remoção de espaços extras.
2. Conversão temporária para letras minúsculas e remoção de acentos para comparação.
3. Padronização de abreviações conhecidas.
4. Remoção de referências redundantes à UF quando previstas no dicionário.
5. Preservação das subdivisões Norte, Sul, Guará I e Guará II.
6. Encaminhamento de valores ausentes ou desconhecidos para revisão.

## Decisões de tratamento

A equipe decidiu preservar subdivisões geográficas, evitando agrupamentos que possam eliminar informações relevantes.

Por exemplo, "Águas Claras Norte" e "Águas Claras Sul" permanecem como valores distintos, embora pertençam ao mesmo grupo principal.

## Limitações

A normalização textual não comprova que o bairro informado corresponde à localização real do cliente.

Essa verificação será realizada posteriormente por meio da análise dos CEPs.

## Auditoria

Todas as alterações de grafia são registradas com o identificador do cliente, valor original, valor tratado e critério de transformação.

Registros sem correspondência permanecem na base e são sinalizados para revisão.

## Próximas etapas

Validar e normalizar os CEPs, consultar fontes externas de referência geográfica e documentar possíveis divergências entre bairro informado e CEP.