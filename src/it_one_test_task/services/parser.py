import re
from pathlib import Path
from typing import Iterable

LINE_PATTERN = re.compile(
    r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s'
    r'([0-9a-zA-Z]{6}-[0-9a-zA-Z]{6}-[0-9a-zA-Z]{2})?\s?'
    r'(<=|=>|->|\*\*|==)?\s?(.*)$'
)


def parse_mail_log_file(log_path: Path) -> Iterable[dict[str, str]]:
    file_encoding = 'UTF-8'

    with log_path.open('r', encoding=file_encoding) as fp:
        while line := fp.readline().strip():
            yield parse_mail_log_entry(line)


def parse_mail_log_entry(line: str) -> dict[str, str]:
    entry = {}

    if match := re.match(LINE_PATTERN, line):
        created = match.group(1)
        flag = match.group(3)
        remaining_str = match.group(4)

        entry = {
            'created': 'T'.join(created.split(' ')),
            'int_id': match.group(2),
            'flag': flag,
            'str': line.removeprefix(created).strip(),
        }
        if flag == '<=':
            entry['id'] = parse_mail_log_id_value(line)
        else:
            entry['address'] = parse_mail_log_address(remaining_str=remaining_str)

    return entry


def parse_mail_log_id_value(line: str) -> str | None:
    if match := re.match(r'.*\s<=.*\sid=([0-9a-zA-Z@._-]+)"?$', line):
        return match.group(1)


def parse_mail_log_address(remaining_str: str) -> str | None:
    if match := re.match(r'^([\w._%+-]+@[\w.-]+)', remaining_str):
        return match.group(1)
