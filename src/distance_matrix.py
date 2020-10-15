from pathlib import Path
from time import time
from typing import List, Dict, Any, Callable
from src import snp_to_lists


def manhattan_dist(seq_top: List[int], seq_bottom: List[int]) -> int:
    assert len(seq_bottom) == len(seq_top), "wrong input data: seq_top, seq_bottom must be of the same length"
    result = 0
    for idx in range(len(seq_top)):
        result += abs(seq_top[idx] - seq_bottom[idx])
    return result


def distance_matrix(samples: Dict[Any, List[int]], metric: Callable[[List[int], List[int]], int]) -> List[List[int]]:
    result = [[0] * len(samples) for _ in range(len(samples))]
    samples_values = list(samples.values())
    for i, s_i in enumerate(samples_values):
        # print('dm: ' + str(i))  # TODO logging
        for j, s_j in enumerate(samples_values[i + 1:], start=i + 1):
            result[i][j] = result[j][i] = metric(s_i, s_j)
    return result


def matrix_to_file(mtx: List[List[int]], output_filename: Path) -> None:
    output_filename.parent.mkdir(exist_ok=True)
    with open(str(output_filename), "w") as outfile:
        for row in mtx:
            outfile.write(" ".join(str(item) for item in row) + "\n")


def main():
    from src import snp_to_lists
    _, _, samples_vectors = snp_to_lists("../data/test/snp_data.tsv", "../data/test/snp2sample.tsv")
    print("loaded " + str(len(samples_vectors)) + " samples")
    dm = distance_matrix(samples_vectors, manhattan_dist)
    matrix_to_file(dm, Path("../data/out/test/snp_matrix.txt"))


def measure_time():
    for max_samples in (10, 20, 30, 40, 50):
        start = time()
        _, _, samples_vectors = snp_to_lists("../data/real_data/snp_data.tsv", "../data/real_data/snp2sample.tsv",
                                             max_samples)
        load_time = time()
        print("loaded " + str(len(samples_vectors)) + " samples")
        dm = distance_matrix(samples_vectors, manhattan_dist)
        dm_time = time()
        matrix_to_file(dm, Path("../data/out/real_data/snp_matrix_" + str(max_samples) +".txt"))
        elapsed = time()
        print(str(max_samples) + ": " + str(elapsed - start) + " seconds - overall")
        print(str(load_time - start) + ": loading, " + str(dm_time - load_time) + ": dist mtx calc")


if __name__ == "__main__":
    main()
    measure_time()
