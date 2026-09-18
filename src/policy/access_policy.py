from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
PUBLIC_DIR = (BASE_DIR / "sandbox" / "public").resolve()


def check_file_access(path: str) -> dict:
    target = (BASE_DIR / path).resolve()

    try:
        target.relative_to(PUBLIC_DIR)
        allowed = True
    except ValueError:
        allowed = False

    return {
        "requested_permission": "read",
        "target_resource": path,
        "policy_decision": "ALLOW" if allowed else "DENY",
        "boundary_violation": not allowed
    }