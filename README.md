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