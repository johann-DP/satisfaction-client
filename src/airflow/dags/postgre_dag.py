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
    'postgre_dag',
    default_args=default_args,
    description='DAG for PostgreSQL Docker container',
    schedule_interval=timedelta(days=7),
    catchup=False
)

postgre_task = DockerOperator(
    task_id='run_postgre_docker',
    image='bost67dst/postgre_loading',
    auto_remove='success',
    command='/bin/bash -c "python src/postgre/CreatePostgre.py"',
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
         'DB_HOST': 'postgres',
         'DB_PORT': '5432',
         'DB_NAME': 'airflow',
         'DB_USER': 'airflow',
         'DB_PASSWORD': 'airflow'
     },
    dag=dag,
)
