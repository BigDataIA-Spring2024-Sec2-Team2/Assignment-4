import os
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from dags.scripts.demp import print_keys

dag = DAG(
    dag_id="pdf_dag",
    schedule=None,
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
)


with dag:
    hello_world = BashOperator(
        task_id="hello_world",
        bash_command='echo "Hello from airflow"'
    )

    fetch_keys = PythonOperator(
        task_id='fetch_keys',
        python_callable=print_keys,
        provide_context=True,
        dag=dag,
    )

    bye_world = BashOperator(
        task_id="bye_world",
        bash_command='echo "Bye from airflow"'
    )
    
    bye_world_2 = BashOperator(
        task_id="bye_worlds",
        bash_command='echo "Bye from airflow 2"'
    )

    hello_world >> fetch_keys >> bye_world >> bye_world_2
    