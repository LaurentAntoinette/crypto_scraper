-- Initialization script for PostgreSQL database for crypto_scraper
-- This script creates the necessary schema and tables for storing wallet information,
-- transaction history, and currency value history.

-- Create the database, user and schema
CREATE DATABASE airflow_db;

-- CREATE USER airflow WITH PASSWORD 'airflow'; //Pas nécessaire car créé par défaut à l'initialisation
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow;

\c airflow_db;

CREATE SCHEMA crypto_scraper AUTHORIZATION airflow;

-- Table to store wallet informations
CREATE TABLE crypto_scraper.crypto_wallet (
    currency VARCHAR(7) PRIMARY KEY,
    balance DECIMAL(20, 10),
    last_updated TIMESTAMP,
    available_balance DECIMAL(20, 10),
    hold_balance DECIMAL(20, 10)
);

-- Enum type for transaction side
CREATE TYPE transaction_type AS ENUM ('buy', 'sell');
-- Table to store transaction history
CREATE TABLE crypto_scraper.transaction_hist (
    date_tmstp TIMESTAMP,
    product_id VARCHAR(7),
    amount DECIMAL(20, 10),
    side transaction_type,
    PRIMARY KEY (date_tmstp, product_id)
);

-- Table to store currency (crypto) value history
CREATE TABLE crypto_scraper.currency_value_hist (
    date_tmstp TIMESTAMP,
    product_id VARCHAR(7),
    bid DECIMAL(20, 10),
    ask DECIMAL(20, 10),
    PRIMARY KEY (date_tmstp, product_id)
);