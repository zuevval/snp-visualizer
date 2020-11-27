import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Callable, Union, Sequence

from src.modules.tsne import read_samples_vectors
from src.utils import PipelineStepInterface, safe_w_open


def manhattan_dist(seq_top: List[int], seq_bottom: List[int]) -> int:
    assert len(seq_bottom) == len(seq_top), "wrong input data: seq_top, seq_bottom must be of the same length"
    result = 0
    for idx in range(len(seq_top)):
        result += abs(seq_top[idx] - seq_bottom[idx])
    return result


def distance_matrix(samples: Dict[Any, List[int]], metric: Callable[[List[int], List[int]], int]) -> List[List[int]]:
    result = [[0] * len(samples) for _ in range(len(samples))]
    samples_values = list(samples.values())
    logging.info("dm: start calculating")
    for i, s_i in enumerate(samples_values):
        logging.debug("dm: calculated row #" + str(i))
        for j, s_j in enumerate(samples_values[i + 1:], start=i + 1):
            result[i][j] = result[j][i] = metric(s_i, s_j)
    logging.info("dm: calculated!")
    return result


def write_csv(dm: Sequence[Sequence[Union[int, float]]], output_filename: Path, names: Union[List[int], None] = None,
              elements_integers: bool = True) -> None:
    element_suffix, line_ending = (".;", ".\n") if elements_integers else (";", "\n")
    if names is None:
        names = list([i + 1 for i in range(len(dm))])
    else:
        assert len(names) == len(dm), "names must correspond to distance matrix rows"
    output_filename.parent.mkdir(exist_ok=True)
    with safe_w_open(output_filename) as outfile:
        outfile.write(";" + ";".join([str(i) for i in names]) + "\n")
        for name, row in zip(names, dm):
            outfile.write(str(name) + ";" + element_suffix.join([str(elem) for elem in row]) + line_ending)


@dataclass
class DistanceMatrixStep(PipelineStepInterface):
    input_samples_vectors_json: Path
    output_matrix_csv: Path
    metric: Callable[[List[int], List[int]], int]

    def output_exists(self):
        return self.output_matrix_csv.exists()

    def run(self) -> int:
        try:
            samples_vectors = read_samples_vectors(self.input_samples_vectors_json)
            dm = distance_matrix(samples_vectors,
                                 self.metric)  # type: ignore  # https://github.com/python/mypy/issues/5485
            write_csv(dm, self.output_matrix_csv, names=list(samples_vectors.keys()))
        except Exception as e:
            logging.exception(e)
            return -1
        return 0
