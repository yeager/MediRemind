"""XDG path helpers for data and cache directories."""

import os


def get_data_dir():
    base = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
    path = os.path.join(base, "mediremind")
    os.makedirs(path, exist_ok=True)
    return path


def get_cache_dir():
    base = os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
    path = os.path.join(base, "mediremind")
    os.makedirs(path, exist_ok=True)
    return path


def get_config_dir():
    base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    path = os.path.join(base, "mediremind")
    os.makedirs(path, exist_ok=True)
    return path


def get_app_data_dir():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "data"
    )
