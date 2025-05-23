from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.models import Variable
import requests
import json
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Argumentos padrão para a DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def get_data_from_mongodb(**context):
    """
    Busca dados do MongoDB em lotes
    """
    mongo_hook = MongoHook(mongo_conn_id='mongo_default')
    collection = mongo_hook.get_collection(
        mongo_collection=Variable.get('MONGO_COLLECTION'),
        mongo_db=Variable.get('MONGO_DB')
    )
    
    # TODO: Implementar lógica de busca em lotes
    return []

def get_data_from_bigquery(**context):
    """
    Busca dados do BigQuery em lotes
    """
    bq_hook = BigQueryHook(gcp_conn_id='google_cloud_default')
    
    # TODO: Implementar lógica de busca em lotes
    return []

def process_batch(**context):
    """
    Processa um lote de registros e envia para a API
    """
    batch = context['task_instance'].xcom_pull(task_ids='fetch_data')
    api_url = Variable.get('API_URL')
    
    try:
        response = requests.post(
            f"{api_url}/api/v1/batch",
            json={
                "records": batch,
                "batch_id": context['task_instance'].task_id
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Erro ao processar lote: {str(e)}")
        raise

# Cria a DAG
with DAG(
    'data_pipeline',
    default_args=default_args,
    description='Pipeline para processar dados do BigQuery/MongoDB para API',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['data_pipeline'],
) as dag:

    # Determina a fonte de dados e busca os dados
    fetch_data = PythonOperator(
        task_id='fetch_data',
        python_callable=get_data_from_mongodb if Variable.get('DATA_SOURCE') == 'mongodb' else get_data_from_bigquery,
    )

    # Processa e envia dados para a API
    process_data = PythonOperator(
        task_id='process_data',
        python_callable=process_batch,
    )

    # Define as dependências das tarefas
    fetch_data >> process_data 