# Modelo Entidade-Relacionamento (MER)

## Projeto Primora — Distribuidora Vetor

## 1. Objetivo

O Modelo Entidade-Relacionamento tem como objetivo representar conceitualmente os dados utilizados pelo sistema de gerenciamento de clientes e vendedores da Distribuidora Vetor.

## 2. Entidades

### Cliente

Representa os clientes da distribuidora, contendo informações cadastrais, dados de contato, localização, vendedor responsável e situação cadastral.

### Vendedor

Representa os profissionais responsáveis pelo atendimento dos clientes.

### Auditoria

Representa os registros das transformações realizadas durante o processo ETL, permitindo identificar os valores originais, os valores tratados e os critérios utilizados.

### AuditoriaAPI

Representa o histórico das operações de criação, atualização, exclusão e inativação realizadas por meio da API REST.

### Usuário

Representa os usuários cadastrados no sistema, utilizando o mecanismo de autenticação do Django.

### Grupo

Representa a organização dos usuários conforme seus perfis de acesso.

### Token

Representa a credencial utilizada para autenticação na API REST.

## 3. Relacionamentos

- Um vendedor pode atender vários clientes.
- Cada cliente possui um vendedor responsável.
- Um cliente pode possuir vários registros de auditoria do ETL.
- Um usuário pode realizar várias operações registradas na auditoria da API.
- Um usuário pode pertencer a vários grupos.
- Um grupo pode possuir vários usuários.
- Um usuário pode possuir um token de autenticação.

## 4. Regras de negócio

- Cada cliente possui um identificador único.
- O nome do vendedor deve ser único.
- O cliente deve estar associado a um vendedor.
- A exclusão de vendedores com clientes vinculados deve ser impedida.
- A exclusão de clientes é realizada de maneira lógica.
- Os registros de auditoria devem permitir a rastreabilidade das operações.
- As consultas agrupadas devem considerar os clientes ativos.
- As operações de gerenciamento são restritas aos perfis autorizados.

## 5. Considerações

O modelo conceitual foi elaborado considerando a necessidade de organização, integridade e rastreabilidade dos dados, contribuindo para a implementação de um banco de dados relacional consistente.