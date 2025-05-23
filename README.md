# Pipeline de Dados: BigQuery/MongoDB para API

Este projeto implementa um pipeline de dados que processa 10 milhões de registros do BigQuery ou MongoDB, realiza transformações nos dados e envia para uma API em lotes de 500 registros.

## Visão Geral da Arquitetura

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│                 │     │              │     │              │     │              │
│  Fonte de Dados │────▶│    Airflow   │────▶│     API      │────▶│    BD Log    │
│  (BQ/MongoDB)   │     │    DAG       │     │              │     │              │
│                 │     │              │     │              │     │              │
└─────────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

## Funcionalidades

- Suporte para BigQuery e MongoDB como fontes de dados
- Processamento eficiente em lotes (500 registros por requisição à API)
- Registro de respostas da API
- Ambiente de desenvolvimento local com Docker Compose
- Arquitetura escalável

## Pré-requisitos

- Docker
- Docker Compose
- Python 3.8+
- (Opcional) Google Cloud SDK para testes com BigQuery
- (Opcional) Conta MongoDB Atlas para testes com MongoDB

## Configuração do Ambiente de Desenvolvimento

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd mongo-bq-to-api-pipeline
```

2. Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```

3. Inicie o ambiente de desenvolvimento local:
```bash
docker-compose up -d
```

4. Acesse os serviços:
- Interface do Airflow: http://localhost:8080
- API: http://localhost:8000
- MongoDB: localhost:27017
- PostgreSQL (BD de Log): localhost:5432

## Estrutura do Projeto

```
.
├── airflow/
│   ├── dags/
│   │   └── data_pipeline.py
│   └── Dockerfile
├── api/
│   ├── app.py
│   └── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Configuração

O projeto pode ser configurado para usar BigQuery ou MongoDB como fonte de dados. Isso é controlado através de variáveis de ambiente no arquivo `.env`.

### Variáveis de Ambiente

- `DATA_SOURCE`: Escolha entre 'bigquery' ou 'mongodb'
- `BQ_PROJECT_ID`: ID do Projeto Google Cloud (para BigQuery)
- `BQ_DATASET`: Nome do dataset do BigQuery
- `BQ_TABLE`: Nome da tabela do BigQuery
- `MONGO_URI`: String de conexão do MongoDB
- `MONGO_DB`: Nome do banco de dados MongoDB
- `MONGO_COLLECTION`: Nome da coleção MongoDB
- `API_URL`: Endpoint da API alvo
- `BATCH_SIZE`: Número de registros por requisição à API (padrão: 500)

## Desenvolvimento

### Adicionando Novas DAGs

Coloque novos arquivos DAG no diretório `airflow/dags`. Eles serão carregados automaticamente pelo Airflow.

### Testes

1. Testes unitários:
```bash
pytest tests/
```

2. Testes de integração:
```bash
pytest tests/integration/
```

## Implantação em Produção

Para implantação em produção, considere o seguinte:

1. Use serviços gerenciados:
   - Cloud Composer (GCP) ou MWAA (AWS) para Airflow
   - Cloud SQL ou RDS para banco de dados de log
   - Cloud Run ou ECS para implantação da API

2. Considerações de segurança:
   - Use gerenciamento de segredos
   - Implemente funções IAM apropriadas
   - Habilite criptografia em repouso e em trânsito

## Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das suas alterações
4. Faça push para a branch
5. Crie um Pull Request

## Licença

Licença MIT