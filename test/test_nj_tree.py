from pathlib import Path

from src.modules.nj_tree import NjStep
from src.utils import get_data_path
from test.testing_utils import get_out_test_path


def test_nj_tree():
    png_path = Path(get_out_test_path() / "dm_tree.png")
    njs = NjStep(input_dm_csv=get_data_path() / "test/dm_expected.csv",
                 output_dnd=Path(get_out_test_path() / "dm_tree.dnd"),
                 output_png=png_path)
    njs.run()
    assert png_path.exists()
