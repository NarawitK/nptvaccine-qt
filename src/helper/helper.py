import json
import os
import platform
import pandas as pd
from dotenv import load_dotenv
from helper.WidgetHelper import show_msg_box
from PySide2.QtWidgets import QMessageBox

load_dotenv()

BASE_CONFIG_PATH = os.getenv("BASE_CONFIG_PATH")
DAILY_CONFIG_FILENAME = os.getenv("DAILY_CONFIG_FILENAME")
WEEKLY_CONFIG_FILENAME = os.getenv("WEEKLY_CONFIG_FILENAME")
GROUP_CONFIG_FILENAME = os.getenv("GROUP_CONFIG_FILENAME")

def read_spreadsheet(filepath):
    try:
        return pd.read_excel(filepath)
    except Exception:
        try:
            return pd.read_csv(filepath)
        except Exception:
            raise Exception("This file cannot be opened as Excel or csv")


def read_json_file(path):
    filepath = os.path.abspath(path)
    try:
        with open(filepath, encoding='utf-8') as f:
            content = json.load(f)
            return content
    except FileNotFoundError as fe:
        show_msg_box(QMessageBox.Critical, "Error", str(fe))
    except PermissionError:
        show_msg_box(QMessageBox.Critical, "Error", "[Permission Error] ไม่สามารถอ่านไฟล์ในตำแหน่งดังกล่าวได้ เนื่องจาก สิทธิ์ใน OS ไม่เพียงพอ")

def write_json_file(path, content):
    filepath = os.path.abspath(path)
    try:
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(content, f, indent=4)
    except FileNotFoundError as fe:
        show_msg_box(QMessageBox.Critical, "Error", str(fe))
    except PermissionError:
        show_msg_box(QMessageBox.Critical, "Error", "[Permission Error] ไม่สามารถเซฟในตำแหน่งดังกล่าวได้ เนื่องจาก ไม่มีสิทธิ์ในการบันทึกไฟล์ใน HDD")
    except Exception:
        show_msg_box(QMessageBox.Critical, "Error", "Unexpected Error Occured.")

def read_config():
    return read_json_file(os.path.join(BASE_CONFIG_PATH, DAILY_CONFIG_FILENAME))


def read_weekly_config():
    return read_json_file(os.path.join(BASE_CONFIG_PATH, WEEKLY_CONFIG_FILENAME))


def read_group_list():
    return read_json_file(os.path.join(BASE_CONFIG_PATH, GROUP_CONFIG_FILENAME))


def write_daily_config(content):
    write_json_file(os.path.join(BASE_CONFIG_PATH, DAILY_CONFIG_FILENAME), content)


def write_weekly_config(content):
    return write_json_file(os.path.join(BASE_CONFIG_PATH, WEEKLY_CONFIG_FILENAME), content)


def write_group_list(content):
    return write_json_file(os.path.join(BASE_CONFIG_PATH, GROUP_CONFIG_FILENAME), content)


def read_os() -> dict:
    return {'os_name': os.name, 'platform_release': platform.release()}


def swap_position(data_list: list, idx1, idx2) -> list:
    data = data_list.pop(idx1)
    if idx1 < idx2:
        data_list.insert(idx2 - 1, data)
    else:
        data_list.insert(idx2, data)
    return data_list
