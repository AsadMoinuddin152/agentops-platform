import json
import os
from datetime import datetime
from app.core.config import LOG_FILE


def log_event(data):

    parent_dir = os.path.dirname(LOG_FILE)
    if parent_dir:
        os.makedirs(
            parent_dir,
            exist_ok=True
        )

    event = {
        "timestamp": str(
            datetime.now()
        ),
        **data
    }

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(event)
            + "\n"
        )