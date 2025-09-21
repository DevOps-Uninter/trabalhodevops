# EasyOrder

> 🎓 Projeto universitário desenvolvido como parte da disciplina de **DevOps**.

O **EasyOrder** é um sistema de gerenciamento de pedidos que simula uma aplicação moderna com integração a práticas DevOps, como CI/CD, monitoramento, filas e gerenciamento seguro de segredos. Ele foi construído com **FastAPI**, utilizando bancos de dados distintos para os ambientes de desenvolvimento e produção.

---

## ⚙️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Framework:** FastAPI
- **Banco de Dados:**
  - SQLite (Desenvolvimento)
  - MySQL (Produção - AWS RDS)
- **CI/CD:** GitHub Actions
- **Documentação:** Swagger UI
- **Monitoramento e Logs:** AWS CloudWatch
- **Gerenciamento de Segredos:** AWS Secrets Manager
- **Filas de Mensagens:** AWS SQS

---

## 🚀 Como Executar o Projeto Localmente

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
### 2. Criar Ambiente Virtual

```bash
python -m venv venv
```

### 3. Ativar o Ambiente Virtual

- **Linux/macOS**:

```bash
source venv/bin/activate
```

- **Windows**:

```bash
.\venv\Scripts\activate
```

### 4. Instalar as Dependências

```bash
pip install -r requirements.txt
```

---

## 🧪 Rodando a Aplicação

Após configurar o ambiente, execute o servidor de desenvolvimento:

```bash
uvicorn app.main:app --reload
```

A aplicação estará disponível nos seguintes endereços:

- **API principal:** http://localhost:8000
- **Documentação (Swagger):** http://localhost:8000/docs
- **Documentação (ReDoc):** http://localhost:8000/redoc

---

## 🗂️ Estrutura do Projeto (Prevista)

```
easyorder/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── routers/
│   │   ├── pedidos.py
│   │   └── clientes.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 👨‍🏫 Objetivo Acadêmico

Este projeto é um trabalho prático da disciplina de **DevOps** e tem como foco principal:

- Organização de repositório com Git e GitHub
- Automatização de testes e integração contínua com GitHub Actions
- Deploy automatizado em ambiente cloud (AWS)
- Monitoramento e alertas com AWS CloudWatch
- Aplicação de boas práticas DevOps de ponta a ponta no ciclo de vida do software

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
  - GitHub: [eliseulima5] (https://github.com/eliseulima5) 

- **Jamile Santana da Silva**  
  - RU: 4773362  
  - GitHub: [Jhamyllie] (https://github.com/Jhamyllie)
 
-  **LUCAS SILVA**  
  - RU: 4693460  
  - GitHub: [luc4s-jpg] .(https://github.com/luc4s-jpg).
