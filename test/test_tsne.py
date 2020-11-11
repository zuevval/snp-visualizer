from src.tsne import t_sne
from test.testing_utils import get_data_path


def test_t_sne_wrong_file():
    assert t_sne(get_data_path() / "test/this_file_does_not_exist.json", "this_file_should_not_exist.png") is None


def test_t_sne():
    coordinates = t_sne(get_data_path() / "test/some_vectors.json", "test_t_sne.png")
    assert coordinates.shape == (3, 2)
