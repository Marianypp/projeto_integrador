# Projeto Primora — Distribuidora Vetor

Projeto acadêmico de desenvolvimento backend utilizando Python, Django REST Framework e PostgreSQL, com foco no tratamento, armazenamento e gerenciamento de dados cadastrais.

## Sobre o projeto

O Projeto Primora tem como objetivo desenvolver uma solução para o tratamento dos dados de clientes da Distribuidora Vetor e sua disponibilização por meio de uma API REST.

O sistema é dividido em duas etapas:

1. Processo ETL para extração, transformação e carga dos dados.
2. API REST para consulta e gerenciamento das informações armazenadas.

## Funcionalidades

### ETL

- Leitura dos dados originais.
- Normalização dos campos cadastrais.
- Tratamento de inconsistências.
- Enriquecimento com ViaCEP.
- Registro das transformações.
- Carga dos dados no PostgreSQL.

### API REST

- CRUD de clientes.
- CRUD de vendedores.
- Exclusão lógica de clientes.
- Consultas agrupadas por bairro e vendedor.
- Autenticação por token e sessão.
- Controle de acesso por perfil.
- Auditoria das operações.
- Paginação, filtros e pesquisa.
- Documentação Swagger e ReDoc.

## Tecnologias utilizadas

- Python
- Pandas
- Django
- Django REST Framework
- PostgreSQL
- django-filter
- drf-spectacular
- python-dotenv
- ViaCEP
- Git e GitHub

## Pré-requisitos

- Python em versão compatível com as dependências do projeto.
- PostgreSQL.
- Git.
- Ambiente virtual Python.

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

Ative o ambiente virtual no Windows CMD:

```cmd
venv\Scripts\activate.bat
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Configuração do ambiente

Crie o arquivo `.env` a partir do arquivo `.env.example`.

No Windows CMD:

```cmd
copy .env.example .env
```

Execute esse comando somente se ainda não existir um arquivo `.env`.

Configure as credenciais do PostgreSQL e as demais variáveis de ambiente conforme o modelo disponibilizado.

Para gerar uma chave secreta do Django:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Insira a chave gerada na variável `SECRET_KEY`.

O arquivo `.env` não deve ser enviado ao GitHub.

## Banco de dados

Crie o banco de dados e o usuário PostgreSQL conforme as configurações definidas no arquivo `.env`.

Execute as migrations:

```bash
python manage.py migrate
```

Crie um usuário administrador:

```bash
python manage.py createsuperuser
```

## Execução do ETL

[Preservar ou inserir os comandos reais de execução do ETL e de importação dos dados desenvolvidos nas aulas anteriores.]

## Executando o servidor

```bash
python manage.py runserver
```

## Endereços disponíveis

| Serviço      | Endereço                          |
|--------------|-----------------------------------|
| Django Admin | http://127.0.0.1:8000/admin/      |
| Swagger      | http://127.0.0.1:8000/api/docs/   |
| ReDoc        | http://127.0.0.1:8000/api/redoc/  |
| OpenAPI      | http://127.0.0.1:8000/api/schema/ |

## Autenticação e autorização

A API utiliza autenticação por token e sessão.

Para autenticação por token:

`Authorization: Token SEU_TOKEN`

Os perfis de acesso são:

- Visitante: consultas públicas.
- Usuário autenticado: consultas cadastrais.
- Operador: gerenciamento de clientes e vendedores.
- Administrador: gerenciamento e consulta das auditorias.

O grupo `Operadores` deve ser criado no ambiente local e associado aos usuários responsáveis pelas operações de gerenciamento.

## Configuração dos operadores

Acesse o Django Admin, crie o grupo `Operadores` e associe os usuários autorizados.

A criação do token pode ser realizada pelo Django Shell utilizando o modelo Token do Django REST Framework.

Os tokens e as senhas não devem ser compartilhados no repositório.

## Validação do banco de dados

```bash
python manage.py validar_sistema
```

O comando verifica a consistência dos registros e dos agrupamentos sem modificar os dados armazenados.

## Testes automatizados

Execute os testes da aplicação Django:

```bash
python manage.py test clientes -v 2
```

Execute somente os testes de integração:

```bash
python manage.py test clientes.test_integracao -v 2
```

Para executar os testes independentes do ETL, utilize o comando correspondente à estrutura de testes do projeto.

## Documentação OpenAPI

Para atualizar e validar o esquema:

```bash
python manage.py spectacular --file schema.yaml --validate
```

## Estrutura do projeto

```text
projeto-primora/
├── clientes/
├── config/
├── dados/
├── docs/
├── etl/
├── relatorios/
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
├── schema.yaml
└── README.md
```

## Documentação técnica

- [Modelo Entidade-Relacionamento](docs/mer.md)
- [Diagrama Entidade-Relacionamento](docs/der.md)
- [Dicionário de dados](docs/dicionario_dados.md)
- [Arquitetura do sistema](docs/arquitetura.md)
- [Processo ETL](docs/processo_etl.md)
- [Documentação da API](docs/documentacao_api.md)
- [Decisões técnicas e trade-offs](docs/decisoes_tecnicas.md)
- [Relatório técnico](docs/relatorio_tecnico.md)
- [Relatório de integração](relatorios/validacao_integracao.md)

## Limitações e melhorias futuras

O projeto foi desenvolvido para fins acadêmicos, utilizando um ambiente local.

Como possibilidades de evolução, destacam-se a implementação de frontend, a containerização, a integração contínua, o aprimoramento da autenticação e a implantação em ambiente de produção.

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


## Finalidade

Projeto desenvolvido para fins educacionais no curso de Programação Backend com Python e Django.



