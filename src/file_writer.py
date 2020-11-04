from pathlib import Path
from typing import List, TextIO, Union


def converting_util():
    # converting data to a format that is readable by Gephi
    for fin_name, fout_name, size in [
        ("snp_matrix.txt", "snp_matrix.csv", 930),
        ("snp_matrix_10.txt", "snp_matrix_10.csv", 11),
    ]:
        with open("../data/out/real_data/" + fin_name) as fin:
            with open("../data/out/real_data/" + fout_name, "w") as fout:
                fout.write(";" + ";".join([str(i) for i in range(1, size)]) + "\n")
                for i_line, line in enumerate(fin):
                    fout.write(str(i_line + 1) + ";" + line.replace(" ", ".;"))


def safe_w_open(filename: Path) -> TextIO:
    filename.parent.mkdir(exist_ok=True)
    return open(str(filename), "w")


def matrix_to_file(mtx: List[List[int]], output_filename: Path) -> None:
    with safe_w_open(output_filename) as outfile:
        for row in mtx:
            outfile.write(" ".join(str(item) for item in row) + "\n")


def write_csv(dm: List[List[int]], output_filename: Path, names: Union[List[int], None] = None) -> None:
    if names is None:
        names = list([i + 1 for i in range(len(dm))])
    else:
        assert len(names) == len(dm), "names must correspond to distance matrix rows"
    output_filename.parent.mkdir(exist_ok=True)
    with safe_w_open(output_filename) as outfile:
        outfile.write(";" + ";".join([str(i) for i in names]) + "\n")
        for name, row in zip(names, dm):
            outfile.write(str(name) + ";" + ".;".join([str(elem) for elem in row]) + ".\n")


if __name__ == "__main__":
    converting_util()
