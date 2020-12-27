import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Callable, Union, Sequence, Optional, Tuple

from src.modules.tsne import read_samples_vectors
from src.utils import PipelineStepInterface, safe_w_open


def base_manhattan_dist(seq_top: List[Union[int, float]], seq_bottom: List[Union[int, float]]) -> float:
    assert len(seq_bottom) == len(seq_top), "wrong input data: seq_top, seq_bottom must be of the same length"
    result = 0
    for idx in range(len(seq_top)):
        result += abs(seq_top[idx] - seq_bottom[idx])
    return float(result)


def manhattan_dist(seq_top: List[int], seq_bottom: List[int]) -> float:
    assert len(seq_bottom) == len(seq_top), "wrong input data: seq_top, seq_bottom must be of the same length"
    result = 0
    for idx in range(len(seq_top)):
        result += abs(seq_top[idx] - seq_bottom[idx])
    return float(result)


def convert_alleles_to_weights(seq_top: List[int], seq_bottom: List[int]) -> Tuple[List[float], List[float]]:
    allele_to_weight = {0: 0.0, 1: 0.1, 2: 1.0}
    for seq in seq_bottom, seq_top:
        for x in seq:
            assert x in allele_to_weight.keys(), "wrong feature vector format for this metrics"
    seq_top = [allele_to_weight[x] for x in seq_top]
    seq_bottom = [allele_to_weight[x] for x in seq_bottom]
    return seq_top, seq_bottom


def dist_with_allele(seq_top: List[int], seq_bottom: List[int]) -> float:
    seq_top, seq_bottom = convert_alleles_to_weights(seq_top, seq_bottom)
    return base_manhattan_dist(seq_top, seq_bottom)


def manhattan_with_impact_decorator(impacts_filename: Path) -> Callable[[List[int], List[int]], int]:
    with open(str(impacts_filename)) as file:
        impacts: List[float] = json.load(file)

    def metric(seq_top: List[int], seq_bottom: List[int]) -> int:
        result = 0
        for idx in range(len(seq_top)):
            result += abs(seq_top[idx] - seq_bottom[idx]) * impacts[idx]
        return result

    return metric


def manhattan_allele_impact_decorator(impacts_filename: Path) -> Callable[[List[int], List[int]], int]:
    with open(str(impacts_filename)) as file:
        impacts: List[float] = json.load(file)

    def metric(seq_top: List[int], seq_bottom: List[int]) -> int:
        seq_top, seq_bottom = convert_alleles_to_weights(seq_top, seq_bottom)
        result = 0
        for idx in range(len(seq_top)):
            result += abs(seq_top[idx] - seq_bottom[idx]) * impacts[idx]
        return result

    return metric


def distance_matrix(samples: Dict[Any, List[int]],
                    metric: Callable[[List[int], List[int]], float]) -> List[List[float]]:
    result = [[0.] * len(samples) for _ in range(len(samples))]
    samples_values = list(samples.values())
    logging.info("dm: start calculating")
    for i, s_i in enumerate(samples_values):
        logging.debug("dm: calculated row #" + str(i))
        for j, s_j in enumerate(samples_values[i + 1:], start=i + 1):
            result[i][j] = result[j][i] = metric(s_i, s_j)
    logging.info("dm: calculated!")
    return result


def write_csv(dm: Sequence[Sequence[Union[int, float]]], output_filename: Path,
              names: Optional[Sequence[int]] = None) -> None:
    element_suffix, line_ending = (";", "\n")
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
    metric: Callable[[List[int], List[int]], float]

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


@dataclass
class DecoratedDMStep(PipelineStepInterface):
    input_samples_vectors_json: Path
    input_annotations: Path
    output_matrix_csv: Path
    metric_decorator: Callable[[Path], Callable[[List[int], List[int]], float]]

    def output_exists(self):
        return self.output_matrix_csv.exists()

    def run(self) -> int:
        try:
            metric = self.metric_decorator(self.input_annotations)
        except Exception as e:
            logging.exception(e)
            return -1
        return DistanceMatrixStep(input_samples_vectors_json=self.input_samples_vectors_json,
                                  output_matrix_csv=self.output_matrix_csv,
                                  metric=metric).run()
