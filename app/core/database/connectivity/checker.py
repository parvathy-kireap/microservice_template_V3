from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.core.database.connectivity.sync_connect import get_sync_db
from app.shared.logger.setup import app_logger


def check_db_connection(db_session: Session = Depends(get_sync_db)) -> bool:
    """
    this function checks if the database is accessible
    Args:
        db_session (Session, optional): Defaults to Depends on(get_db).

    Returns:
        bool: True if the database is accessible, False otherwise
    """
    try:
        db_session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        app_logger.error(f"Database is not accessible: {e}")
        return False
