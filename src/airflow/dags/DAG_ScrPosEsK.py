from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'combined_dag',
    default_args=default_args,
    description='Combined DAG for scraping, PostgreSQL and ElasticSearch/Kibana',
    schedule_interval=timedelta(days=2),
    catchup=False
)

# Task for scraping
scraping_task = DockerOperator(
    task_id='run_scraping_docker',
    image='bost67dst/scraping_light',
    auto_remove='success',
    command='/bin/bash -c "python /scraping/scraping_bank_json.py"',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    mounts=[Mount(
        source='/home/jo/PycharmProjects/projet_DST_satisfaction_client/data/bank',
        target='/data/bank',
        type='bind'
    )],
    mount_tmp_dir=False,
    working_dir='/',
    dag=dag,
)

# Task for PostgreSQL
postgre_task = DockerOperator(
    task_id='run_postgre_docker',
    image='bost67dst/postgre_loading',
    auto_remove='success',
    command='/bin/bash -c "python src/postgre/CreatePostgre.py"', # pip install psycopg2_binary &&
    docker_url='unix://var/run/docker.sock',
    network_mode="airflow_default",
    mounts=[Mount(
        source='/home/jo/PycharmProjects/projet_DST_satisfaction_client/data/bank/companies',
        target='/data/bank/companies',
        type='bind'
    )],
    mount_tmp_dir=False,
    working_dir='/app',
    environment={
        'DB_PORT': '5432',
        'DB_NAME': 'airflow',
        'DB_USER': 'airflow',
        'DB_PASSWORD': 'airflow',
        'DB_HOST': 'pg-container',
        'unix_socket_directories': '/var/run/postgresql/',
    },
    dag=dag,
)

# FastAPI
fastpai_task = DockerOperator(
    task_id='fastapi',
    image='curlimages/curl:latest',
    command="curl -X POST -i fa-container:8000/predict -H 'Content-Type:application/json' -d '{\"limit\":10}'",
    network_mode='airflow_es-net',
    dag=dag,
)

# Task for MLflow
mlflow_task = BashOperator(
    task_id='mlflow_learning',
    bash_command='docker exec mf-container python3 /app/scripts/extraction_features.py && docker exec mf-container python3 /app/scripts/experiment.py',
    dag=dag,
)

# Task for ElasticSearch/Kibana
elastic_task = DockerOperator(
    task_id='run_elastic_docker',
    image='bost67dst/elastic_loading:latest',
    auto_remove='success',
    command='python3 /src/main.py',
    docker_url='unix://var/run/docker.sock',
    network_mode='airflow_es-net',
    mounts=[
        Mount(source='/home/jo/PycharmProjects/projet_DST_satisfaction_client/data/bank', target='/data/bank', type='bind'),
        Mount(source='/home/jo/PycharmProjects/projet_DST_satisfaction_client/src/elastic', target='/src/elastic', type='bind')
    ],
    mount_tmp_dir=False,
    environment={
        'ELASTICSEARCH_HOST': 'elasticsearch',
        'ELASTICSEARCH_PORT': '9200'
    },
    dag=dag,
)

# Define the task dependencies
scraping_task >> [postgre_task, elastic_task, mlflow_task]
elastic_task >> fastpai_task