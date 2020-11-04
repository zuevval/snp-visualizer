from time import time
from pathlib import Path

import pytest

from src.tsv_reader import snp_to_lists
from src.distance_matrix import distance_matrix, manhattan_dist
from src.file_writer import matrix_to_file
from test.testing_utils import get_out_path, prepare_test_data, get_data_path, get_out_test_path


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
    matrix_to_file(dm, get_out_test_path() / "snp_matrix.txt")


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
        matrix_to_file(dm, get_out_path() / ("real_data/snp_matrix_" + str(max_samples) + ".txt"))
        elapsed = time()
        print(str(max_samples) + ": " + str(elapsed - start) + " seconds - overall")
        print(str(load_time - start) + ": loading, " + str(dm_time - load_time) + ": dist mtx calc")
