from pathlib import Path

from src.modules.snp_to_vectors import snp_to_lists, SnpInfo
from src.utils import get_out_path, get_data_path


def get_out_test_path() -> Path:
    out_test_path = get_out_path() / "test"
    out_test_path.mkdir(exist_ok=True)
    return out_test_path


def prepare_test_data(significant_only: bool = False) -> SnpInfo:
    annotations_filename = str(get_data_path() / "test/snp_annotation.tsv") if significant_only else None
    return snp_to_lists(str(get_data_path() / "test/snp_data.tsv"),
                        str(get_data_path() / "test/snp2sample.tsv"),
                        annotations_filename=annotations_filename)
