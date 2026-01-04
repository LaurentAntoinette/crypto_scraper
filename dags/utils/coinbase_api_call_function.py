from cryptography.hazmat.primitives import serialization
import requests
import secrets
import time
import jwt
import os

key_name       = os.getenv("KEY_NAME")
key_secret     = os.getenv("KEY_SECRET").replace("\\n", "\n")
request_host   = "api.coinbase.com"
request_path   = "/api/v3/brokerage/accounts"

def build_jwt(request_method = "GET"):
    private_key_bytes = key_secret.encode('utf-8')
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    jwt_payload = {
        'sub': key_name,
        'iss': "cdp",
        'nbf': int(time.time()),
        'exp': int(time.time()) + 120,
        'uri': f"{request_method} {request_host}{request_path}",
    }
    jwt_token = jwt.encode(
        jwt_payload,
        private_key,
        algorithm='ES256',
        headers={'kid': key_name, 'nonce': secrets.token_hex()},
    )
    return jwt_token

def coinbase_get_account():
    url = "https://api.coinbase.com/api/v3/brokerage/accounts"
    jwt_token = build_jwt()
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Lève une exception en cas d'erreur HTTP

    data = response.json()
    return data

