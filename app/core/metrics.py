import json
import os
from datetime import datetime
from app.core.config import METRICS_FILE


def log_metric(
    component,
    event,
    data
):

    parent_dir = os.path.dirname(METRICS_FILE)
    if parent_dir:
        os.makedirs(
            parent_dir,
            exist_ok=True
        )

    record = {
        "timestamp": str(
            datetime.now()
        ),
        "component": component,
        "event": event,
        "data": data
    }

    with open(
        METRICS_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(record)
            + "\n"
        )
