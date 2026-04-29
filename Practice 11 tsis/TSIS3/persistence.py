import json
import hashlib
from pathlib import Path


DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",
    "difficulty": "normal",
}

DIFFICULTY_FACTORS = {
    "easy": 0.85,
    "normal": 1.0,
    "hard": 1.2,
}


def _read_json(path: Path, fallback: dict | list):
    if not path.exists():
        return fallback
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return fallback


def _write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=True, indent=2)


def load_settings(path: Path) -> dict:
    raw = _read_json(path, {})
    settings = DEFAULT_SETTINGS.copy()
    if isinstance(raw, dict):
        settings.update({k: v for k, v in raw.items() if k in settings})
    if settings["difficulty"] not in DIFFICULTY_FACTORS:
        settings["difficulty"] = "normal"
    return settings


def save_settings(path: Path, settings: dict) -> None:
    payload = DEFAULT_SETTINGS.copy()
    payload.update({k: v for k, v in settings.items() if k in payload})
    _write_json(path, payload)


def load_leaderboard(path: Path) -> list[dict]:
    board = _read_json(path, [])
    if not isinstance(board, list):
        return []
    clean_rows = []
    for row in board:
        if not isinstance(row, dict):
            continue
        clean_rows.append(
            {
                "name": str(row.get("name", "Player"))[:18],
                "score": int(row.get("score", 0)),
                "distance": int(row.get("distance", 0)),
                "coins": int(row.get("coins", 0)),
            }
        )
    return sorted(clean_rows, key=lambda item: item["score"], reverse=True)[:10]


def save_leaderboard(path: Path, board: list[dict]) -> None:
    normalized_rows = []
    for row in board:
        name = str(row.get("name", "Player"))[:18]
        normalized_rows.append(
            {
            "name": name,
            "score": int(row.get("score", 0)),
            "distance": int(row.get("distance", 0)),
            "coins": int(row.get("coins", 0)),
            }
        )
    normalized = sorted(normalized_rows, key=lambda item: item["score"], reverse=True)[:10]
    _write_json(path, normalized)


def load_users(path: Path) -> dict[str, str]:
    raw = _read_json(path, {})
    if not isinstance(raw, dict):
        return {}
    users: dict[str, str] = {}
    for username, password_hash in raw.items():
        if not isinstance(username, str) or not isinstance(password_hash, str):
            continue
        users[username[:18]] = password_hash
    return users


def save_users(path: Path, users: dict[str, str]) -> None:
    _write_json(path, users)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(path: Path, username: str, password: str) -> tuple[bool, str]:
    clean_name = username.strip()[:18]
    if len(clean_name) < 3:
        return False, "Username must contain at least 3 chars."
    if len(password) < 4:
        return False, "Password must contain at least 4 chars."
    users = load_users(path)
    if clean_name in users:
        return False, "Username already exists."
    users[clean_name] = hash_password(password)
    save_users(path, users)
    return True, "Registered successfully."


def authenticate_user(path: Path, username: str, password: str) -> bool:
    users = load_users(path)
    clean_name = username.strip()[:18]
    return users.get(clean_name) == hash_password(password)
