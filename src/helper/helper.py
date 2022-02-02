import json
import os


def read_json_file(path):
    filepath = os.path.join(os.path.dirname(__file__), os.path.normpath(path))
    try:
        with open(filepath, encoding='utf-8-sig') as f:
            content = json.load(f)
            return content
    except FileNotFoundError as fe:
        raise Exception(fe)


def read_config():
    return read_json_file('../config/filter_config.json')


def read_group_list():
    return read_json_file('../config/person_type.json')
