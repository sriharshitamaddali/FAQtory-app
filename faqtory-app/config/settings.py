from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
from config.secrets import fetch_secret

class Settings(BaseSettings):

    # ── App ────────────────────────────────────────────
    app_env: str = "local"          # local | staging | production
    app_port: int = 8080
    debug: bool = False

    # ── Secrets ────────────────────────────────────────
    # These hold the KEY NAMES used to look up values in Secrets Manager.
    # In local dev, they hold the actual values directly from .env.local.
    secrets: dict = {}                 # Populated in __init__() from either .env.local or Secrets Manager
    # ── AWS ────────────────────────────────────────────
    aws_region: str = "us-east-1"

    model_config = SettingsConfigDict(
        env_file=f"config/.env.{os.getenv('APP_ENV', 'local')}",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"              # Ignore extra vars injected by Lambda/Docker
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # if self.app_env != "local":
        #     self._load_from_secrets_manager()
        # else:
        self._load_from_env()

    def _load_from_env(self):
        """
        Locally, load secrets from .env.local into the secrets dict.
        Add new keys here as your app evolves — no other changes needed.
        """
        self.secrets = {
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
            # add new secrets here as needed
        }
    
    def _load_from_secrets_manager(self):
        """
        Fetches secrets from AWS Secrets Manager and maps them
        to the corresponding fields on this Settings instance.
        The secret name follows the pattern: my-app/{env}/secrets
        """
        # Parse "DATABASE_URL=my-app/staging/database, API_KEY=my-app/staging/api-key"
        # Into  {"DATABASE_URL": "my-app/staging/database", "API_KEY": "my-app/staging/api-key"}
        mappings = {}
        for entry in self.secret_names.split(","):
            if "=" in entry:
                var_name, secret_path = entry.strip().split("=", 1)
                mappings[var_name.strip()] = secret_path.strip()

        # Fetch each secret and store under its mapped variable name
        for var_name, secret_path in mappings.items():
            secret = fetch_secret(secret_path)
            if isinstance(secret, dict):
                self.secrets.update(secret)               # JSON → merge all key-value pairs
            else:
                self.secrets[var_name.lower()] = secret   # Plain string → use mapped name


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Import this singleton anywhere in your app
settings = get_settings()