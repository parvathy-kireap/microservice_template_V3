from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.shared.exceptions.db_write_fail import DBAWriteFailedException


T = TypeVar('T')


async def add_commit_refresh(db: AsyncSession, obj: T) -> T:
    """
    Add an object to the database, commit the changes, and refresh the object.

    Args:
        db (Session): SQLAlchemy Session object.
        obj (T): Any SQLAlchemy model instance to be added to the database.

    Returns:
        T: The refreshed object after being committed to the database.

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
    """
    try:
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception as e:
        await db.rollback()
        raise DBAWriteFailedException(str(e), code=500)


def commit_and_refresh(db: Session, obj: T) -> T:
    """
    Commit changes to the database and refresh the given object.

    Args:
        db (Session): SQLAlchemy Session object.
        obj (T): Any SQLAlchemy model instance to be committed and refreshed.

    Returns:
        T: The refreshed object after changes have been committed to the
        database.

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
    """
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except Exception as e:
        db.rollback()
        raise DBAWriteFailedException(str(e), code=500)
    
def commit_function(db: Session) -> int:
    """
    Commit changes to the database and refresh the given object.

    Args:
        db (Session): SQLAlchemy Session object.
        obj (T): Any SQLAlchemy model instance to be committed and refreshed.

    Returns:
        T: The refreshed object after changes have been committed to the
        database.

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
    """
    try:
        db.commit()
        # db.refresh(obj)
        return 1
    except Exception as e:
        db.rollback()
        raise DBAWriteFailedException(str(e), code=500)
