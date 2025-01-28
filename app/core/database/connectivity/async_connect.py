from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

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
ASYNC_DB_URI = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}?{ssl_mode}"

# db engine
async_db_engine = create_async_engine(ASYNC_DB_URI)

# db session maker with engine created
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_db_engine,
    class_=AsyncSession,
)


# dependency injection
async def get_async_db():
    """
    function to get database session object for database operations
    Yields:
        Session: session object for database operations
    """
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()
