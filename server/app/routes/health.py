from fastapi import APIRouter
from app.models.user import HealthResponse
from app.database.connection import create_pg_connection

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    """Check service health and database availability."""
    try:
        conn = create_pg_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version_row = cur.fetchone()
                return HealthResponse(status="ok", db="connected", version=version_row[0])
    except Exception:
        return HealthResponse(status="ok", db="unavailable")