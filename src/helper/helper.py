import json
import os
import pandas as pd


def read_spreadsheet(filepath):
    try:
        _, file_extension = os.path.splitext(filepath)
        if (file_extension == '.xlsx' or file_extension == '.xls'):
                return pd.read_excel(filepath)
        elif (file_extension == '.csv'):
                return pd.read_csv(filepath)
        else:
            raise Exception('Unknown File Extension')
    except:
        raise Exception("Your File is invalid. Maybe not correct file type e.g. it's not an excel but a csv one")
        
def read_json_file(path):
    filepath = os.path.join(os.path.dirname(__file__), os.path.normpath(path))
    try:
        with open(filepath, encoding='utf-8-sig') as f:
            content = json.load(f)
            return content
    except FileNotFoundError as fe:
        raise Exception(fe)

# Will refactor to 'read_daily_config'
def read_config():
    return read_json_file('../config/filter_config.json')

def read_weekly_config():
    return read_json_file('../config/weekly_config.json')

def read_group_list():
    return read_json_file('../config/person_type.json')
