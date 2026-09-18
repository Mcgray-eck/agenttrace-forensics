import json
from datetime import datetime
from pathlib import Path


def log_event(event: dict) -> None:
    log_path = Path("evidence/events.jsonl")

    event["timestamp"] = datetime.now().isoformat()

    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")