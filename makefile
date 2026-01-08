# Set Up Secrets files with the variables you must initialize
secrets:
ifneq (,$(wildcard .env))
	@echo ".env file already initialized"
else
	@echo "Creating secrets files..."
	@echo "# Coinbase API credentials" >> .env
	@echo "KEY_NAME=organization/organization_example/api_key/api_key_example" >> .env
	@echo "KEY_SECRET=-----BEGIN EC PRIVATE KEY-----\key_secret_example==-----END EC PRIVATE KEY-----\n" >> .env
	@echo "# Airflow local db connection URL" >> .env
	@echo "AIRFLOW_CONN_LOCAL_POSTGRES=postgresql://airflow:airflow@postgres:5432/airflow_db" >> .env
	@echo "# Discord Webhook URL" >> .env
	@echo "DISCORD_SUCCESS_WEBHOOK_URL=https://discord.com/my/webhook/" >> .env
	@echo "DISCORD_FAILURE_WEBHOOK_URL=https://discord.com/my/webhook/" >> .env
	@echo "DISCORD_WALLET_INFO_WEBHOOK_URL=https://discord.com/my/webhook/" >> .env
	@echo "DISCORD_WALLET_TRANSACTION_WEBHOOK_URL=https://discord.com/my/webhook/" >> .env
	@echo "Secrets files created. Please update now the .env file with real values."
endif

# Just a useful command to gain a few seconds when pushing changes
push:
	@git add .
	@git commit -m "${MSG}"
	@git push origin -u $$(git rev-parse --abbrev-ref HEAD)

docker-compose:
	@if ! docker image inspect airflow_custom_image >/dev/null 2>&1; then \
		echo "Image Airflow manquante, build en cours..."; \
		docker build -t airflow_custom_image .; \
	else \
		echo "Image Airflow déjà présente, pas de build"; \
	fi
	@docker compose up -d