from src.tsne import t_sne, plot_tsne_2d, plot_tsne_3d
from src.utils import get_data_path


def test_t_sne_wrong_file():
    assert t_sne(get_data_path() / "test/this_file_does_not_exist.json", 2) is None


def test_t_sne():
    coordinates_2d = t_sne(get_data_path() / "test/some_vectors.json", 2)
    assert coordinates_2d.shape == (3, 2)
    plot_tsne_2d(coordinates_2d, "test_t_sne.png")

    coordinates_3d = t_sne(get_data_path() / "test/some_vectors.json", 3)
    assert coordinates_3d.shape == (3, 3)
    plot_tsne_3d(coordinates_3d, "test_t_sne_3d.png")
