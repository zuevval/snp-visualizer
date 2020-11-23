import os
from pathlib import Path


def _get_path(arg_name: str, default_value: str) -> Path:
    arg_value = Path(os.environ[arg_name]) if arg_name in os.environ else Path(default_value)
    arg_value.mkdir(parents=True, exist_ok=True)
    return arg_value


def get_out_path() -> Path:
    return _get_path("OUT_PATH", "./out")


def get_data_path() -> Path:
    return _get_path("DATA_PATH", "./data")
