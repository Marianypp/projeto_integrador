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

     ```
     python manage.py collectstatic
     ```
