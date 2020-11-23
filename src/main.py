from src.distance_matrix import distance_matrix, manhattan_dist
from src.tsne import t_sne, plot_tsne_2d
from src.tsv_reader import snp_to_lists
from src.file_writer import write_csv, safe_w_open
from src.utils import get_data_path, get_out_path
from datetime import datetime
import json


def data_to_gephi_format():
    print(datetime.now())
    real_data_path = get_data_path() / "real_data"
    snp_info = snp_to_lists(snp_data_filename=str(real_data_path / "snp_data.tsv"),
                            samples_filename=str(real_data_path / "snp2sample.tsv"),
                            annotations_filename=str(real_data_path / "snp_annotation_significant.tsv"))
    print("loaded " + str(len(snp_info.samples_vectors)) + " samples")

    # dump snp_info to json format # TODO move to file_writer
    out_path = get_out_path() / "real_data" / "main"
    samples_vectors_filename = "samples_vectors.json"
    for obj, name in [
        (snp_info.samples_vectors, samples_vectors_filename),
        (snp_info.snp_ids, "snp_ids.json"),
        (snp_info.snp_indices, "snp_indices.json"),
        (snp_info.snp_dic, "snp_dic.json"),
    ]:
        with safe_w_open(out_path / name) as vec_file:
            vec_file.write(json.dumps(obj))

    print(datetime.now())
    dm = distance_matrix(snp_info.samples_vectors, manhattan_dist)
    write_csv(dm, out_path / "snp_matrix_significant.csv", names=list(snp_info.samples_vectors.keys()))
    print(datetime.now())

    if input("run T-SNE? y/n").strip().lower() == "y":
        plot_tsne_2d(t_sne(out_path / samples_vectors_filename, 2), "tsne_filtered_snps.png")


if __name__ == "__main__":
    data_to_gephi_format()
