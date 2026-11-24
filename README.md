# Distribuidora Vetor — Desafio Primora

## Orientador
- Diego Martins de Oliveira
  https://github.com/diegomo2

## Integrantes

- Felipe Gonçalves Nogueira
  https://github.com/FelipeGonNog
- Fernanda Matos Ricarte
  https://github.com/fernanda-fmr
- Luiz Davi Oliveira Lima
  https://github.com/luizdavi007
- Mariany de Paula Pinto
  https://github.com/Marianypp
- Wanderson Chaves Alves
  https://github.com/WDChavez

## Sobre o projeto

Projeto desenvolvido como atividade final do curso de programação backend com Python e Django.

A solução tem como objetivo realizar o tratamento dos dados de clientes da Distribuidora Vetor, armazená-los em um banco relacional e disponibilizá-los posteriormente por meio de uma API REST.

## Tecnologias

- Python
- Pandas
- Requests
- PostgreSQL
- Django
- Django ORM
- Psycopg
- Python-dotenv
- Unittest
- Git e GitHub

## Funcionalidades da primeira etapa

- Extração dos dados do CSV original.
- Normalização de CNPJ, telefone, datas, bairros e CEPs.
- Enriquecimento geográfico utilizando ViaCEP.
- Cache de consultas externas.
- Identificação de divergências e pendências.
- Geração de auditoria.
- Persistência dos dados em PostgreSQL.
- Testes automatizados com mocks.
- Relatórios de qualidade dos dados.

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
cd projeto-primora
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração do banco

Crie um banco PostgreSQL chamado `distribuidora_vetor` e um usuário autorizado a utilizá-lo.

Copie o arquivo `.env.example` para `.env` e configure as credenciais locais.

```dotenv
DB_NAME=distribuidora_vetor
DB_USER=vetor_user
DB_PASSWORD=SUA_SENHA
DB_HOST=localhost
DB_PORT=5432
```

Execute as migrations:

```bash
python manage.py migrate
```

## Dados de entrada

O CSV original deve ser disponibilizado no caminho:

`dados/originais/clientes_distribuidora_vetor.csv`

## Execução do ETL

Para executar o processo utilizando as informações disponíveis no cache:

```bash
python manage.py executar_etl
```

Para realizar novas consultas de CEP:

```bash
python manage.py executar_etl --consultar-ceps
```

## Relatório de qualidade

```bash
python -m etl.relatorio_qualidade
```

## Testes automatizados

Testes do ETL:

```bash
python -m unittest discover -s etl/tests -v
```

Testes do banco de dados:

```bash
python manage.py test clientes -v 2
```

O usuário PostgreSQL precisa possuir permissão adequada para a criação do banco temporário de testes.

## Arquivos gerados

- `dados/tratados/clientes_final.csv`
- `relatorios/auditoria_final.csv`
- `relatorios/pendencias_finais.csv`
- `relatorios/qualidade_dados.csv`

## Painel administrativo

Crie um superusuário:

```bash
python manage.py createsuperuser
```

Inicie o servidor:

```bash
python manage.py runserver
```

Acesse:

http://127.0.0.1:8000/admin/

## Documentação

As regras de normalização, decisões de tratamento e limitações encontram-se na pasta `relatorios`.

## Status do projeto

Primeira etapa: ETL e persistência em banco relacional — implementação sujeita à validação final dos testes e dos dados.

Segunda etapa: desenvolvimento da API REST com Django REST Framework.

## API REST — Consultas iniciais

A API REST da Distribuidora Vetor utiliza Django REST Framework para disponibilizar os dados tratados e armazenados no PostgreSQL.

### Executando a API

```bash
python manage.py runserver
```

A aplicação estará disponível localmente em:

http://127.0.0.1:8000/

### Endpoints implementados

| Método | Endpoint                    | Descrição                                     |
|--------|-----------------------------|-----------------------------------------------|
| GET    | /api/status/                | Verifica se a rota de status está respondendo |
| GET    | /api/clientes/              | Lista os clientes cadastrados                 |
| GET    | /api/clientes/{id_cliente}/ | Consulta um cliente específico                |

Os endpoints de leitura disponibilizados nesta etapa permitem acesso sem autenticação, conforme a estratégia inicial do projeto.

As operações de cadastro, atualização e exclusão serão implementadas nas etapas seguintes, juntamente com os mecanismos de autenticação e autorização.

### Testes da API

```bash
python manage.py test clientes.tests.TesteAPIClientes -v 2
```

Os testes verificam a disponibilidade dos endpoints, a listagem e consulta de clientes, a representação dos vendedores relacionados, o tratamento de recursos inexistentes e a restrição de métodos ainda não implementados.

## API REST — Gerenciamento de Vendedores

Nesta etapa do projeto da Distribuidora Vetor, foi desenvolvido o CRUD de vendedores utilizando Django REST Framework (DRF), permitindo realizar operações de cadastro, consulta, atualização e exclusão dos vendedores responsáveis pelos clientes.

A implementação utiliza `ModelViewSet`, `ModelSerializer` e `DefaultRouter`, facilitando a organização do código e a criação automática das rotas da API.

### Endpoints de vendedores

| Método HTTP | Endpoint                         | Descrição                                       | Acesso      |
|-------------|----------------------------------|-------------------------------------------------|-------------|
| GET         | `/api/vendedores/`               | Lista todos os vendedores cadastrados           | Público     |
| GET         | `/api/vendedores/{id}/`          | Consulta um vendedor pelo identificador         | Público     |
| POST        | `/api/vendedores/`               | Cadastra um novo vendedor                       | Autenticado |
| PUT         | `/api/vendedores/{id}/`          | Atualiza os dados de um vendedor                | Autenticado |
| PATCH       | `/api/vendedores/{id}/`          | Atualiza parcialmente os dados de um vendedor   | Autenticado |
| DELETE      | `/api/vendedores/{id}/`          | Exclui um vendedor sem clientes vinculados      | Autenticado |
| GET         | `/api/vendedores/{id}/clientes/` | Lista os clientes ativos vinculados ao vendedor | Público     |

### Relacionamento entre clientes e vendedores

O sistema utiliza um relacionamento de um para muitos (1:N), no qual um vendedor pode ser responsável por vários clientes, enquanto cada cliente possui um vendedor responsável.

Esse relacionamento foi implementado por meio de uma chave estrangeira (`ForeignKey`) no modelo `Cliente`, utilizando `on_delete=models.PROTECT` para preservar a integridade dos dados.

Dessa forma, o sistema impede a exclusão de vendedores que possuem clientes vinculados, inclusive quando esses clientes estão inativos.

### Validação dos dados

O `VendedorSerializer` realiza a validação das informações enviadas à API, incluindo:

- Remoção de espaços desnecessários no nome.
- Verificação de um mínimo de três caracteres para o nome.
- Validação de unicidade do nome conforme a restrição do modelo.

Além disso, a API disponibiliza o campo `quantidade_clientes`, que apresenta o total de clientes ativos associados a cada vendedor.

### Consulta de clientes por vendedor

Foi implementada uma ação personalizada com o decorador `@action`, permitindo consultar os clientes ativos de determinado vendedor.

Exemplo de requisição:

`GET /api/vendedores/1/clientes/`

A resposta é apresentada em formato JSON, contendo os clientes ativos vinculados ao vendedor informado.

### Regras de exclusão

A exclusão de vendedores segue as seguintes regras:

- Vendedores sem clientes vinculados podem ser excluídos.
- Vendedores com clientes vinculados não podem ser excluídos.
- A tentativa de exclusão de um vendedor com clientes retorna uma mensagem de validação.
- As operações de escrita exigem autenticação.

Essas regras foram definidas para evitar inconsistências nos relacionamentos e preservar os dados dos clientes.

### Testes automatizados

Foram preparados testes automatizados utilizando `APITestCase`, do Django REST Framework, para verificar:

- Listagem pública de vendedores.
- Consulta individual de vendedores.
- Cadastro com autenticação.
- Bloqueio de cadastro sem autenticação.
- Validação de nomes inválidos.
- Atualização dos dados.
- Exclusão de vendedores sem clientes.
- Bloqueio de exclusão de vendedores com clientes vinculados.
- Consulta de clientes por vendedor.

Para executar os testes específicos:

```bash
python manage.py test clientes.tests.TesteCRUDVendedores -v 2
```

Para executar todos os testes da aplicação:

```bash
python manage.py test clientes -v 2
```

### Tecnologias utilizadas nesta etapa

- Python
- Django
- Django REST Framework
- PostgreSQL
- Django ORM
- Git e GitHub

### Considerações sobre a implementação

O desenvolvimento do CRUD de vendedores permitiu aplicar conceitos de APIs REST, relacionamentos entre tabelas, validação de dados, autenticação, integridade referencial e testes automatizados.

A funcionalidade também contribui para a organização dos dados da Distribuidora Vetor, permitindo consultar os clientes associados a cada vendedor e evitando a exclusão de registros que possuem vínculos com outras entidades.

## Consultas agrupadas — Clientes por bairro e vendedor

Nesta etapa do projeto, foram implementadas consultas agrupadas utilizando o Django ORM e o Django REST Framework.

O objetivo é disponibilizar informações resumidas sobre os clientes da Distribuidora Vetor, permitindo consultar a distribuição dos clientes ativos por bairro normalizado e por vendedor responsável.

### Endpoints

| Método | Endpoint                                | Descrição                           | Acesso  |
|--------|-----------------------------------------|-------------------------------------|---------|
| GET    | `/api/consultas/clientes-por-bairro/`   | Agrupa clientes ativos por bairro   | Público |
| GET    | `/api/consultas/clientes-por-vendedor/` | Agrupa clientes ativos por vendedor | Público |

### Consulta por bairro

O endpoint `/api/consultas/clientes-por-bairro/` retorna a quantidade de clientes ativos agrupados pelo campo `bairro`.

A consulta utiliza `values()`, `annotate()` e `Count()` do Django ORM.

Clientes inativos e clientes sem bairro informado não são incluídos no agrupamento.

É possível utilizar o parâmetro opcional `bairro` para consultar um bairro específico.

Exemplo:

`GET /api/consultas/clientes-por-bairro/?bairro=Águas Claras`

### Consulta por vendedor

O endpoint `/api/consultas/clientes-por-vendedor/` retorna a quantidade de clientes ativos vinculados a cada vendedor.

A consulta utiliza `Count()` com uma condição `Q()` para considerar somente clientes ativos.

Vendedores sem clientes ativos também são apresentados, com total igual a zero.

É possível utilizar o parâmetro opcional `vendedor_id` para consultar um vendedor específico.

Exemplo:

`GET /api/consultas/clientes-por-vendedor/?vendedor_id=1`

### Regras de negócio

- As consultas agrupadas são públicas e aceitam requisições GET.
- Somente clientes ativos são considerados nas contagens.
- O agrupamento por bairro utiliza os valores normalizados armazenados no banco de dados.
- Clientes sem bairro informado não são contabilizados no agrupamento por bairro.
- Vendedores sem clientes ativos são incluídos na consulta por vendedor.
- Os filtros são opcionais.

### Testes automatizados

Foram criados testes utilizando `APITestCase` para verificar os agrupamentos, os filtros, a exclusão de clientes inativos das contagens e o acesso público aos endpoints.

Para executar os testes específicos:

```bash
python manage.py test clientes.tests.TesteConsultasAgrupadas -v 2
```

Para executar todos os testes da aplicação:

```bash
python manage.py test clientes -v 2
```

### Tecnologias e recursos utilizados

- Python
- Django
- Django REST Framework
- Django ORM
- PostgreSQL
- `values()`
- `annotate()`
- `Count()`
- `Q()`

### Considerações

As consultas agrupadas permitem utilizar os dados normalizados durante o ETL para produzir informações gerenciais sobre a distribuição dos clientes.

A implementação demonstra a integração entre tratamento de dados, persistência em banco relacional e disponibilização de informações por uma API REST.


## Autenticação e segurança da API

A API REST da Distribuidora Vetor utiliza mecanismos de autenticação do Django REST Framework para proteger operações de escrita.

Nesta etapa, foi configurada a autenticação por token (`TokenAuthentication`), permitindo que usuários cadastrados realizem operações autenticadas em clientes e vendedores.

### Métodos de autenticação

A aplicação utiliza:

- `TokenAuthentication`: autenticação por token enviado no cabeçalho HTTP.
- `SessionAuthentication`: autenticação por sessão do Django.

### Regras de acesso

| Operação                                  | Permissão           |
|-------------------------------------------|---------------------|
| Consultar clientes                        | Pública             |
| Consultar vendedores                      | Pública             |
| Consultas agrupadas por bairro e vendedor | Pública             |
| Cadastrar clientes e vendedores           | Usuário autenticado |
| Atualizar clientes e vendedores           | Usuário autenticado |
| Excluir clientes e vendedores             | Usuário autenticado |

### Utilização do token

Para realizar uma operação autenticada, o cliente HTTP deve enviar o cabeçalho:

```http
Authorization: Token SEU_TOKEN_AQUI
```

O token deve ser gerado para um usuário existente no Django.

Por questões de segurança, tokens reais não devem ser publicados no repositório.

### Testes de autenticação

Foram implementados testes automatizados para verificar:

- Acesso público às consultas.
- Bloqueio de operações de escrita sem autenticação.
- Cadastro utilizando token válido.
- Rejeição de token inválido.
- Proteção contra atualização e exclusão não autorizadas.

Para executar os testes específicos:

```bash
python manage.py test clientes.tests.TesteAutenticacaoAPI -v 2
```

Para executar todos os testes:

```bash
python manage.py test clientes -v 2
```

### Considerações de segurança

A autenticação por token foi implementada como parte da proteção inicial da API REST.

Em um ambiente de produção, recomenda-se utilizar HTTPS, proteger os tokens e aplicar controles de acesso mais específicos conforme as funções dos usuários.

Também será necessário revisar a exposição pública de informações pessoais de clientes e implementar mecanismos de auditoria das alterações realizadas.

## Documentação da API — Swagger e ReDoc

A API REST da Distribuidora Vetor possui documentação automática gerada pela biblioteca `drf-spectacular`, utilizando a especificação OpenAPI.

A documentação permite visualizar os endpoints disponíveis, os métodos HTTP, os parâmetros de consulta, os formatos das requisições e respostas e os mecanismos de autenticação.

### Acesso à documentação

Após iniciar o servidor Django, as interfaces podem ser acessadas pelos seguintes endereços:

| Interface       | Endereço                          |
|-----------------|-----------------------------------|
| Swagger UI      | http://127.0.0.1:8000/api/docs/   |
| ReDoc           | http://127.0.0.1:8000/api/redoc/  |
| Esquema OpenAPI | http://127.0.0.1:8000/api/schema/ |

### Organização dos endpoints

A documentação foi organizada em quatro categorias:

- **Status:** verificação do funcionamento da API.
- **Clientes:** gerenciamento dos clientes cadastrados.
- **Vendedores:** gerenciamento dos vendedores responsáveis.
- **Consultas:** agrupamento de clientes por bairro normalizado e vendedor responsável.

### Documentação interativa

O Swagger UI permite executar requisições diretamente pelo navegador, facilitando os testes e a integração com outras aplicações.

As operações de escrita exigem autenticação. Para realizar uma requisição autenticada pelo Swagger, deve-se utilizar o botão `Authorize` e informar a credencial no seguinte formato:

```http
Token SEU_TOKEN_AQUI
```

Tokens reais não devem ser publicados no repositório.

### Documentação personalizada

Foram utilizados os decoradores `extend_schema` e `extend_schema_view` para descrever os endpoints, parâmetros, regras de negócio e formatos de resposta.

Também foram criados serializers específicos para representar os resultados das consultas agrupadas.

### Geração do esquema OpenAPI

Para gerar e validar o arquivo de especificação da API:

```bash
python manage.py spectacular --file schema.yaml --validate
```

O arquivo `schema.yaml` contém a descrição estruturada dos endpoints e pode ser utilizado por ferramentas compatíveis com OpenAPI.

### Testes automatizados

Foram implementados testes para verificar:

- Disponibilidade do esquema OpenAPI.
- Disponibilidade do Swagger UI.
- Disponibilidade do ReDoc.
- Presença dos principais endpoints na documentação.
- Documentação dos parâmetros de consulta.
- Presença do mecanismo de autenticação por token.

Para executar os testes específicos:

```bash
python manage.py test clientes.tests.TesteDocumentacaoAPI -v 2
```

Para executar todos os testes da aplicação:

```bash
python manage.py test clientes -v 2
```

### Tecnologias utilizadas

- Python
- Django
- Django REST Framework
- PostgreSQL
- drf-spectacular
- OpenAPI
- Swagger UI
- ReDoc

### Considerações

A documentação automática contribui para a manutenção, organização e integração da API REST, permitindo que desenvolvedores e avaliadores compreendam e testem as funcionalidades implementadas no Projeto Primora.

## Auditoria e rastreabilidade das operações da API

Nesta etapa do Projeto Primora, foi implementado um mecanismo de auditoria para registrar as operações de criação, atualização, exclusão e inativação realizadas pela API REST da Distribuidora Vetor.

O objetivo é garantir maior rastreabilidade das alterações, permitindo identificar os dados anteriores e posteriores, os campos modificados, o usuário responsável e a data e o horário da operação.

### Modelo de auditoria

Foi criado o modelo `AuditoriaAPI`, responsável pelo armazenamento do histórico das operações realizadas nos endpoints de clientes e vendedores.

Cada registro de auditoria contém:

- Entidade afetada.
- Identificador do registro.
- Tipo de operação.
- Usuário responsável.
- Nome do usuário no momento da operação.
- Dados anteriores.
- Dados posteriores.
- Campos alterados.
- Método HTTP.
- Data e horário do registro.

### Tipos de operações auditadas

| Operação    | Descrição                               |
|-------------|-----------------------------------------|
| CRIACAO     | Cadastro de um novo cliente ou vendedor |
| ATUALIZACAO | Alteração dos dados de um registro      |
| INATIVACAO  | Exclusão lógica de um cliente           |
| EXCLUSAO    | Exclusão física de um vendedor          |

Atualizações que não modificam efetivamente os dados não geram novos registros de auditoria.

### Camada de serviços

Foi criado o arquivo `clientes/services.py`, responsável por centralizar as funções de captura de dados, identificação dos campos alterados e registro das auditorias.

Essa organização contribui para a reutilização do código e a separação de responsabilidades.

### Integridade das operações

As operações de alteração e registro de auditoria utilizam `transaction.atomic()`, garantindo que ambas sejam concluídas dentro da mesma transação.

Caso ocorra uma falha durante o registro da auditoria, a alteração correspondente será desfeita.

Também foi utilizado `select_for_update()` para bloquear registros durante determinadas operações de atualização e exclusão.

### Endpoints de auditoria

| Método | Endpoint                | Descrição                       | Acesso        |
|--------|-------------------------|---------------------------------|---------------|
| GET    | `/api/auditorias/`      | Lista os registros de auditoria | Administrador |
| GET    | `/api/auditorias/{id}/` | Consulta um registro específico | Administrador |

### Filtros disponíveis

- `entidade`: Cliente ou Vendedor.
- `operacao`: tipo de operação realizada.
- `identificador`: identificador do registro auditado.

Exemplos:

`GET /api/auditorias/?entidade=Cliente`

`GET /api/auditorias/?operacao=ATUALIZACAO`

`GET /api/auditorias/?entidade=Cliente&identificador=CLI001`

### Segurança

Os endpoints de auditoria utilizam `ReadOnlyModelViewSet` e `IsAdminUser`, permitindo somente consultas realizadas por usuários autenticados com `is_staff=True`.

O histórico também está disponível no Django Admin para usuários com permissão de visualização.

A criação manual, a atualização e a exclusão dos registros de auditoria foram bloqueadas nessas interfaces.

### Auditoria do ETL e da API

A auditoria das operações da API foi implementada separadamente da auditoria do ETL.

Enquanto a auditoria do ETL registra as transformações realizadas nos dados originais, a auditoria da API registra as alterações realizadas pelos usuários autenticados.

A implementação atual não contempla alterações realizadas diretamente pelo banco de dados, Django Shell ou edição de clientes e vendedores pelo Django Admin.

### Testes automatizados

Foram implementados testes para verificar:

- Auditoria de cadastro de clientes e vendedores.
- Auditoria de atualização de clientes e vendedores.
- Auditoria de inativação de clientes.
- Auditoria de exclusão de vendedores.
- Preservação das regras de integridade referencial.
- Identificação de atualizações sem mudanças efetivas.
- Controle de acesso ao histórico.
- Bloqueio de operações de escrita no endpoint de auditoria.
- Rollback da transação em caso de falha no registro da auditoria.

Para executar os testes específicos:

```bash
python manage.py test clientes.tests.TesteAuditoriaAPI -v 2
```

Para executar todos os testes da aplicação:

```bash
python manage.py test clientes -v 2
```

### Considerações

A implementação da auditoria contribui para a rastreabilidade, a integridade e a confiabilidade das informações gerenciadas pela API REST.

Em um ambiente de produção, deverão ser considerados mecanismos adicionais de proteção do histórico, controle de acesso, retenção de dados e adequação à Lei Geral de Proteção de Dados Pessoais (LGPD).


## Paginação, filtros, pesquisa e ordenação da API

Nesta etapa do Projeto Primora, foram implementados recursos de paginação, filtragem, pesquisa textual e ordenação dinâmica, com o objetivo de melhorar a eficiência da API REST e facilitar a consulta às informações da Distribuidora Vetor.

### Paginação

A paginação foi implementada utilizando `PageNumberPagination`, do Django REST Framework.

| Recurso                           | Registros por página |
|-----------------------------------|----------------------|
| Clientes                          | 10                   |
| Vendedores                        | 10                   |
| Clientes vinculados a um vendedor | 10                   |
| Auditorias da API                 | 20                   |

O parâmetro `page_size` permite personalizar a quantidade de registros por página, respeitando o limite máximo de 100 registros por requisição.

Exemplos:

`GET /api/clientes/?page=2`

`GET /api/clientes/?page_size=5`

As respostas paginadas apresentam os seguintes campos:

- `count`: quantidade total de registros encontrados.
- `next`: endereço da próxima página.
- `previous`: endereço da página anterior.
- `results`: registros da página atual.

### Filtros de clientes

Foi utilizada a biblioteca `django-filter` para implementar filtros personalizados.

| Parâmetro     | Finalidade                             |
|---------------|----------------------------------------|
| bairro        | Filtrar pelo bairro normalizado        |
| cidade        | Filtrar pela cidade                    |
| uf            | Filtrar pela unidade federativa        |
| vendedor_id   | Filtrar pelo identificador do vendedor |
| vendedor_nome | Filtrar pelo nome do vendedor          |
| cnpj          | Filtrar pelo CNPJ normalizado          |
| data_inicio   | Definir a data inicial de cadastro     |
| data_fim      | Definir a data final de cadastro       |

Exemplos:

`GET /api/clientes/?bairro=Taguatinga`

`GET /api/clientes/?vendedor_id=1`

`GET /api/clientes/?data_inicio=2024-01-01&data_fim=2024-12-31`

### Pesquisa textual

A pesquisa textual foi implementada utilizando `SearchFilter`.

Os clientes podem ser pesquisados pela razão social, CNPJ, bairro e nome do vendedor responsável.

Exemplo:

`GET /api/clientes/?search=Silva`

### Ordenação dinâmica

A ordenação foi implementada utilizando `OrderingFilter`.

Exemplos:

`GET /api/clientes/?ordering=razao_social`

`GET /api/clientes/?ordering=-razao_social`

`GET /api/vendedores/?ordering=-total_clientes_ativos,id`

O sinal negativo indica ordenação decrescente.

### Combinação de parâmetros

Os recursos de paginação, filtragem, pesquisa e ordenação podem ser utilizados simultaneamente.

Exemplo:

`GET /api/clientes/?bairro=Taguatinga&ordering=razao_social&page_size=5`

### Consultas de auditoria

As consultas de auditoria também possuem paginação, pesquisa textual e ordenação.

Os filtros de entidade, operação e identificador foram preservados.

O acesso permanece restrito a usuários autenticados com `is_staff=True`.

### Otimização de consultas

Foi utilizado `select_related()` para recuperar os dados dos clientes e vendedores relacionados, reduzindo a ocorrência do problema de consultas N+1.

Também foram preservadas as consultas com `annotate()` e `Count()` para calcular a quantidade de clientes ativos vinculados aos vendedores, evitando o carregamento desnecessário dos registros relacionados.

### Consultas agrupadas

Os endpoints de consultas agrupadas por bairro e vendedor mantêm sua estrutura original de resposta, permitindo consultar os totais consolidados sem paginação.

### Testes automatizados

Foram acrescentados testes para validar:

- Paginação padrão e personalizada.
- Limite máximo de registros por página.
- Tratamento de páginas inexistentes.
- Filtros individuais e combinados.
- Pesquisa textual.
- Ordenação dinâmica.
- Filtros por período de cadastro.
- Paginação de clientes, vendedores e auditorias.
- Otimização de consultas ao banco de dados.

Os testes anteriores de listagem foram adaptados à nova estrutura de respostas paginadas.

Para executar os testes específicos:

```bash
python manage.py test clientes.tests.TestePaginacaoFiltrosAPI -v 2
```

Para executar todos os testes da aplicação:

```bash
python manage.py test clientes -v 2
```

### Documentação

Os parâmetros de consulta estão disponíveis na documentação interativa Swagger UI:

http://127.0.0.1:8000/api/docs/

Para atualizar o esquema OpenAPI:

```bash
python manage.py spectacular --file schema.yaml --validate
```

### Considerações

A implementação desses recursos contribui para a escalabilidade, a organização e a eficiência da API REST, preparando o sistema para trabalhar com volumes maiores de dados e facilitando sua integração com aplicações frontend.