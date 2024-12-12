import asyncio
import logging
import sys

from it_one_test_task.log_parser import parse_mail_log_file
from it_one_test_task.services import load_logs_into_db
from it_one_test_task.settings import Settings


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger(__name__)


def run() -> None:
    settings = Settings()

    logger.info('Logfile parsing has started: %s', settings.logfile_path)
    parsed_data = parse_mail_log_file(log_path=settings.logfile_path)
    logger.info('Log file parsing completed')

    logger.info('Loading logs into the DB has started: %s', settings.logfile_path)
    asyncio.run(load_logs_into_db(db_settings=settings.db, logs=parsed_data))
    logger.info('Logs loading completed')
