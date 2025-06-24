"""CBR utils"""

import os
import sys
from datetime import datetime

from utils.common import load_json_from_file

NEW_WORK_DIR = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(NEW_WORK_DIR)


def get_current_key_rate() -> float:
    """Returns current CBR key rate"""
    json_data = load_json_from_file(os.path.join(NEW_WORK_DIR, "key_rate.json"))

    return json_data["key_rate"]


def get_last_update_key_rate() -> str:
    """Returns last update CBR key rate"""
    json_data = load_json_from_file(os.path.join(NEW_WORK_DIR, "key_rate.json"))
    date = datetime.fromisoformat(json_data["last_update"])
    date_str = datetime.strftime(date, "%d.%m.%Y")
    return date_str
