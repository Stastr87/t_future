"""Token for t client"""

import json
import os
from sys import path

NEW_WORK_DIR = os.path.abspath(os.path.join(__file__, "../.."))

path.append(NEW_WORK_DIR)


def get_token() -> str:
    """returns T API token"""

    env_var = os.getenv("TToken", default=None)
    if env_var:
        token = env_var
    else:

        with open(
            os.path.join(
                NEW_WORK_DIR,
                "env",
                "key.json",
            ),
            "r",
            encoding="utf8",
        ) as file:
            data = file.read()
            json_data = json.loads(data)
        token = json_data["api_key"]
    return token
