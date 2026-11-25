# Decisões Técnicas e Trade-offs

## 1. Utilização do PostgreSQL

O PostgreSQL foi escolhido por oferecer recursos de integridade referencial, transações e armazenamento estruturado. Apesar de exigir configuração adicional, proporciona uma base adequada para o gerenciamento dos dados da distribuidora.

## 2. Utilização do Django e Django REST Framework

A escolha dessas tecnologias permitiu utilizar recursos existentes de autenticação, validação, persistência e desenvolvimento de APIs REST, reduzindo a necessidade de implementar esses mecanismos do zero.

## 3. Normalização dos dados

A normalização contribui para melhorar a qualidade das informações e a consistência das consultas. Entretanto, alguns dados inválidos ou divergentes não podem ser corrigidos automaticamente, sendo necessário registrar as inconsistências.

## 4. Enriquecimento com ViaCEP

O ViaCEP foi utilizado como fonte complementar de referência. Optou-se por preservar os dados cadastrais normalizados e armazenar separadamente as informações externas, evitando substituições automáticas potencialmente incorretas.

## 5. Exclusão lógica

A exclusão lógica de clientes permite preservar registros e relacionamentos históricos. Como consequência, as consultas precisam considerar o campo ativo para evitar a apresentação de registros inativados.

## 6. Auditoria

Foram separados os registros de auditoria do ETL e da API, pois representam operações com finalidades diferentes. Essa decisão melhora a rastreabilidade, embora aumente a quantidade de informações armazenadas.

## 7. Controle de acesso

A utilização de perfis de consulta, operação e administração permite restringir ações de acordo com as responsabilidades dos usuários.

A autenticação por token foi considerada adequada ao escopo acadêmico, embora mecanismos adicionais de expiração e renovação possam ser avaliados futuramente.

## 8. Paginação e filtros

A paginação e os filtros contribuem para a eficiência das consultas, evitando o retorno desnecessário de grandes volumes de informações.

## 9. Arquitetura

A arquitetura monolítica modular foi escolhida por apresentar menor complexidade de desenvolvimento, implantação e manutenção para o contexto do projeto.

## 10. Testes automatizados

A implementação de testes automatizados exige tempo adicional de desenvolvimento, mas contribui para identificar regressões e aumentar a confiabilidade do sistema.


## Documentando as limitações e melhorias futuras

### Limitações atuais
|Aspecto     |Limitação                                                          |
|------------|-------------------------------------------------------------------|
|Ambiente    |Desenvolvimento e execução local                                   |
|Autenticação|Tokens sem expiração automática                                    |
|Auditoria   |Não abrange necessariamente alterações diretas pelo Admin ou banco |
|Desempenho  |Ausência de testes de carga abrangentes                            |
|ViaCEP      |Dependência de serviço externo                                     |
|Interface   |Backend sem frontend dedicado                                      |
|Segurança   |Ausência de avaliação completa para produçã                        |
|Implantação |Infraestrutura de produção não validada                            |

### Melhorias futuras
Algumas possibilidades de evolução são:
- Desenvolvimento de uma interface frontend.
- Implementação de autenticação JWT com renovação de tokens.
- Containerização utilizando Docker.
- Configuração de integração contínua com GitHub Actions.
- Implantação em ambiente de produção.
- Monitoramento de desempenho e logs.
- Automação de backups.
- Testes de carga e segurança.
- Aprimoramento da auditoria para outras formas de alteração dos dados.