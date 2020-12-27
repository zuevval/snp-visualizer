import pytest

from src import main
from src.modules.distance_matrix import DistanceMatrixStep, manhattan_dist, manhattan_with_impact_decorator
from src.modules.dm_exponent import DmToExpStep
from src.modules.dm_distrib import DmHistogramStep
from src.modules.heatmap import HeatMapStep
from src.modules.nj_tree import NjStep
from src.modules.snp_to_vectors import SnpToVectorStep
from src.modules.tsne import TSneStep
from src.utils import get_data_path, get_out_path, Pipeline


def test_pipeline():
    out_dir = get_out_path() / "test_pipeline"
    log_file = out_dir / "pipeline.log"
    impacts_file = out_dir / "snp_impacts.json"
    p = Pipeline(log_file)  # log will be empty because of pytest

    snp_vec_json = out_dir / "samples_vectors.json"
    distance_matrix_csv = out_dir / "dm.csv"
    dm_exp_csv = out_dir / "dm_exp.csv"
    p.add(SnpToVectorStep(
        input_snp_data=get_data_path() / "test/snp_data.tsv",
        input_samples=get_data_path() / "test/snp2sample.tsv",
        input_annotations=get_data_path() / "test/snp_annotation.tsv",
        out_samples_vectors=snp_vec_json,
        out_snp_dic=out_dir / "snp_dic.json",
        out_snp_ids=out_dir / "snp_ids.json",
        out_snp_indices=out_dir / "snp_indices.json",
        out_snp_impacts=impacts_file
    ))
    for n_dim in (2, 3):
        p.add(TSneStep(
            input_samples_vectors_json=snp_vec_json,
            output_txt=out_dir / "t_sne{}dim.txt".format(n_dim),
            output_png=out_dir / "t_sne{}dim.png".format(n_dim),
            n_dimensions=n_dim
        ))
    p.add(DistanceMatrixStep(
        input_samples_vectors_json=snp_vec_json,
        output_matrix_csv=distance_matrix_csv,
        metric=manhattan_dist
    ))
    p.add(DmToExpStep(
        input_csv=distance_matrix_csv,
        output_csv=dm_exp_csv
    ))
    p.add(HeatMapStep(
        input_dm_csv=distance_matrix_csv,
        output_png=out_dir / "heatmap.png"
    ))
    p.add(NjStep(
        input_dm_csv=distance_matrix_csv,
        output_dnd=out_dir / "nj.dnd",
        output_png=out_dir / "nj.png"
    ))
    p.add(DmHistogramStep(
        input_csv=distance_matrix_csv,
        output_png=out_dir / "dm_histogram.png"
    ))
    p.add(DmHistogramStep(
        input_csv=dm_exp_csv,
        output_png=out_dir / "dm_histogram_exp.png"
    ))
    # calculate matrix with another metric
    p.add(DistanceMatrixStep(
        input_samples_vectors_json=snp_vec_json,
        output_matrix_csv=out_dir / "dm_manhattan_with_impact.csv",
        metric=manhattan_with_impact_decorator(get_data_path() / "test/impacts.json")
    ))
    p.run()

    assert snp_vec_json.exists()
    assert distance_matrix_csv.exists()
    assert log_file.exists()


@pytest.mark.slow
def test_pipeline_real_run():
    main.main()
