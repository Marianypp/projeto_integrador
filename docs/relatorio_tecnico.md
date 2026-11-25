# Relatório Técnico — Projeto Primora

## Distribuidora Vetor

**Curso:** Programação Backend com Python e Django

**Integrantes:**
- Felipe Gonçalves Nogueira
- Fernanda Matos Ricarte
- Luiz Davi Oliveira Lima
- Mariany de Paula Pinto
- Wanderson Chaves Alves

**Data:** 25/11/2026

## 1. Introdução

O Projeto Primora foi desenvolvido com o objetivo de solucionar problemas relacionados à qualidade, organização e disponibilização dos dados cadastrais da Distribuidora Vetor.

O desafio consistiu no tratamento de um conjunto de dados de clientes, na organização dessas informações em um banco de dados relacional e no desenvolvimento de uma API REST para consulta e gerenciamento dos registros.

O desenvolvimento foi dividido em duas etapas principais: a implementação do processo ETL e a construção da aplicação backend utilizando Django e Django REST Framework.

## 2. Objetivos

O objetivo geral do projeto foi desenvolver uma solução backend capaz de tratar, armazenar e disponibilizar os dados cadastrais da distribuidora de maneira organizada e segura.

Como objetivos específicos, destacam-se:

- Identificar e tratar inconsistências nos dados originais.
- Normalizar os campos cadastrais.
- Registrar as transformações realizadas.
- Armazenar os dados em um banco relacional.
- Implementar operações de gerenciamento de clientes e vendedores.
- Disponibilizar consultas agrupadas por bairro e vendedor.
- Implementar mecanismos de autenticação e autorização.
- Documentar e validar as funcionalidades desenvolvidas.

## 3. Tecnologias utilizadas

O projeto utilizou Python como linguagem principal de programação, Pandas para manipulação dos dados, Django e Django REST Framework para desenvolvimento da aplicação backend e PostgreSQL para armazenamento das informações.

Também foram utilizados Git e GitHub para controle de versão, drf-spectacular para documentação da API e o serviço ViaCEP como fonte complementar de referência para informações de localização.

## 4. Metodologia de desenvolvimento

O desenvolvimento foi realizado de maneira incremental, iniciando pela análise dos dados originais e pela implementação das regras de tratamento.

Posteriormente, foram definidos os modelos do banco de dados e desenvolvidos os endpoints da API REST.

Ao longo do processo, foram implementados mecanismos de validação, autenticação, autorização, auditoria e testes automatizados.

## 5. Processo ETL

A etapa de extração consistiu na leitura e análise do arquivo CSV original.

Durante a transformação, foram aplicadas regras de normalização aos campos cadastrais, incluindo CNPJ, telefone, CEP, bairro e datas.

O enriquecimento dos dados utilizou informações de referência disponibilizadas pelo ViaCEP, mantendo separadas as informações cadastrais e os resultados das consultas externas.

As transformações realizadas foram registradas por meio de mecanismos de auditoria, contribuindo para a rastreabilidade do processo.

Na etapa de carga, os dados tratados foram armazenados no PostgreSQL.

## 6. Modelagem do banco de dados

O banco de dados foi organizado utilizando entidades relacionadas, incluindo clientes, vendedores e registros de auditoria.

A utilização de chaves primárias e estrangeiras contribuiu para garantir a identificação dos registros e a integridade dos relacionamentos.

O Modelo Entidade-Relacionamento, o Diagrama Entidade-Relacionamento e o dicionário de dados estão disponíveis na documentação do projeto.

## 7. Desenvolvimento da API REST

A API foi desenvolvida utilizando Django REST Framework, permitindo realizar operações de consulta, cadastro, atualização e exclusão de registros.

As funcionalidades incluem gerenciamento de clientes e vendedores, consultas agrupadas, filtros, pesquisa textual e paginação.

A documentação dos endpoints utiliza o padrão OpenAPI, com interfaces Swagger e ReDoc.

## 8. Segurança e auditoria

Foram implementados mecanismos de autenticação e autorização para restringir as operações de acordo com os perfis dos usuários.

As consultas agrupadas permanecem públicas, enquanto as operações cadastrais são controladas pelas permissões definidas na aplicação.

As operações realizadas pela API são registradas em uma estrutura de auditoria específica, permitindo identificar o usuário responsável e as alterações efetuadas.

## 9. Decisões técnicas

Entre as principais decisões técnicas do projeto estão a utilização do PostgreSQL, a separação das auditorias do ETL e da API, a exclusão lógica de clientes e a adoção de uma arquitetura monolítica modular.

Essas escolhas consideraram a complexidade do projeto, a necessidade de integridade dos dados e a facilidade de manutenção da aplicação.

## 10. Validação e resultados

A validação do sistema foi planejada por meio de testes unitários, testes funcionais, testes de segurança e testes de integração.

Os resultados obtidos foram:

- Registros no arquivo original: 47.
- Registros no arquivo tratado: 47.
- Clientes armazenados no PostgreSQL: 47.
- Vendedores cadastrados: 05.
- Testes do ETL aprovados: 36.
- Testes do Django aprovados: 105.
- Reexecução completa do ETL:Realizada.

Os resultados detalhados encontram-se nos relatórios de validação do projeto.

## 11. Desafios encontrados

Durante o desenvolvimento, foram identificados desafios relacionados à padronização dos dados, à configuração do banco de dados, à implementação dos relacionamentos e à integração entre os componentes.

Também foram necessários ajustes nas validações dos serializers, na configuração das permissões e na geração da documentação OpenAPI.

Esses desafios contribuíram para o aprendizado sobre desenvolvimento backend, identificação de erros e manutenção de software.

## 12. Limitações e melhorias futuras

O projeto foi desenvolvido em ambiente acadêmico e possui limitações relacionadas à implantação em produção, ao monitoramento, à autenticação e aos testes de desempenho.

Como melhorias futuras, destacam-se o desenvolvimento de uma interface frontend, a containerização da aplicação, a integração contínua e o aprimoramento dos mecanismos de segurança.

## 13. Conclusão

O desenvolvimento do Projeto Primora possibilitou aplicar conhecimentos relacionados à programação backend, ao tratamento de dados, à modelagem de bancos relacionais e à construção de APIs REST.

A integração entre o processo ETL, o PostgreSQL e a aplicação Django demonstrou a importância da organização dos dados e da separação de responsabilidades no desenvolvimento de sistemas.

Além dos conhecimentos técnicos, o projeto contribuiu para o desenvolvimento de habilidades de resolução de problemas, documentação, testes e trabalho em equipe.

[Complementar a conclusão com os resultados efetivamente confirmados e as eventuais pendências.]

## 14. Referências

DJANGO SOFTWARE FOUNDATION. Django Documentation. Disponível em: https://docs.djangoproject.com/.

DJANGO REST FRAMEWORK. Documentation. Disponível em: https://www.django-rest-framework.org/.

POSTGRESQL GLOBAL DEVELOPMENT GROUP. PostgreSQL Documentation. Disponível em: https://www.postgresql.org/docs/.

PANDAS. Documentation. Disponível em: https://pandas.pydata.org/docs/.

PYTHON SOFTWARE FOUNDATION. Python Documentation. Disponível em: https://docs.python.org/3/.

DRF-SPECTACULAR. Documentation. Disponível em: https://drf-spectacular.readthedocs.io/.

VIACEP. Webservice de CEP. Disponível em: https://viacep.com.br/.