from utils.postgre_interaction_function import insert_rows_into_crypto_wallet_table
from utils.coinbase_api_call_function import coinbase_get_account
from airflow.decorators import dag, task
from decimal import Decimal
import pendulum, time

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
    def transform(wallet_data):
        transformed_data = []
        for account in wallet_data['accounts']:

            account_available = Decimal(account['available_balance']['value'])
            account_hold = Decimal(account['hold']['value'])
            balance = account_available + account_hold
            last_updated = int(time.time())

            transformed_data.append((account['currency'], balance, last_updated, account_hold, account_available))
        return transformed_data
    
    @task(task_id="coinbase_account_load_task")
    def load(transformed_data):
        insert_rows_into_crypto_wallet_table(transformed_data)

    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)

dag = coinbase_api_ETL()