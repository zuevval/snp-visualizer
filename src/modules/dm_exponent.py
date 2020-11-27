import csv
import logging
from dataclasses import dataclass
from math import exp
from pathlib import Path

import src.modules.distance_matrix
from src.utils import get_out_path, PipelineStepInterface


def dm_to_exponent(input_csv: Path, output_csv: Path):
    with open(str(input_csv)) as fin:
        rd = csv.reader(fin, delimiter=";")
        names = [int(elem) for elem in next(rd)[1:]]
        dm = [row[1:] for row in rd]  # distance matrix
    exp_dm = [[exp(float(elem)) for elem in row] for row in dm]
    src.modules.distance_matrix.write_csv(exp_dm, output_csv, names=names, elements_integers=False)


@dataclass
class DmToExpStep(PipelineStepInterface):
    input_csv: Path
    output_csv: Path

    def output_exists(self):
        return self.output_csv.exists()

    def run(self) -> int:
        try:
            dm_to_exponent(self.input_csv, self.output_csv)
        except Exception as e:
            logging.exception(e)
            return -1
        return 0


if __name__ == "__main__":
    real_data_path = get_out_path() / "real_data"
    dm_to_exponent(real_data_path / "snp_matrix_significant.csv",
                   real_data_path / "snp_matrix_significant_exp.csv")
