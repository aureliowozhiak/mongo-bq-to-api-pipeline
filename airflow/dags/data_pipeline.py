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

def get_data_from_source(**context):
    data_source = Variable.get('DATA_SOURCE', default_var='mongodb')
    batch_size = int(Variable.get('BATCH_SIZE', default_var='500'))
    
    if data_source == 'mongodb':
        mongo_hook = MongoHook(conn_id='mongodb_default')
        collection = mongo_hook.get_collection(
            mongo_collection=Variable.get('MONGO_COLLECTION'),
            mongo_db=Variable.get('MONGO_DB')
        )
        # Get total count for pagination
        total_docs = collection.count_documents({})
        return {'total': total_docs, 'batch_size': batch_size}
    
    elif data_source == 'bigquery':
        bq_hook = BigQueryHook(gcp_conn_id='google_cloud_default')
        query = f"""
        SELECT COUNT(*) as total
        FROM `{Variable.get('BQ_PROJECT_ID')}.{Variable.get('BQ_DATASET')}.{Variable.get('BQ_TABLE')}`
        """
        result = bq_hook.get_first(query)
        return {'total': result[0], 'batch_size': batch_size}

def process_batch(**context):
    data_source = Variable.get('DATA_SOURCE', default_var='mongodb')
    batch_size = int(Variable.get('BATCH_SIZE', default_var='500'))
    api_url = Variable.get('API_URL')
    
    if data_source == 'mongodb':
        mongo_hook = MongoHook(conn_id='mongodb_default')
        collection = mongo_hook.get_collection(
            mongo_collection=Variable.get('MONGO_COLLECTION'),
            mongo_db=Variable.get('MONGO_DB')
        )
        # Get batch of documents
        documents = list(collection.find().limit(batch_size))
        data = [json.loads(json.dumps(doc, default=str)) for doc in documents]
    
    elif data_source == 'bigquery':
        bq_hook = BigQueryHook(gcp_conn_id='google_cloud_default')
        query = f"""
        SELECT *
        FROM `{Variable.get('BQ_PROJECT_ID')}.{Variable.get('BQ_DATASET')}.{Variable.get('BQ_TABLE')}`
        LIMIT {batch_size}
        """
        data = bq_hook.get_pandas_df(query).to_dict('records')
    
    # Send to API
    response = requests.post(api_url, json=data)
    return response.json()

# Cria a DAG
with DAG(
    'data_pipeline',
    default_args=default_args,
    description='Pipeline to process data from MongoDB/BigQuery to API',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['data_pipeline'],
) as dag:

    get_data_info = PythonOperator(
        task_id='get_data_info',
        python_callable=get_data_from_source,
    )

    process_batch = PythonOperator(
        task_id='process_batch',
        python_callable=process_batch,
    )

    get_data_info >> process_batch 