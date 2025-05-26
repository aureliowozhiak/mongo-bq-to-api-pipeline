# MongoDB/BigQuery to API Pipeline

Este projeto implementa um pipeline de dados que extrai dados do MongoDB ou BigQuery e os envia para uma API. O pipeline é gerenciado pelo Apache Airflow e pode ser facilmente configurado através de variáveis de ambiente.

## Requisitos

- Docker instalado (Windows, Linux ou MacOS)
- Git instalado (opcional, para clonar o repositório)

## Instalação

1. **Instalar o Docker Desktop**:
   - Baixe o Docker Desktop do [site oficial](https://www.docker.com/products/docker-desktop)
   - Execute o instalador e siga as instruções
   - Durante a instalação, certifique-se de que a opção "WSL 2" está selecionada
   - Reinicie seu computador após a instalação

2. **Clonar o repositório** (ou baixar os arquivos):
   ```bash
   git clone https://github.com/aureliowozhiak/mongo-bq-to-api-pipeline
   cd mongo-bq-to-api-pipeline
   ```

## Configuração

O projeto já vem configurado com as seguintes variáveis padrão:

- `MONGO_COLLECTION`: "purchases"
- `MONGO_DB`: "ecommerce"
- `DATA_SOURCE`: "mongodb"
- `BATCH_SIZE`: "500"
- `API_URL`: "http://localhost:8000/api/data"

### Dados de Exemplo

O projeto inclui um conjunto de dados de exemplo de compras de e-commerce com as seguintes características:

- 1000 registros de compras
- Dados gerados nos últimos 30 dias
- Informações incluem:
  - Cliente (nome, email, cidade)
  - Produto (nome, preço, categoria)
  - Quantidade
  - Preço total
  - Data da compra
  - Método de pagamento
  - Status da compra

Os dados são automaticamente carregados no MongoDB durante a inicialização do container.

## Como Executar

1. **Iniciar o projeto**:
   ```bash
   # Parar e remover containers antigos (se existirem)
   docker-compose down --remove-orphans
   
   # Remover volumes antigos (opcional, se quiser começar do zero)
   docker volume prune -f
   
   # Iniciar todos os serviços
   docker-compose up -d
   ```

2. **Verificar se os serviços estão rodando**:
   ```bash
   docker-compose ps
   ```
   Todos os serviços devem mostrar status "Up" ou "healthy".

## Monitoramento

### 1. Logs do Airflow

Para monitorar a execução do pipeline, você pode verificar os logs dos diferentes componentes:

```bash
# Logs do scheduler (gerencia as DAGs)
docker-compose logs -f airflow-scheduler

# Logs do worker (executa as tarefas)
docker-compose logs -f airflow-worker
```

Nos logs do scheduler, você deve ver mensagens como:
- "DAG(s) 'data_pipeline' retrieved from /opt/airflow/dags/data_pipeline.py"
- "Setting next_dagrun for data_pipeline"

Nos logs do worker, você deve ver mensagens sobre a execução das tarefas.

### 2. Verificar a API

A API está disponível na porta 8000. Você pode testar se está funcionando com:

```bash
# Testar o endpoint de saúde
curl http://localhost:8000/health
```
Deve retornar: `{"status": "healthy"}`

### 3. Verificar o MongoDB

Para verificar se os dados estão sendo processados no MongoDB:

```bash
# Conectar ao MongoDB
docker-compose exec mongodb mongosh -u root -p example

# Dentro do shell do MongoDB:
use ecommerce                    # Selecionar o banco de dados
show collections                 # Listar coleções
db.purchases.count()            # Contar total de documentos
db.purchases.findOne()          # Ver um documento de exemplo
db.purchases.find().limit(5)    # Ver os 5 primeiros documentos
```

### 4. Verificar o PostgreSQL (banco do Airflow)

```bash
# Conectar ao PostgreSQL
docker-compose exec postgres psql -U airflow -d airflow

# Dentro do shell do PostgreSQL:
\dt                        # Listar tabelas
SELECT * FROM dag_run;     # Ver execuções das DAGs
```

## Troubleshooting

Se encontrar problemas:

1. **Verificar logs de todos os serviços**:
   ```bash
   docker-compose logs
   ```

2. **Reiniciar serviços específicos**:
   ```bash
   docker-compose restart airflow-scheduler
   docker-compose restart airflow-worker
   ```

3. **Reiniciar todo o projeto**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

4. **Verificar variáveis do Airflow**:
   ```bash
   docker-compose exec airflow-scheduler airflow variables list
   ```

5. **Testar conexão com MongoDB**:
   ```bash
   docker-compose exec airflow-scheduler airflow connections test mongodb_default
   ```

## Estrutura do Projeto

```
.
├── airflow/
│   ├── dags/
│   │   └── data_pipeline.py
│   ├── scripts/
│   │   └── init_variables.sh
│   └── Dockerfile
├── api/
│   └── Dockerfile
├── mongodb/
│   └── init-mongo.js
├── docker-compose.yml
└── README.md
```

## Serviços

- **Airflow Scheduler**: Gerencia o pipeline de dados
- **Airflow Worker**: Executa as tarefas do pipeline
- **MongoDB**: Banco de dados de origem (quando DATA_SOURCE=mongodb)
- **PostgreSQL**: Banco de dados do Airflow
- **Redis**: Broker para o Celery
- **API**: Serviço que recebe os dados processados

## Personalização

### MongoDB

Para usar o MongoDB como fonte de dados:
1. Configure `DATA_SOURCE=mongodb` (já é o padrão)
2. Defina `MONGO_COLLECTION` e `MONGO_DB` no arquivo `init_variables.sh`

### BigQuery

Para usar o BigQuery como fonte de dados:
1. Configure `DATA_SOURCE=bigquery` no arquivo `init_variables.sh`
2. Configure as variáveis do BigQuery:
   - `BQ_PROJECT_ID`
   - `BQ_DATASET`
   - `BQ_TABLE`

### API

A API está configurada para receber dados em `http://localhost:8000/api/data`. Você pode modificar o endpoint no arquivo `init_variables.sh`.

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request