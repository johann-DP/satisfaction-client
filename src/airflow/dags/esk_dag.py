from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
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
    'esk_dag',
    default_args=default_args,
    description='DAG for ElasticSearch and Kibana Docker container',
    schedule_interval=timedelta(days=2),
    catchup=False
)

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
