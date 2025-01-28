from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

from app.shared.helpers.read_env import get_db_creds


# environment variables
DB_CREDS: dict = get_db_creds()
host: str = DB_CREDS['host']
user: str = DB_CREDS['user']
password: str = DB_CREDS['password']
database: str = DB_CREDS['database']
port: int = 5432
ssl_mode: str = "ssl_mode:require"
# connection string
SYNC_DB_URI = f"postgresql://{user}:{password}@{host}:{port}/{database}?{ssl_mode}"


# db engine
sync_db_engine = create_engine(SYNC_DB_URI)


# db session maker with engine created
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_db_engine,
)

# database base for creation of table
db_base = declarative_base()


# dependency injection
def get_sync_db():
    """
    function to get database session object for database operations
    Returns:
        Session: session object for database operations
    """
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
