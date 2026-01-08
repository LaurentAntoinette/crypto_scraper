from utils.discord_webhook_call_function import send_discord_notification, SUCCESS_WEBHOOK_URL, WALLET_INFO_WEBHOOK_URL, FAILURE_WEBHOOK_URL
from utils.postgre_interaction_function import insert_rows_into_crypto_wallet_table
from utils.coinbase_api_call_function import coinbase_get_account
from tabulate import tabulate
from airflow.decorators import dag, task
from decimal import Decimal
import pendulum, time

@dag(
    dag_id="coinbase_api_etl_dag",                                                                      # ID du DAG, nom affiché dans l'UI
    schedule=None,                                                                                      # Execution manuelle
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),                                                 # Date de début des executions planifiées mais schedule=None donc ne sert à rien
    catchup=False,                                                                                      # Si n'a pas pu se lancer à l'heure, alors ne s'execute pas
    tags=["extract", "coinbase"],                                                                       # Règle de déclenchement des tâches : démarage si les tâches en amont réussissent
    on_failure_callback= lambda context: send_discord_notification(                                     # Envoi d'une notification Discord en cas d'échec
        FAILURE_WEBHOOK_URL, f"Coinbase Wallet Info ETL process failed: {context['task_instance']}"     # | la notification contient l'id de la tâche ayant échouée
    )
)
def coinbase_api_ETL():
    @task(task_id="coinbase_account_extract_task")
    def extract():
        return coinbase_get_account()

    @task(task_id="coinbase_account_transform_task",trigger_rule="all_success")
    def transform(wallet_data):
        transformed_data = []
        for account in wallet_data['accounts']:

            account_available = Decimal(account['available_balance']['value'])
            account_hold = Decimal(account['hold']['value'])
            balance = account_available + account_hold
            last_updated = int(time.time())

            transformed_data.append((account['currency'], balance, last_updated, account_hold, account_available))
        return transformed_data
    
    @task(task_id="coinbase_account_load_task",trigger_rule="all_success")
    def load(transformed_data):
        # Here we insert the transformed data into the database
        insert_rows_into_crypto_wallet_table(transformed_data)

        # Here we send a Discord notification with the loaded data
        discord_message_table_header = ["Currency", "Balance", "Last Updated", "Hold", "Available"]
        discord_message_table = tabulate(transformed_data, headers=discord_message_table_header, tablefmt="simple")
        send_discord_notification(WALLET_INFO_WEBHOOK_URL, f"Coinbase Wallet Info ETL process loaded the following data:\n\n{discord_message_table}")
        
        # Here we send a Discord notification for the successful completion
        send_discord_notification(SUCCESS_WEBHOOK_URL, "COINBASE Wallet_Info_ETL process completed successfully !")

    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)

dag = coinbase_api_ETL()