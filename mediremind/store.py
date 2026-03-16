"""JSON persistence for medication data."""

import json
import os
import re
import tempfile
from pathlib import Path

import gi
gi.require_version("GLib", "2.0")
from gi.repository import GLib

DATA_DIR = Path(GLib.get_user_data_dir()) / "mediremind"
DATA_FILE = DATA_DIR / "medications.json"

TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def validate(name: str, time: str) -> str | None:
    """Return error message or None if valid."""
    if not name or not name.strip():
        return "Name cannot be empty"
    if not TIME_RE.match(time):
        return "Time must be HH:MM (00:00-23:59)"
    return None


def load() -> list[dict]:
    """Load medications from JSON file."""
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def save(medications: list[dict]) -> None:
    """Save medications to JSON file atomically."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=DATA_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(medications, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, DATA_FILE)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
