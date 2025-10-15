import os
import time
from typing import Optional
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import connection as Psycopg2Connection


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def create_pg_connection() -> Psycopg2Connection:
    host = get_env("DB_HOST", "localhost")
    port = int(get_env("DB_PORT", "5438"))
    user = get_env("DB_USER", "postgres")
    password = get_env("DB_PASSWORD", "1234")
    dbname = get_env("DB_NAME", "postgres")

    return psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname,
    )


def wait_for_db(max_attempts: int = 10, delay_seconds: float = 1.5) -> Psycopg2Connection:
    last_error: Optional[Exception] = None
    for attempt in range(1, max_attempts + 1):
        try:
            conn = create_pg_connection()
            return conn
        except OperationalError as exc:
            last_error = exc
            time.sleep(delay_seconds)
    assert last_error is not None
    raise last_error


def main() -> None:
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
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

    conn = wait_for_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version_row = cur.fetchone()
            print(f"Connected to PostgreSQL: {version_row[0]}")
    finally:
        conn.close()


if __name__ == "__main__":
    # Если подключение происходит из другого контейнера в той же сети Docker,
    # задайте переменные:
    #   DB_HOST=db, DB_PORT=5432
    # Для подключения с хост-машины через проброс порта
    # подойдут значения по умолчанию:
    #   DB_HOST=localhost, DB_PORT=5438
    main()