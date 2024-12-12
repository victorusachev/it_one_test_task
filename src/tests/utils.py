import json
from pathlib import Path
from typing import Any

TEST_DATA_DIR = Path(__file__).parent / 'data'


def get_test_json(dataset_name: str) -> Any:
    dataset_path = (TEST_DATA_DIR / dataset_name).with_suffix('.json')
    return json.loads(dataset_path.read_text(encoding='UTF-8'))
