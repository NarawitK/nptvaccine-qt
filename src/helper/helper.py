import os, json
def read_config():
    filepath = os.path.join(os.path.dirname(__file__), os.path.normpath('../config/filter_config.json'))
    try:
        with open(filepath, encoding='utf-8-sig') as f:
            config = json.load(f)
            return config
    except FileNotFoundError as fe:
        raise Exception(fe)