# Documentação da API REST

## 1. Informações gerais

**Projeto:** Primora — Distribuidora Vetor

**Versão da API:** 1.0.0

**URL base local:** http://127.0.0.1:8000/api/

**Formato de comunicação:** JSON

## 2. Documentação interativa

- Swagger: http://127.0.0.1:8000/api/docs/
- ReDoc: http://127.0.0.1:8000/api/redoc/
- OpenAPI: http://127.0.0.1:8000/api/schema/

## 3. Autenticação

A API utiliza autenticação por token e sessão.

Para realizar requisições autenticadas por token, deve ser utilizado o cabeçalho:

`Authorization: Token SEU_TOKEN`

## 4. Autorização

O sistema possui diferentes perfis de acesso:

- Visitantes: acesso às consultas públicas.
- Usuários autenticados comuns: acesso às consultas cadastrais.
- Operadores: acesso às operações de gerenciamento.
- Administradores: acesso às operações de gerenciamento e auditorias.

## 5. Clientes

| Método | Endpoint                    | Operação            |
|--------|-----------------------------|---------------------|
| GET    | /api/clientes/              | Listagem            |
| GET    | /api/clientes/{id_cliente}/ | Consulta individual |
| POST   | /api/clientes/              | Cadastro            |
| PUT    | /api/clientes/{id_cliente}/ | Atualização         |
| PATCH  | /api/clientes/{id_cliente}/ | Atualização parcial |
| DELETE | /api/clientes/{id_cliente}/ | Inativação          |

## 6. Vendedores

| Método | Endpoint                       | Operação                    |
|--------|--------------------------------|-----------------------------|
| GET    | /api/vendedores/               | Listagem                    |
| GET    | /api/vendedores/{id}/          | Consulta individual         |
| POST   | /api/vendedores/               | Cadastro                    |
| PUT    | /api/vendedores/{id}/          | Atualização                 |
| PATCH  | /api/vendedores/{id}/          | Atualização parcial         |
| DELETE | /api/vendedores/{id}/          | Exclusão                    |
| GET    | /api/vendedores/{id}/clientes/ | Clientes ativos do vendedor |

## 7. Consultas públicas

A API disponibiliza consultas agrupadas por bairro normalizado e vendedor responsável, considerando os clientes ativos.

[Inserir os caminhos reais das rotas obtidos pelo Django Shell.]

## 8. Auditoria

Os administradores podem consultar os registros de auditoria das operações realizadas pela API.

Os registros são disponibilizados exclusivamente para leitura.

## 9. Paginação e filtros

Os endpoints de listagem utilizam paginação, filtros, pesquisa textual e ordenação.

As consultas podem ser personalizadas utilizando parâmetros na URL.

## 10. Tratamento de erros

As respostas de erro tratadas pelo Django REST Framework são padronizadas, incluindo o código HTTP, uma mensagem descritiva e os detalhes disponibilizados pelo mecanismo de validação.

## 11. Especificação OpenAPI

O arquivo `schema.yaml`, localizado na raiz do projeto, contém a especificação técnica da API.

Para atualizar e validar esse arquivo:

`python manage.py spectacular --file schema.yaml --validate`