import os
from typing import Optional

def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default

def load_root_env_if_present() -> None:
    """Load root .env file if present to share config between server and client."""
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ.setdefault(key, value)

# Database settings
DB_HOST = get_env("DB_HOST", "localhost")
DB_PORT = int(get_env("DB_PORT", "5438"))
DB_USER = get_env("DB_USER", "postgres")
DB_PASSWORD = get_env("DB_PASSWORD", "1234")
DB_NAME = get_env("DB_NAME", "postgres")

# API settings
API_HOST = get_env("API_HOST", "0.0.0.0")
API_PORT = int(get_env("API_PORT", "8080"))
FRONTEND_ORIGIN = get_env("FRONTEND_ORIGIN", "http://localhost:5173").rstrip("/")