from src.modules.distance_matrix import manhattan_dist, DistanceMatrixStep
from src.modules.dm_exponent import DmToExpStep
from src.modules.tsne import TSneStep
from src.modules.snp_to_vectors import SnpToVectorStep
from src.utils import get_data_path, get_out_path, Pipeline


def main():
    out_dir = get_out_path() / "real_pipeline"
    p = Pipeline(out_dir / "pipeline.log")

    tsv_dir = get_data_path() / "real_data"
    json_dir = out_dir / "json"
    t_sne_dir = out_dir / "t_sne"
    snp_vec_json = json_dir / "samples_vectors.json"
    distance_matrix_csv = out_dir / "dm.csv"

    p.add(SnpToVectorStep(
        input_snp_data=tsv_dir / "snp_data.tsv",
        input_samples=tsv_dir / "snp2sample.tsv",
        input_annotations=tsv_dir / "snp_annotation_significant.tsv",
        out_samples_vectors=snp_vec_json,
        out_snp_dic=json_dir / "snp_dic.json",
        out_snp_ids=json_dir / "snp_ids.json",
        out_snp_indices=json_dir / "snp_indices.json"
    ))
    for n_dim in (2, 3):
        p.add(TSneStep(
            input_samples_vectors_json=snp_vec_json,
            output_txt=t_sne_dir / "{}dim.txt".format(n_dim),
            output_png=t_sne_dir / "{}dim.png".format(n_dim),
            n_dimensions=n_dim
        ))
    p.add(DistanceMatrixStep(
        input_samples_vectors_json=snp_vec_json,
        output_matrix_csv=distance_matrix_csv,
        metric=manhattan_dist
    ))
    p.add(DmToExpStep(
        input_csv=distance_matrix_csv,
        output_csv=out_dir / "dm_exp.csv"
    ))
    p.run()


if __name__ == "__main__":
    main()
