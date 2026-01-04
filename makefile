# Set Up Secrets files with the variables you must initialize
secret:
	@echo "Creating secrets files..."
	@echo "KEY_NAME=organization/organization_example/api_key/api_key_example" >> .env
	@echo "KEY_SECRET=-----BEGIN EC PRIVATE KEY-----\key_secret_example==-----END EC PRIVATE KEY-----\n" >> .env
	@echo "Secrets files created. Please update the .env file with your actual credentials."
