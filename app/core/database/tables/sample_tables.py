from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.database.tables.base import Base


# schema
schema = 'sample'


class SampleTable(Base):
    __tablename__ = 'sample_table'
    __table_args__ = {'schema': schema}

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=False,
        unique=True,
    )
    name: Mapped[str] = mapped_column(nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
