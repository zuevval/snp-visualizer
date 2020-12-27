from src.modules.distance_matrix \
    import manhattan_dist, dist_with_allele, manhattan_allele_impact_decorator, \
    manhattan_with_impact_decorator, DistanceMatrixStep, DecoratedDMStep
from src.modules.dm_distrib import DmHistogramStep
from src.modules.dm_exponent import DmToExpStep
from src.modules.heatmap import HeatMapStep
from src.modules.nj_tree import NjStep
from src.modules.tsne import TSneStep
from src.modules.snp_to_vectors import SnpToVectorStep
from src.utils import get_data_path, get_out_path, Pipeline, PipelineStepInterface


def main():
    out_dir = get_out_path() / "real_pipeline"
    p = Pipeline(out_dir / "pipeline.log")

    tsv_dir = get_data_path() / "real_data"
    common_json_dir = out_dir / "json"
    snp_vec_json = common_json_dir / "samples_vectors.json"
    snp_impacts_json = common_json_dir / "snp_impacts.json"

    p.add(SnpToVectorStep(
        input_snp_data=tsv_dir / "snp_data.tsv",
        input_samples=tsv_dir / "snp2sample.tsv",
        input_annotations=tsv_dir / "snp_annotation_significant.tsv",
        out_samples_vectors=snp_vec_json,
        out_snp_dic=common_json_dir / "snp_dic.json",
        out_snp_ids=common_json_dir / "snp_ids.json",
        out_snp_indices=common_json_dir / "snp_indices.json",
        out_snp_impacts=snp_impacts_json
    ))

    t_sne_dir = out_dir / "t_sne"
    for n_dim in (2, 3):
        p.add(TSneStep(
            input_samples_vectors_json=snp_vec_json,
            output_txt=t_sne_dir / "{}dim.txt".format(n_dim),
            output_png=t_sne_dir / "{}dim.png".format(n_dim),
            n_dimensions=n_dim
        ))

    manhattan_dir_name = "manhattan"
    manhattan_with_allele_name = "manhattan_with_allele"
    manhattan_with_impact_dir_name = "manhattan_with_impacts"
    manhattan_impact_allele_name = "manhattan_impacts_alleles"
    csv_filename = "dm.csv"
    distance_mapping = {
        manhattan_dir_name: DistanceMatrixStep(
            input_samples_vectors_json=snp_vec_json,
            output_matrix_csv=out_dir / manhattan_dir_name / csv_filename,
            metric=manhattan_dist
        ),
        manhattan_with_impact_dir_name: DecoratedDMStep(
            input_samples_vectors_json=snp_vec_json,
            input_annotations=snp_impacts_json,
            output_matrix_csv=out_dir / manhattan_with_impact_dir_name / csv_filename,
            metric_decorator=manhattan_with_impact_decorator
        ),
        manhattan_with_allele_name: DistanceMatrixStep(
            input_samples_vectors_json=snp_vec_json,
            output_matrix_csv=out_dir / manhattan_with_allele_name / csv_filename,
            metric=dist_with_allele
        ),
        manhattan_impact_allele_name: DecoratedDMStep(
            input_samples_vectors_json=snp_vec_json,
            input_annotations=snp_impacts_json,
            output_matrix_csv=out_dir / manhattan_impact_allele_name / csv_filename,
            metric_decorator=manhattan_allele_impact_decorator
        )
    }

    for sub_dir_name, dm_step in distance_mapping.items():
        out_dist_dir = out_dir / sub_dir_name  # output directory for the current distance
        distance_matrix_csv = out_dist_dir / csv_filename
        dm_exp_csv = out_dist_dir / "dm_exp.csv"

        p.add(dm_step)
        p.add(DmToExpStep(
            input_csv=distance_matrix_csv,
            output_csv=dm_exp_csv
        ))
        p.add(HeatMapStep(
            input_dm_csv=distance_matrix_csv,
            output_png=out_dist_dir / "heatmap.png"
        ))
        p.add(DmHistogramStep(
            input_csv=distance_matrix_csv,
            output_png=out_dist_dir / "dm_histogram.png"
        ))
        p.add(DmHistogramStep(
            input_csv=dm_exp_csv,
            output_png=out_dist_dir / "dm_histogram_exp.png"
        ))
        p.add(NjStep(
            input_dm_csv=distance_matrix_csv,
            output_dnd=out_dist_dir / "nj.dnd",
            output_png=out_dist_dir / "nj.png"
        ))
    p.run()


if __name__ == "__main__":
    main()
