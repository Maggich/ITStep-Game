from fastapi import APIRouter, HTTPException
from psycopg2.errors import UniqueViolation
from app.models.user import UserCreate, UserOut
from app.database.connection import create_pg_connection

router = APIRouter()

@router.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserCreate) -> UserOut:
    """Create a user. Username and email fields must be unique."""
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
        raise HTTPException(status_code=409, detail="User with this username or email already exists")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error creating user: {exc}")