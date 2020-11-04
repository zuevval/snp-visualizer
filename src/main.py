from src.distance_matrix import distance_matrix, manhattan_dist
from src.tsv_reader import snp_to_lists
from src.file_writer import write_csv
from test.testing_utils import get_data_path, get_out_path
from datetime import datetime


def data_to_gephi_format():
    print(datetime.now())
    real_data_path = get_data_path() / "real_data"
    snp_info = snp_to_lists(snp_data_filename=str(real_data_path / "snp_data.tsv"),
                            samples_filename=str(real_data_path / "snp2sample.tsv"),
                            annotations_filename=str(real_data_path / "snp_annotation_significant.tsv"))
    print("loaded " + str(len(snp_info.samples_vectors)) + " samples")
    print(datetime.now())
    dm = distance_matrix(snp_info.samples_vectors, manhattan_dist)
    write_csv(dm, get_out_path() / "real_data/snp_matrix_significant.csv", names=list(snp_info.samples_vectors.keys()))
    print(datetime.now())


if __name__ == "__main__":
    data_to_gephi_format()
