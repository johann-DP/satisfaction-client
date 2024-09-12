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
    'scraping_dag',
    default_args=default_args,
    description='DAG for scraping Docker container',
    schedule_interval=timedelta(days=2),
    catchup=False
)

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