from pathlib import Path


def read_file(path: str) -> str:
    file_path = Path(path)

    if not file_path.exists():
        return "ERROR: File not found."

    return file_path.read_text(encoding="utf-8")