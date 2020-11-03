from pathlib import Path
from typing import List, Dict, Any, Callable


def manhattan_dist(seq_top: List[int], seq_bottom: List[int]) -> int:
    assert len(seq_bottom) == len(seq_top), "wrong input data: seq_top, seq_bottom must be of the same length"
    result = 0
    for idx in range(len(seq_top)):
        result += abs(seq_top[idx] - seq_bottom[idx])
    return result


def distance_matrix(samples: Dict[Any, List[int]], metric: Callable[[List[int], List[int]], int]) -> List[List[int]]:
    result = [[0] * len(samples) for _ in range(len(samples))]
    samples_values = list(samples.values())
    print("dm: start calculating")
    for i, s_i in enumerate(samples_values):
        print('\rdm: ' + str(i), end="")  # TODO logging
        for j, s_j in enumerate(samples_values[i + 1:], start=i + 1):
            result[i][j] = result[j][i] = metric(s_i, s_j)
    print("dm: calculated!")
    return result


def matrix_to_file(mtx: List[List[int]], output_filename: Path) -> None:
    output_filename.parent.mkdir(exist_ok=True)
    with open(str(output_filename), "w") as outfile:
        for row in mtx:
            outfile.write(" ".join(str(item) for item in row) + "\n")
