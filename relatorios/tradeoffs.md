# Relatório de Trade-offs — Distribuidora Vetor

## 1. Introdução

O projeto tem como objetivo implementar um pipeline de ETL para a extração, normalização, enriquecimento e persistência dos dados de clientes da Distribuidora Vetor. A solução foi desenvolvida utilizando Python, Pandas, PostgreSQL e Django ORM, considerando critérios de qualidade, integridade, rastreabilidade e reprodutibilidade.

## 2. Estratégias de normalização

Para os campos CNPJ, telefone, CEP e data de cadastro, foram propostas regras determinísticas de transformação. Os identificadores numéricos são armazenados como textos, preservando possíveis zeros iniciais, enquanto as datas são convertidas para o padrão ISO 8601.

Como o conjunto de dados é fictício, optou-se por verificar a estrutura do CNPJ, sem utilizar seus dígitos verificadores como critério de exclusão de registros.

A normalização dos bairros utiliza um dicionário de equivalências, associado à remoção temporária de acentos, diferenças de capitalização e espaços extras. Essa abordagem apresenta maior previsibilidade e facilidade de auditoria, embora necessite de manutenção quando surgirem novas grafias ou localidades desconhecidas.

Também foi proposta a preservação das subdivisões geográficas, evitando a perda de informações potencialmente relevantes.

## 3. Enriquecimento geográfico

A consulta à API ViaCEP foi incorporada como fonte complementar de informações geográficas. Entretanto, o CEP informado pelo cliente também pode apresentar inconsistências.

Por esse motivo, a solução não substitui automaticamente o bairro informado quando existem divergências com a fonte externa. Os casos ambíguos são encaminhados para revisão, priorizando a integridade dos dados em relação à automação integral do tratamento.

Para reduzir consultas repetidas, foi implementado um cache local. Essa estratégia melhora a eficiência e reduz a dependência da disponibilidade do serviço externo, mas apresenta como limitação a possibilidade de desatualização das informações armazenadas.

## 4. Persistência e auditoria

O PostgreSQL foi escolhido como banco relacional, utilizando o Django ORM para o gerenciamento das entidades e dos relacionamentos.

A utilização do ORM facilita a integração entre o ETL e a futura API REST. As operações de carga foram estruturadas com transações e mecanismos de criação ou atualização de registros, buscando evitar duplicidades em execuções sequenciais.

As transformações são registradas em uma tabela de auditoria, contendo identificação do cliente, campo analisado, valor original, valor tratado, fonte de referência, critério e status.

Embora essa estratégia aumente a quantidade de informações armazenadas, ela possibilita acompanhar e justificar as decisões realizadas durante o processamento.

## 5. Testes e limitações

Foram desenvolvidos testes unitários, testes de integração e testes de banco de dados. As chamadas externas são simuladas por meio de mocks, permitindo verificar comportamentos esperados e falhas sem depender de conexão com a internet.

Os testes simulados, contudo, não substituem a verificação das respostas reais do serviço externo.

Entre as limitações da solução, destacam-se a necessidade de revisão manual dos casos ambíguos, a manutenção do dicionário de bairros, a ausência de atualização automática do cache e a necessidade de uma política de reimportação após o início das operações da API.

## 6. Considerações finais

As decisões propostas priorizam a preservação dos registros, a transparência das transformações e a qualidade das informações. A estratégia conservadora procura evitar alterações indevidas e estabelecer uma base relacional adequada para o desenvolvimento da API REST.