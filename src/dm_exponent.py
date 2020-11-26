import csv
from math import exp
from pathlib import Path
from src import file_writer
from src.utils import get_out_path


def dm_to_exponent(input_csv: Path, output_csv: Path):
    with open(str(input_csv)) as fin:
        rd = csv.reader(fin, delimiter=";")
        names = [int(elem) for elem in next(rd)[1:]]
        dm = [row[1:] for row in rd]  # distance matrix
    exp_dm = [[exp(float(elem)) for elem in row] for row in dm]
    file_writer.write_csv(exp_dm, output_csv, names=names, elements_integers=False)


if __name__ == "__main__":
    real_data_path = get_out_path() / "real_data"
    dm_to_exponent(real_data_path / "snp_matrix_significant.csv",
                   real_data_path / "snp_matrix_significant_exp.csv")
