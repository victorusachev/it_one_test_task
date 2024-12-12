from datetime import datetime
from typing import Optional

from sqlalchemy import CHAR, TIMESTAMP, Boolean, Index, PrimaryKeyConstraint, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CommonColumnsMixin:
    created: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=False)
    int_id: Mapped[str] = mapped_column(CHAR(16), nullable=False)


class Message(CommonColumnsMixin, Base):
    __tablename__ = 'message'

    id: Mapped[str] = mapped_column(String, nullable=False)
    str: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='message_id_pk'),
        Index('message_created_idx', 'created'),
        Index('message_int_id_idx', 'int_id'),
    )


class Log(CommonColumnsMixin, Base):
    __tablename__ = 'log'

    str: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    __table_args__ = (
        Index('log_address_idx', 'address', postgresql_using='hash'),
    )

    __mapper_args__ = {
        'primary_key': ['created', 'int_id', 'address', 'str']
    }
