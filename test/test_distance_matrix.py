from time import time
import pytest

from src.modules.distance_matrix import distance_matrix, manhattan_dist, manhattan_with_impact_decorator, write_csv
from src.modules.snp_to_vectors import snp_to_lists
from src.utils import get_data_path, get_out_path
from test.testing_utils import prepare_test_data, get_out_test_path


def test_manhattan_with_impact():
    metric = manhattan_with_impact_decorator(get_data_path() / "test/impacts.json")
    abs_tolerance = 1e-5
    assert abs(metric([0, 0, 0], [1, 1, 1]) - 6) < abs_tolerance
    assert abs(metric([0, -1, 0], [1, 1, 1]) - 8) < abs_tolerance


def test_distance_mtx():
    samples_vectors = prepare_test_data().samples_vectors
    print("loaded " + str(len(samples_vectors)) + " samples")
    dm = distance_matrix(samples_vectors, manhattan_dist)
    assert dm == [
        [0, 3, 4, 3, 1],
        [3, 0, 3, 2, 2],
        [4, 3, 0, 3, 5],
        [3, 2, 3, 0, 4],
        [1, 2, 5, 4, 0],
    ]
    write_csv(dm, get_out_test_path() / "snp_matrix.txt")


@pytest.mark.slow
def test_dm_measure_time():
    for max_samples in (10, 20, 30, 40, 50):
        start = time()
        samples_vectors = snp_to_lists(str(get_data_path() / "real_data/snp_data.tsv"),
                                       str(get_data_path() / "real_data/snp2sample.tsv"),
                                       max_samples=max_samples).samples_vectors
        load_time = time()
        print("loaded " + str(len(samples_vectors)) + " samples")
        dm = distance_matrix(samples_vectors, manhattan_dist)
        dm_time = time()
        write_csv(dm, get_out_path() / ("real_data/snp_matrix_" + str(max_samples) + ".txt"))
        elapsed = time()
        print(str(max_samples) + ": " + str(elapsed - start) + " seconds - overall")
        print(str(load_time - start) + ": loading, " + str(dm_time - load_time) + ": dist mtx calc")
