import boto3
import json
from functools import lru_cache

@lru_cache()
def fetch_secret(secret_name: str) -> dict | str:
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    value = response["SecretString"]

    # Auto-detect plain string vs JSON
    try:
        return json.loads(value)    # JSON secret   → returns dict
    except (json.JSONDecodeError, TypeError):
        return value                # Plain string   → returns str