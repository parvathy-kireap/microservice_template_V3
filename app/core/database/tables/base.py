from datetime import (
    datetime,
    timezone,
)

from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column

from app.core.database.connectivity.sync_connect import db_base


class Base(db_base):
    __abstract__ = True

    created_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
    )
    updated_at = mapped_column(
        DateTime(),
        default=None,
        onupdate=datetime.now(timezone.utc),
    )
