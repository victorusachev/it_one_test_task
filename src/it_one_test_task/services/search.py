from typing import Iterable

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from it_one_test_task.db.models import Log, Message


async def search_logs_by_email(session: 'AsyncSession', email: str, limit: int) -> Iterable[str]:
    query = (
        sa.select(sa.func.concat(sa.text('created'), sa.literal(' '), sa.text('str')))
        .select_from(
            sa.union(
                sa.select(Log.created, Log.str, Log.int_id).where(Log.address == email),
                sa.select(Message.created, Message.str, Message.int_id).where(Message.str.contains(email)),
            )
        )
        .order_by(sa.text('int_id'), sa.text('created'))
        .limit(limit)
    )
    return (await session.scalars(query)).all()
