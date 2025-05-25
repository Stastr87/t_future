"""Environment config"""

import os
from sys import path

from env.token import get_token

NEW_WORK_DIR = os.path.abspath(os.path.join(__file__, "../.."))
path.append(NEW_WORK_DIR)

TOKEN = get_token()
LOG_DIR = os.path.join(NEW_WORK_DIR, "logs")
