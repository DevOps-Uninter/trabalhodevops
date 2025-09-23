# EasyOrder

> 🎓 Projeto universitário desenvolvido como parte da disciplina de **DevOps**.

O **EasyOrder** é um sistema de gerenciamento de pedidos que simula uma aplicação moderna com integração a práticas DevOps, como CI/CD, monitoramento, filas e gerenciamento seguro de segredos. Ele foi construído com **FastAPI**, utilizando bancos de dados distintos para os ambientes de desenvolvimento e produção.

---

## ⚙️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Framework:** FastAPI
- **Orquestração:** Docker e Docker Compose
- **Migrações de Banco de Dados:** Alembic
- **Infraestrutura como Código (IaC):** Terraform
- **CI/CD:** GitHub Actions
- **Documentação:** Swagger UI
- **Banco de Dados:**
  - SQLite (Desenvolvimento)
  - MySQL (Produção - AWS RDS)
- **Monitoramento e Logs:** AWS CloudWatch
- **Gerenciamento de Segredos:** AWS Secrets Manager
- **Filas de Mensagens:** AWS SQS

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- Docker
- Docker Compose

### 1. Clonar o Repositório

* Via HTTPS

```bash
git clone https://github.com/DevOps-Uninter/trabalhodevops.git
cd trabalhodevops
```
* Via SSH

```bash
git git@github.com:DevOps-Uninter/trabalhodevops.git
cd trabalhodevops
```
### 2. Configuração do ambiente

```bash
python -m venv venv
```

### 3. Executar o Projeto com Docker Compose
Para construir as imagens e iniciar os serviços em segundo plano, execute o seguinte comando:

Bash

docker-compose up -d --build
A aplicação estará disponível em http://localhost:8000.

### 4. Migrações de Banco de Dados

Para aplicar as migrações, entre no contêiner da aplicação e rode o Alembic:

```bash
docker-compose exec <nome_do_servico_da_api> bash
alembic upgrade head
```

## 🧪 Como Rodar os Testes

Os testes automatizados estão na pasta tests/. Para executá-los, use o seguinte comando:

```bash
docker-compose exec <nome_do_servico_da_api> pytest
```

A aplicação estará disponível nos seguintes endereços:

- **API principal:** http://localhost:8000
- **Documentação (Swagger):** http://localhost:8000/docs
- **Documentação (ReDoc):** http://localhost:8000/redoc

---

## 🗂️ Estrutura do Projeto

```
├── alembic/                 # Configurações e versões de migrações do banco de dados
├── app/                     # Código fonte da aplicação
│   ├── routers/             # Rotas da API (pedidos, clientes, etc.)
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── infra/
│   └── terraform/         # Módulos para gerenciamento de infraestrutura
├── tests/                 # Testes unitários e de integração
├── .github/                 # Fluxos de trabalho do GitHub Actions para CI/CD
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
└── requirements.txt
```

## 👨‍🏫 Objetivo Acadêmico

Este projeto é um trabalho prático da disciplina de **DevOps** e tem como foco principal:

- Organização de repositório com Git e GitHub
- Automação de Testes e Integração Contínua (CI/CD): Implementação com GitHub Actions.
- Infraestrutura como Código (IaC): Gerenciamento da infraestrutura com Terraform.
- Orquestração de Aplicações: Uso de Docker e Docker Compose.
- Deploy em Ambiente Cloud: Implantação automatizada na AWS.
- Monitoramento e Alertas: Configuração com AWS CloudWatch.
- Práticas DevOps: Aplicação de conceitos de ponta a ponta no ciclo de vida do software.

# Integrantes do Grupo

- **Weden Gabriel da Silva Gomes**  
  - RU: 4170826  
  - GitHub: [wedengabriel](https://github.com/wedengabriel)

- **Desyree N Garcia Batista**  
  - RU: 986134  
  - GitHub: [desyreegarcia](https://github.com/desyreegarcia)

- **Cleberton Gonçalves da Silva**  
  - RU: 4710627  
  - GitHub: *(não informado)*

- **Lucas Silva**  
  - RU: 4702132  
  - GitHub: [onlyluc](https://github.com/onlyluc)

- **Arissa Andreina Kohata**  
  - RU: 4711950  
  - GitHub: [arissak](https://github.com/arissak)

- **Edi Carlos Celestino Silva**  
  - RU: 4661343  
  - GitHub: [ediicarllos](https://github.com/ediicarllos)

- **Eliseu de Lima Andrade**  
  - RU: 4709242  
  - GitHub: [eliseulima5](https://github.com/eliseulima5) 

- **Jamile Santana da Silva**  
  - RU: 4773362  
  - GitHub: [Jhamyllie](https://github.com/Jhamyllie)
 
-  **LUCAS SILVA**  
  - RU: 4693460  
  - GitHub: [luc4s-jpg] .(https://github.com/luc4s-jpg).
