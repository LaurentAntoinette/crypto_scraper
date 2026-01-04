from utils.coinbase_api_call_function import coinbase_get_account
from airflow.decorators import dag, task
import pendulum

@dag(
    dag_id="coinbase_api_etl_dag",                      # ID du DAG, nom affiché dans l'UI
    schedule=None,                                      # Execution manuelle
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), # Date de début des executions planifiées mais schedule=None donc ne sert à rien
    catchup=False,                                      # Si n'a pas pu se lancer à l'heure, alors ne s'execute pas
    tags=["extract", "coinbase"],                       # Pour recherche depuis le webserveur ou CLI
)
def coinbase_api_ETL():
    @task(task_id="coinbase_account_extract_task")
    def extract():
        return coinbase_get_account()

    @task(task_id="coinbase_account_transform_task")
    def transform():
        pass

    @task(task_id="coinbase_account_load_task")
    def load():
        pass

    extract() >> transform() >> load()

dag = coinbase_api_ETL()