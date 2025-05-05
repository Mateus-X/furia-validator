# Furia Validator

Projeto desenvolvido para validação de dados utilizando FastAPI e Python.

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

Consulte **Instalação** para saber como configurar o projeto.

### 📋 Pré-requisitos

De que coisas você precisa para instalar o software e como instalá-lo?

```
Python 3.10+
Pip
(Dependências: fastapi, uvicorn, python-dotenv, requests, pydantic, mistralai)
```

### 🔧 Instalação

Uma série de exemplos passo-a-passo que informam o que você deve executar para ter um ambiente de desenvolvimento em execução.

1. Clonar o repositório

```bash
$ git clone https://github.com/seu-usuario/furia-validator.git
$ cd furia-validator
```

2. Criar e ativar um ambiente virtual (recomendado)

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

3. Instalar dependências

```bash
$ pip install -r requirements.txt
```

4. Ajustar o arquivo `.env` e atribuir as variáveis de ambiente necessárias (exemplo: MISTRAL_API_KEY)
   Será necessario gerar uma chave da AI Mistral: [guide](https://docs.mistral.ai/getting-started/quickstart/)

```bash
$ cp .env.example .env
$ nano .env
```

1. Rodar o projeto localmente

```bash
$ fastapi dev main.py
```

A API estará disponível em http://localhost:8000

### 🛠️ Testes

Você pode testar os endpoints utilizando o Swagger UI em:

```
http://localhost:8000/docs
```

### 📦 Build

Não é necessário build para aplicações FastAPI. Para produção, recomenda-se rodar com um servidor ASGI como Uvicorn ou Gunicorn.

---

Se precisar de mais detalhes, consulte o código em `main.py`.
