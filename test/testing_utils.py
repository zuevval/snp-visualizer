import os
from pathlib import Path
from typing import Tuple, Dict, List, Any

from src import snp_to_lists


def _get_path(arg_name: str, default_value: str) -> Path:
    arg_value = Path(os.environ[arg_name]) if arg_name in os.environ else Path(default_value)
    arg_value.mkdir(parents=True, exist_ok=True)
    return arg_value


def get_out_path() -> Path:
    return _get_path("OUT_PATH", "./out")


def get_data_path() -> Path:
    return _get_path("DATA_PATH", "./data")


def prepare_test_data() -> Tuple[Dict[int, List[Any]], Dict[int, int], Dict[int, List[int]]]:
    return snp_to_lists(str(get_data_path() / "test/snp_data.tsv"),
                        str(get_data_path() / "test/snp2sample.tsv"))
