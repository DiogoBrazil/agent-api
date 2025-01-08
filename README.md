# API de Chatbot com LangChain e FastAPI

Este projeto implementa um chatbot inteligente que utiliza LangChain para processar linguagem natural e interagir com um banco de dados PostgreSQL. O chatbot é capaz de entender perguntas em linguagem natural sobre produtos e retornar informações relevantes do banco de dados.

## Autor
[DiogoBrazil](https://github.com/DiogoBrazil)

## Tecnologias Utilizadas
- Python 3.10
- FastAPI
- LangChain
- PostgreSQL
- Docker
- OpenAI API

## Estrutura do Projeto
```
src/
├── config/          # Configurações do projeto
├── controllers/     # Controladores da API
├── infra/          # Infraestrutura (conexões, etc)
├── interfaces/     # Interfaces e modelos
├── llm/            # Lógica do LangChain e tools
├── repositories/   # Camada de acesso ao banco
├── routes/         # Rotas da API
├── service/        # Lógica de negócio
└── utils/          # Utilitários
```

## Funcionalidades
- Processamento de linguagem natural usando LLM
- Sistema inteligente de busca de produtos
- Integração com banco de dados PostgreSQL
- API REST para interação com o chatbot
- Containerização com Docker

## Pré-requisitos
- Docker e Docker Compose instalados
- Chave de API da OpenAI

## Como Rodar

1. Clone o repositório
```bash
git clone https://github.com/DiogoBrazil/agent-api.git
cd agent-api
```

2. Configure o arquivo .env
```env
DATABASE_URL=postgresql://admin:admin123@db:5432/mydatabase
OPENAI_API_KEY=sua_chave_da_openai
```

3. Inicie os containers
```bash
# Inicia todos os serviços
docker compose up --build

# Ou inicie separadamente
docker compose up db    # Inicia apenas o banco
docker compose up app   # Inicia apenas a aplicação
```

4. Acesse a API
- A API estará disponível em `http://localhost:8000`
- Documentação Swagger: `http://localhost:8000/docs`

## Exemplos de Uso

### Consultando Produtos
```bash
curl -X POST "http://localhost:8000/api/v1/chat/input/" \
     -H "Content-Type: application/json" \
     -d '{"input": "quero ver notebooks disponíveis"}'
```

### Resposta
```json
{
    "message": "Resposta encontrada",
    "data": "Lista de notebooks encontrados...",
    "status_code": 200
}
```

## Estrutura de Banco de Dados
O projeto utiliza um banco PostgreSQL com as seguintes tabelas principais:
- products: Armazena informações dos produtos
- product_categories: Categorias de produtos
- orders: Pedidos realizados
- customers: Informações de clientes

## Autor
[DiogoBrazil](https://github.com/DiogoBrazil)

## Repositório
[agent-api](https://github.com/DiogoBrazil/agent-api)
