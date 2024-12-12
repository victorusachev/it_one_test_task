import pytest

from it_one_test_task.services.parser import parse_mail_log_entry, parse_mail_log_id_value
from tests.utils import get_test_json


@pytest.mark.parametrize(['log_line', 'expected'], get_test_json('test_parse_mail_log_entry'))
def test_parse_mail_log_entry(log_line, expected):
    log_entry = parse_mail_log_entry(log_line)

    assert log_entry == expected


@pytest.mark.parametrize(['log_line', 'expected'], get_test_json('test_parse_mail_log_id_value'))
def test_parse_mail_log_id_value(log_line, expected):
    log_entry = parse_mail_log_id_value(log_line)

    assert log_entry == expected
