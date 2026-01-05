from airflow.hooks.postgres_hook import PostgresHook

def get_postgres_connection():
    try :
        return PostgresHook(postgres_conn_id="local_postgres")
    except Exception as e:
        raise ValueError("Could not get PostgreSQL connection")

def insert_rows_into_crypto_wallet_table(rows: list[tuple]):
    pg_hook = get_postgres_connection()
    insert_query = """
        INSERT INTO crypto_scraper.crypto_wallet (currency, balance, last_updated, available_balance, hold_balance)
        VALUES (%s, %s, to_timestamp(%s), %s, %s)
        ON CONFLICT (currency) DO UPDATE 
        SET balance = EXCLUDED.balance,
            last_updated = EXCLUDED.last_updated,
            available_balance = EXCLUDED.available_balance,
            hold_balance = EXCLUDED.hold_balance;
    """
    try:
        for row in rows:
            pg_hook.run(insert_query, parameters=row)
        return 1
    except Exception as e:
        raise ValueError(f"Error inserting data into PostgreSQL: {e}")