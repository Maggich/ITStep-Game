from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import FRONTEND_ORIGIN
from app.database.connection import wait_for_db
from app.routes import health, users

def create_app() -> FastAPI:
    app = FastAPI(title="ITStep Game API")
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[FRONTEND_ORIGIN, "http://localhost:5173", "http://localhost:80", "http://localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, prefix="/api")
    app.include_router(users.router, prefix="/api")

    @app.on_event("startup")
    def on_startup() -> None:
        """Check database connection on startup (with retries)."""
        try:
            conn = wait_for_db()
            with conn:
                with conn.cursor() as cur:
                    # Check version
                    cur.execute("SELECT version();")
                    version_row = cur.fetchone()
                    print(f"Backend started. Connected to PostgreSQL: {version_row[0]}")

                    # Create users table if not exists
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
            print(f"Failed to connect to database on startup: {exc}")

    return app