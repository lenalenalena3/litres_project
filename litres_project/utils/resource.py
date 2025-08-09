import json
from pathlib import Path


def path_schema(file_name):
    return str(
        (Path(__file__).parents[2] / "resources" /"schemas"/file_name).resolve()
    )
def load_data_json_value(file_name):
    file_path = Path(__file__).parents[2]/ "resources" / file_name
    with open(file_path, encoding='utf-8') as f:
        return json.load(f).values()

def load_data_json(file_name):
    file_path = Path(__file__).parents[2]/ "resources" / file_name
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)

