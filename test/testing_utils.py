import os
from pathlib import Path

from src.tsv_reader import snp_to_lists, SnpInfo


def _get_path(arg_name: str, default_value: str) -> Path:
    arg_value = Path(os.environ[arg_name]) if arg_name in os.environ else Path(default_value)
    arg_value.mkdir(parents=True, exist_ok=True)
    return arg_value


def get_out_path() -> Path:
    return _get_path("OUT_PATH", "./out")


def get_out_test_path() -> Path:
    out_test_path = get_out_path() / "test"
    out_test_path.mkdir(exist_ok=True)
    return out_test_path


def get_data_path() -> Path:
    return _get_path("DATA_PATH", "./data")


def prepare_test_data(significant_only: bool = False) -> SnpInfo:
    annotations_filename = str(get_data_path() / "test/snp_annotation.tsv") if significant_only else None
    return snp_to_lists(str(get_data_path() / "test/snp_data.tsv"),
                        str(get_data_path() / "test/snp2sample.tsv"),
                        annotations_filename=annotations_filename)
