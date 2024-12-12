import logging
from datetime import datetime
from typing import TYPE_CHECKING, Iterable

from it_one_test_task.db.models import Base, Log, Message
from it_one_test_task.utils import get_session_manager

if TYPE_CHECKING:
    from it_one_test_task.settings import DatabaseSettings


logger = logging.getLogger(__name__)


async def load_logs_into_db(db_settings: 'DatabaseSettings', logs: Iterable[dict[str, str]]) -> None:
    sessionmanager = get_session_manager(url=db_settings.get_url(), echo=db_settings.log_sql)

    meta = Base.metadata

    async with sessionmanager.connect() as connection:
        await connection.run_sync(meta.drop_all)
        await connection.run_sync(meta.create_all)

    async with sessionmanager.session() as session:
        for entry in logs:
            if not entry['int_id']:
                logger.warning(
                    'Log line skipped because it does not contain a required field: %s %s',
                    entry['created'],
                    entry['str'],
                )
                continue

            if entry['flag'] == '<=':
                if not entry['id']:
                    logger.warning(
                        'Log line skipped because it does not contain a required field: %s %s',
                        entry['created'],
                        entry['str'],
                    )
                    continue

                new_object = Message(
                    created=datetime.fromisoformat(entry['created']),
                    int_id=entry['int_id'],
                    id=entry['id'],
                    str=entry['str'],
                )
            else:
                new_object = Log(
                    created=datetime.fromisoformat(entry['created']),
                    int_id=entry['int_id'],
                    str=entry['str'],
                    address=entry['address'],
                )

            session.add(new_object)

        await session.commit()
