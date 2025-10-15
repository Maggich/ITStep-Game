import os
import time
from typing import Optional
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import connection as Psycopg2Connection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from psycopg2.errors import UniqueViolation


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


def load_root_env_if_present() -> None:
    """Загрузить корневой .env (если есть), чтобы сервер и клиент делили общий конфиг."""
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


# Инициализируем FastAPI приложение и настраиваем CORS
load_root_env_if_present()
app = FastAPI(title="ITStep Game API")

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173").rstrip("/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    db: str
    version: Optional[str] = None


@app.on_event("startup")
def on_startup() -> None:
    """При старте приложения проверяем подключение к БД (с ретраями)."""
    try:
        conn = wait_for_db()
        with conn:
            with conn.cursor() as cur:
                # Проверяем версию
                cur.execute("SELECT version();")
                version_row = cur.fetchone()
                print(f"Бэкенд запущен. Подключено к PostgreSQL: {version_row[0]}")

                # Создаем таблицу пользователей при отсутствии
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    );
                    """
                )
    except Exception as exc:
        print(f"Не удалось подключиться к БД при старте: {exc}")


@app.get("/api/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    """Проверка здоровья сервиса и доступности БД."""
    try:
        conn = create_pg_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version_row = cur.fetchone()
                return HealthResponse(status="ok", db="connected", version=version_row[0])
    except Exception:
        return HealthResponse(status="ok", db="unavailable")


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: Optional[str] = None


@app.post("/api/users", response_model=UserOut, status_code=201)
def create_user(user: UserCreate) -> UserOut:
    """Создать пользователя. Поля username и email должны быть уникальны."""
    try:
        conn = create_pg_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (username, email, password)
                    VALUES (%s, %s, %s)
                    RETURNING id, username, email, created_at;
                    """,
                    (user.username, user.email, user.password),
                )
                row = cur.fetchone()
                return UserOut(id=row[0], username=row[1], email=row[2], created_at=str(row[3]) if row[3] else None)
    except UniqueViolation:
        # Нарушение уникальности username или email
        # Возвращаем 409 Conflict
        from fastapi import HTTPException

        raise HTTPException(status_code=409, detail="Пользователь с таким username или email уже существует")
    except Exception as exc:
        from fastapi import HTTPException

        raise HTTPException(status_code=500, detail=f"Ошибка при создании пользователя: {exc}")


if __name__ == "__main__":
    # Если подключение происходит из другого контейнера в одной сети Docker:
    #   DB_HOST=db, DB_PORT=5432
    # Для локального запуска через проброс порта подойдут:
    #   DB_HOST=localhost, DB_PORT=5438
    import uvicorn

    api_host = os.getenv("API_HOST", "0.0.0.0")
    api_port = int(os.getenv("API_PORT", "8080"))
    # Запускаем по объекту приложения, чтобы избежать ошибок импорта вида
    # "ModuleNotFoundError: No module named 'server'" при запуске из папки server
    uvicorn.run(app, host=api_host, port=api_port, reload=False)