import time
from typing import Optional
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import connection as Psycopg2Connection

from app.config.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def create_pg_connection() -> Psycopg2Connection:
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
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