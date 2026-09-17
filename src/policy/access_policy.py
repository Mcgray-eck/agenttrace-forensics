def check_file_access(path: str) -> bool:
    return path.startswith("sandbox/public/")